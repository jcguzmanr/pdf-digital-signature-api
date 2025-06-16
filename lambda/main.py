"""
FastAPI Application para procesamiento de PDFs en AWS Lambda
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Union, Optional
import os
import tempfile
import shutil
from datetime import datetime
import boto3
from botocore.exceptions import NoCredentialsError
from mangum import Mangum
import json

# Importar la lógica de procesamiento
from processor import PDFProcessor

# Crear aplicación FastAPI
app = FastAPI(
    title="PDF Editor API on Lambda",
    description="API para insertar texto e imágenes en PDFs, desplegada en AWS Lambda.",
    version="1.1.0"
)

# Configurar CORS para permitir peticiones desde Bubble
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, deberías restringirlo a tu dominio de Bubble
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic (los mismos que tenías)
class Insertion(BaseModel):
    type: str
    source: Optional[str] = None
    content: Optional[str] = None
    position: List[int]
    font_size: Optional[int] = 12
    font_name: Optional[str] = "helv"
    color: Optional[List[float]] = [0, 0, 0]
    width: Optional[int] = None
    height: Optional[int] = None
    rotate: Optional[int] = 0
    flip: Optional[str] = None
    correct_orientation: Optional[bool] = True
    flip_type: Optional[str] = "horizontal"
    pages: Union[str, int, List[int]] = "all"

# Instancia del procesador y cliente S3
processor = PDFProcessor()
s3_client = boto3.client('s3')

# Nombre del bucket S3 desde variables de entorno
S3_BUCKET_NAME = os.environ.get("PDF_BUCKET_NAME", "your-default-bucket-name")

@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "PDF Editor API on Lambda",
        "version": "1.1.0",
        "status": "Running"
    }

@app.post("/upload-and-process")
async def upload_and_process_pdf(
    file: UploadFile = File(...),
    insertions: str = None  # JSON string de las inserciones
):
    """
    Sube un PDF, lo procesa con las instrucciones dadas y lo guarda en S3.
    Devuelve una URL prefirmada para descargar el resultado.
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")

    # Usar el directorio temporal de Lambda para guardar archivos
    with tempfile.TemporaryDirectory() as temp_dir:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_filename = os.path.splitext(file.filename)[0]
        
        input_filename = f"{original_filename}_{timestamp}.pdf"
        output_filename = f"processed_{input_filename}"
        
        input_path = os.path.join(temp_dir, input_filename)
        output_path = os.path.join(temp_dir, output_filename)
        
        # Guardar archivo subido
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Parsear instrucciones de inserción desde el string JSON
        try:
            insertions_data = json.loads(insertions) if insertions else []
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="El JSON de inserciones es inválido")

        # Preparar datos para el procesador
        pdf_data = {
            "pdf_path": input_path,
            "output_path": output_path,
            "insertions": insertions_data
        }
        
        try:
            # Procesar el PDF
            processor.process_pdf(pdf_data)

            # Subir el archivo procesado a S3
            s3_client.upload_file(output_path, S3_BUCKET_NAME, output_filename)

            # Generar una URL prefirmada para el archivo
            presigned_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': S3_BUCKET_NAME, 'Key': output_filename},
                ExpiresIn=3600  # La URL expira en 1 hora
            )
            
            return {
                "success": True,
                "message": "PDF procesado y subido a S3 exitosamente.",
                "download_url": presigned_url,
                "s3_bucket": S3_BUCKET_NAME,
                "s3_key": output_filename
            }

        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except NoCredentialsError:
            raise HTTPException(status_code=500, detail="Credenciales de AWS no configuradas.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

# Handler de Mangum para AWS Lambda
handler = Mangum(app) 