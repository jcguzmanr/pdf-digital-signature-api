# 🔒 PDF Digital Signature API

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com)
[![PyMuPDF](https://img.shields.io/badge/PyMuPDF-1.23.8-red.svg)](https://pymupdf.readthedocs.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 🚀 **API profesional para inserción de texto, rúbricas y códigos QR en documentos PDF**
> 
> ✨ **Desarrollado con FastAPI y PyMuPDF | Preparado para AWS Lambda**

![Demo](https://img.shields.io/badge/Demo-TikTok%20Ready-ff69b4.svg)

## 🚀 Características

- ✅ Inserción de texto personalizado en cualquier posición
- ✅ Inserción de imágenes (rúbricas, QR, etc.)
- ✅ Soporte para páginas específicas o todas las páginas
- ✅ API REST con FastAPI
- ✅ Documentación automática con Swagger
- ✅ Preparado para migración a AWS Lambda
- ✅ Interfaz local para testing

## 📂 Estructura del Proyecto

```
edit-pdf/
├── main.py              # API FastAPI
├── processor.py         # Lógica de procesamiento PDF
├── requirements.txt     # Dependencias Python
├── test.json           # JSON de ejemplo
├── README.md           # Este archivo
├── venv/              # Entorno virtual
├── input/             # PDFs originales
├── output/            # PDFs procesados
└── assets/            # Imágenes (rúbricas, QR, etc.)
```

## 🛠️ Instalación y Configuración

### 1. Activar el entorno virtual
```bash
source venv/bin/activate
```

### 2. Verificar dependencias (ya instaladas)
```bash
pip list
```

### 3. Crear assets de ejemplo
```bash
python processor.py
```

## 🏃‍♂️ Ejecución

### Iniciar el servidor
```bash
python main.py
```

La API estará disponible en:
- **Servidor**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📋 Endpoints Disponibles

### `GET /`
Información general de la API

### `GET /health`
Estado de salud de la API y directorios

### `POST /process-pdf`
Procesar PDF con instrucciones JSON

**Ejemplo de body:**
```json
{
  "pdf_path": "input/documento.pdf",
  "output_path": "output/documento_firmado.pdf",
  "insertions": [
    {
      "type": "text",
      "content": "Firmado electrónicamente según Ley N° 27269.",
      "position": [50, 30],
      "font_size": 9,
      "pages": "all"
    },
    {
      "type": "image",
      "source": "assets/rubrica.png",
      "position": [400, 100],
      "pages": 3
    }
  ]
}
```

### `POST /upload-pdf`
Subir PDF y procesar en una sola operación

### `GET /download/{filename}`
Descargar archivo procesado

### `GET /list-files`
Listar archivos en todos los directorios

## 📝 Formato de Inserción

### Inserción de Texto
```json
{
  "type": "text",
  "content": "Texto a insertar",
  "position": [x, y],
  "font_size": 12,
  "font_name": "helv",
  "color": [0, 0, 0],
  "pages": "all"
}
```

### Inserción de Imagen
```json
{
  "type": "image",
  "source": "assets/imagen.png",
  "position": [x, y],
  "width": 100,
  "height": 50,
  "pages": "last"
}
```

### Opciones de Páginas
- `"all"`: Todas las páginas
- `"first"`: Primera página
- `"last"`: Última página
- `3`: Página específica (número)
- `[1, 3, 5]`: Lista de páginas

## 🧪 Testing con cURL

### Verificar estado
```bash
curl http://localhost:8000/health
```

### Procesar PDF
```bash
curl -X POST "http://localhost:8000/process-pdf" \
  -H "Content-Type: application/json" \
  -d @test.json
```

### Listar archivos
```bash
curl http://localhost:8000/list-files
```

## 📱 Testing con Postman

1. Importar la colección desde: `http://localhost:8000/docs`
2. Usar el JSON de `test.json` como body
3. Cambiar el método a POST
4. URL: `http://localhost:8000/process-pdf`

## 🔧 Preparación para AWS Lambda

El código ya está preparado para migrar a AWS Lambda:

1. **Usar Mangum** para el handler ASGI:
```python
from mangum import Mangum
handler = Mangum(app)
```

2. **Modificar el procesador** para usar `io.BytesIO` en lugar de archivos locales

3. **Configurar variables de entorno** para S3 o almacenamiento en la nube

## 🚨 Troubleshooting

### Error: "Archivo PDF no encontrado"
- Asegúrate de que el PDF esté en la carpeta `input/`
- Verifica la ruta en el JSON

### Error: "Archivo de imagen no encontrado"
- Verifica que las imágenes estén en `assets/`
- Ejecuta `python processor.py` para crear imágenes de ejemplo

### Puerto en uso
```bash
# Cambiar puerto en main.py o usar:
uvicorn main:app --port 8001
```

## 📦 Dependencias Principales

- **FastAPI**: Framework web moderno
- **PyMuPDF (fitz)**: Manipulación de PDFs
- **Uvicorn**: Servidor ASGI
- **Pillow**: Procesamiento de imágenes
- **Pydantic**: Validación de datos

## 📄 Licencia

Proyecto de ejemplo para procesamiento de PDFs con FastAPI. 