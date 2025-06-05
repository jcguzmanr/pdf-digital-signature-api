"""
FastAPI Application para procesamiento de PDFs
API que recibe JSON con instrucciones y devuelve PDFs modificados
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Union, Optional
import os
import tempfile
import shutil
from datetime import datetime

from processor import PDFProcessor, create_sample_assets

# Crear aplicación FastAPI
app = FastAPI(
    title="PDF Editor API",
    description="API para insertar texto e imágenes en PDFs",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class Insertion(BaseModel):
    type: str  # "text" o "image"
    content: Optional[str] = None  # Para texto
    source: Optional[str] = None   # Para imagen
    position: List[int]
    font_size: Optional[int] = 12
    font_name: Optional[str] = "helv"
    color: Optional[List[float]] = [0, 0, 0]
    width: Optional[int] = None
    height: Optional[int] = None
    pages: Union[str, int, List[int]] = "all"

class PDFRequest(BaseModel):
    pdf_path: str
    output_path: str
    insertions: List[Insertion]

class ProcessResponse(BaseModel):
    success: bool
    message: str
    output_path: Optional[str] = None
    processed_at: str

# Instancia del procesador
processor = PDFProcessor()

@app.on_event("startup")
async def startup_event():
    """Evento de inicio - crear assets de ejemplo"""
    create_sample_assets()
    print("✅ API iniciada correctamente")
    print("📁 Estructura de carpetas verificada")

@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "PDF Editor API",
        "version": "1.0.0",
        "endpoints": {
            "POST /process-pdf": "Procesar PDF con instrucciones JSON",
            "POST /upload-pdf": "Subir PDF y procesar",
            "GET /download/{filename}": "Descargar archivo procesado",
            "GET /health": "Estado de la API"
        },
        "documentation": "/docs"
    }

@app.get("/health")
async def health_check():
    """Verificar estado de la API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "directories": {
            "input": os.path.exists("input"),
            "output": os.path.exists("output"),
            "assets": os.path.exists("assets")
        }
    }

@app.post("/process-pdf", response_model=ProcessResponse)
async def process_pdf(request: PDFRequest):
    """
    Procesar un PDF con las instrucciones proporcionadas
    
    Args:
        request: Objeto PDFRequest con las instrucciones
        
    Returns:
        ProcessResponse: Respuesta con el resultado del procesamiento
    """
    try:
        # Convertir el request a diccionario
        pdf_data = {
            "pdf_path": request.pdf_path,
            "output_path": request.output_path,
            "insertions": [insertion.dict() for insertion in request.insertions]
        }
        
        # Procesar el PDF
        output_path = processor.process_pdf(pdf_data)
        
        return ProcessResponse(
            success=True,
            message="PDF procesado exitosamente",
            output_path=output_path,
            processed_at=datetime.now().isoformat()
        )
        
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.post("/upload-pdf")
async def upload_and_process_pdf(
    file: UploadFile = File(...),
    insertions: str = None  # JSON string de las inserciones
):
    """
    Subir un PDF y procesarlo con instrucciones
    
    Args:
        file: Archivo PDF subido
        insertions: JSON string con las instrucciones de inserción
        
    Returns:
        FileResponse: PDF procesado para descarga
    """
    try:
        import json
        
        # Validar que es un PDF
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")
        
        # Crear nombres de archivo temporales
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        input_filename = f"uploaded_{timestamp}.pdf"
        output_filename = f"processed_{timestamp}.pdf"
        
        input_path = os.path.join("input", input_filename)
        output_path = os.path.join("output", output_filename)
        
        # Guardar archivo subido
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Parsear instrucciones
        if insertions:
            try:
                insertions_data = json.loads(insertions)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="JSON de instrucciones inválido")
        else:
            insertions_data = []
        
        # Preparar datos para procesamiento
        pdf_data = {
            "pdf_path": input_path,
            "output_path": output_path,
            "insertions": insertions_data
        }
        
        # Procesar PDF
        processor.process_pdf(pdf_data)
        
        # Devolver archivo procesado
        return FileResponse(
            path=output_path,
            filename=output_filename,
            media_type="application/pdf"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando archivo: {str(e)}")

@app.get("/download/{filename}")
async def download_file(filename: str):
    """
    Descargar un archivo del directorio output
    
    Args:
        filename: Nombre del archivo a descargar
        
    Returns:
        FileResponse: Archivo para descarga
    """
    file_path = os.path.join("output", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/pdf"
    )

@app.get("/list-files")
async def list_files():
    """Listar archivos disponibles en cada directorio"""
    def list_dir_contents(directory):
        if os.path.exists(directory):
            return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        return []
    
    return {
        "input": list_dir_contents("input"),
        "output": list_dir_contents("output"),
        "assets": list_dir_contents("assets")
    }

# Función para preparar para AWS Lambda
def lambda_handler(event, context):
    """
    Handler para AWS Lambda usando Mangum
    Esta función se usará cuando se migre a Lambda
    """
    from mangum import Mangum
    handler = Mangum(app)
    return handler(event, context)

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Iniciando servidor FastAPI...")
    print("📖 Documentación disponible en: http://localhost:8000/docs")
    print("🔧 API disponible en: http://localhost:8000")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 