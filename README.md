# 📄 PDF Digital Signature API

API REST para procesamiento de PDFs con inserción de imágenes, texto y firmas digitales. Incluye sistema completo de templates de coordenadas para posicionamiento preciso.

## 🚀 Características Principales

- ✅ **Inserción de imágenes** con posicionamiento preciso
- ✅ **Inserción de texto** con múltiples fuentes y colores
- ✅ **Sistema de coordenadas optimizado** para PDFs A4
- ✅ **Templates de cuadrícula** para referencia visual
- ✅ **Corrección automática de orientación** PyMuPDF
- ✅ **Validación de entrada** con Pydantic
- ✅ **API REST** con FastAPI
- ✅ **Documentación automática** con Swagger/OpenAPI

## 📍 Sistema de Templates de Coordenadas

### Templates Disponibles

| Template | Coordenadas | Intervalos | Uso Recomendado |
|----------|-------------|------------|-----------------|
| **Debug** | 5 | N/A | Verificación de esquinas |
| **Optimizado** ⭐ | 1,189 | 20x20 | **Uso general** |
| **Básico** | 816 | 25x25 | Proyectos simples |
| **Ultra-Denso** | 5,100 | 10x10 | Máxima precisión |

### 🎯 Template Recomendado
**`template_coordinates_optimized.json`** - Ideal para la mayoría de casos:
- Margen seguro de 15 puntos
- Cobertura completa sin espacios en blanco
- Basado en dimensiones reales del PDF (595x842 puntos)

## 🛠️ Instalación

### Prerrequisitos
- Python 3.8+
- pip

### Configuración
```bash
# Clonar repositorio
git clone https://github.com/jcguzmanr/pdf-digital-signature-api.git
cd pdf-digital-signature-api

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor
python main.py
```

## 📖 Uso de la API

### Endpoint Principal
```
POST http://localhost:8000/process-pdf
```

### Estructura de Request
```json
{
  "pdf_path": "URL_del_PDF",
  "output_path": "output/resultado.pdf",
  "insertions": [
    {
      "type": "text",
      "content": "Texto a insertar",
      "position": [x, y],
      "font_size": 12,
      "color": [0, 0, 0],
      "font_name": "helv",
      "pages": "all"
    },
    {
      "type": "image",
      "image_path": "URL_de_imagen",
      "position": [x, y],
      "size": [width, height],
      "pages": "all"
    }
  ]
}
```

### Ejemplo con Template de Coordenadas
```bash
curl -X POST "http://localhost:8000/process-pdf" \
  -H "Content-Type: application/json" \
  -d @template_coordinates_optimized.json
```

## 🔧 Herramientas de Debug

### Análisis de PDF
```bash
python debug_pdf_dimensions.py
```
Analiza las dimensiones reales del PDF y genera templates optimizados.

### Generación de Templates
```bash
python generate_ultra_dense_grid.py
```
Genera templates personalizados con diferentes densidades.

## 📐 Sistema de Coordenadas

### Información Técnica
- **Origen:** (0,0) en esquina inferior izquierda
- **Dimensiones A4:** 595 x 842 puntos
- **Coordenadas:** Enteros requeridos
- **Margen recomendado:** 15-20 puntos

### Colores por Zonas
```
Y: 0-168   → Rojo        (zona inferior)
Y: 168-336 → Naranja     
Y: 336-504 → Amarillo    
Y: 504-672 → Verde       
Y: 672-842 → Azul        (zona superior)
```

## 📁 Estructura del Proyecto

```
pdf-digital-signature-api/
├── main.py                              # Servidor FastAPI
├── processor.py                         # Lógica de procesamiento
├── requirements.txt                     # Dependencias
├── README.md                           # Este archivo
├── DEBUG_RESULTS.md                    # Resultados del debug
├── README_templates.md                 # Guía de templates
├── debug_pdf_dimensions.py             # Script de análisis
├── generate_ultra_dense_grid.py        # Generador de templates
├── assets/                             # Imágenes de ejemplo
│   ├── sello_circular_rb.png
│   ├── sello_kb_original.png
│   └── sello_rb_100.png
├── templates/                          # Templates de coordenadas
│   ├── debug_coordinates_test.json
│   ├── template_coordinates_optimized.json ⭐
│   ├── template_coordinates_grid.json
│   └── template_coordinates_ultra_dense.json
├── output/                             # PDFs generados
└── input/                              # PDFs de entrada
```

## 🧪 Testing con Postman

1. Importar colección: `PDF_Editor_API.postman_collection.json`
2. Configurar entorno: `PDF_Editor_API.postman_environment.json`
3. Ver guía: `POSTMAN_SETUP.md`

## 📊 Endpoints Disponibles

### Procesamiento de PDF
- `POST /process-pdf` - Procesar PDF con inserciones
- `GET /` - Página de inicio
- `GET /docs` - Documentación Swagger
- `GET /health` - Estado del servidor

### Respuesta de Éxito
```json
{
  "success": true,
  "message": "PDF procesado exitosamente",
  "output_path": "output/resultado.pdf",
  "processed_at": "2024-01-15T10:30:00"
}
```

## 🔍 Debug y Troubleshooting

### Problemas Comunes

1. **Coordenadas decimales**
   - ❌ Error: `Input should be a valid integer`
   - ✅ Solución: Usar coordenadas enteras

2. **Texto fuera de límites**
   - ❌ Problema: Texto cortado en bordes
   - ✅ Solución: Usar márgenes de 15-20 puntos

3. **Orientación invertida**
   - ❌ Problema: Imágenes/texto al revés
   - ✅ Solución: Sistema automático de corrección incluido

### Logs de Debug
El sistema incluye logs detallados:
```
📍 Insertando texto en: (100, 200) con flip vertical
📐 Rectángulo de inserción: Rect(50.0, 150.0, 150.0, 250.0)
✅ Elemento insertado exitosamente
```

## 🚀 Próximos Pasos

- [ ] Migración a AWS Lambda
- [ ] Soporte para más formatos de imagen
- [ ] Templates dinámicos por tipo de documento
- [ ] API de gestión de templates
- [ ] Integración con servicios de almacenamiento

## 📄 Licencia

MIT License - Ver archivo `LICENSE` para detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📞 Soporte

Para soporte técnico o preguntas:
- Crear issue en GitHub
- Revisar documentación en `/docs`
- Consultar `DEBUG_RESULTS.md` para troubleshooting

---

⭐ **¡Dale una estrella al proyecto si te resulta útil!** 