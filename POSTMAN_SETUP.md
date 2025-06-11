# 📬 POSTMAN COLLECTION - PDF Editor API

Esta colección de Postman te permite probar todos los endpoints de la **PDF Editor API** de manera fácil y organizada.

## 📦 ARCHIVOS INCLUIDOS

- `PDF_Editor_API.postman_collection.json` - Colección completa con todos los endpoints
- `PDF_Editor_API.postman_environment.json` - Entorno con variables configuradas
- `POSTMAN_SETUP.md` - Este archivo con instrucciones

## 🚀 IMPORTACIÓN RÁPIDA

### 1. Importar Colección
1. Abrir Postman
2. Click en **Import** (esquina superior izquierda)
3. Arrastrar el archivo `PDF_Editor_API.postman_collection.json`
4. Click **Import**

### 2. Importar Entorno
1. Click en **Import** nuevamente
2. Arrastrar el archivo `PDF_Editor_API.postman_environment.json`
3. Click **Import**
4. Seleccionar el entorno "PDF Editor API - Local" en el dropdown superior derecho

## 📋 ENDPOINTS INCLUIDOS

```
┌─────────────────────────────────────────────────────────────────┐
│                    POSTMAN COLLECTION                          │
└─────────────────────────────────────────────────────────────────┘

🏠 API Info                    GET    /
🏥 Health Check               GET    /health
📁 List Files                 GET    /list-files
📄 Process PDF - Simple       POST   /process-pdf
📄 Process PDF - Complete     POST   /process-pdf
📤 Upload & Process PDF       POST   /upload-pdf
📥 Download Processed File    GET    /download/{filename}
📚 API Documentation          GET    /docs
```

## 🔧 CONFIGURACIÓN PREVIA

### 1. Asegúrate de que el servidor esté corriendo:
```bash
cd /path/to/edit-pdf
source venv/bin/activate
python main.py
```

### 2. Verificar que el servidor responde:
```bash
curl http://localhost:8000/health
```

## 🧪 ORDEN DE PRUEBA RECOMENDADO

### **Fase 1: Verificación**
1. **🏥 Health Check** - Verificar que la API está funcionando
2. **🏠 API Info** - Ver información general de la API
3. **📁 List Files** - Ver archivos disponibles

### **Fase 2: Procesamiento Básico**
4. **📄 Process PDF - Simple** - Procesar con inserción básica
5. **📥 Download Processed File** - Descargar el resultado

### **Fase 3: Procesamiento Avanzado**
6. **📄 Process PDF - Complete** - Procesar con múltiples insercciones
7. **📤 Upload & Process PDF** - Subir y procesar en una operación

### **Fase 4: Documentación**
8. **📚 API Documentation** - Ver Swagger UI

## ⚡ CARACTERÍSTICAS ESPECIALES

### 🔄 Variables Automáticas
- **{{baseUrl}}** - URL base del servidor (http://localhost:8000)
- **{{lastProcessedFile}}** - Se actualiza automáticamente con el último archivo procesado

### 🧪 Tests Automáticos
Cada endpoint incluye tests que verifican:
- ✅ Status code 200
- ✅ Estructura de respuesta correcta
- ✅ Tipo de contenido apropiado
- ✅ Datos específicos de la API

### 📊 Scripts Pre/Post Request
- **Pre-request**: Log de inicio con timestamp
- **Post-request**: Log de respuesta con tiempo de ejecución

### 🎯 Ejemplos Realistas
Cada endpoint incluye:
- **Headers** apropiados
- **Body** con ejemplos reales
- **Descriptions** detalladas
- **Tests** automáticos

## 🎨 EJEMPLOS DE JSON INCLUIDOS

### Simple Processing:
```json
{
  "pdf_path": "input/documento.pdf",
  "output_path": "output/documento_firmado_postman.pdf",
  "insertions": [
    {
      "type": "text",
      "content": "Firmado electrónicamente según Ley N° 27269.",
      "position": [50, 30],
      "font_size": 9,
      "pages": "all"
    }
  ]
}
```

### Complete Processing:
```json
{
  "pdf_path": "input/documento.pdf",
  "output_path": "output/documento_completo_postman.pdf",
  "insertions": [
    {
      "type": "text",
      "content": "DOCUMENTO OFICIAL",
      "position": [200, 50],
      "font_size": 16,
      "color": [0, 0, 1],
      "pages": "first"
    },
    {
      "type": "image",
      "source": "assets/rubrica_realista.png",
      "position": [400, 100],
      "width": 120,
      "height": 60,
      "pages": "last"
    }
  ]
}
```

## 🔧 PERSONALIZACIÓN

### Cambiar URL del Servidor:
1. Ir a **Environments** en Postman
2. Seleccionar "PDF Editor API - Local"
3. Cambiar el valor de `baseUrl` (ej: `http://localhost:8001`)

### Añadir Nuevos Endpoints:
1. Right-click en la colección
2. **Add Request**
3. Configurar método, URL y body
4. Añadir tests si es necesario

## 🚨 TROUBLESHOOTING

### ❌ "Could not get any response"
- Verificar que el servidor esté corriendo
- Verificar que la URL base sea correcta
- Comprobar firewall/antivirus

### ❌ "404 Not Found"
- Verificar que el endpoint existe
- Revisar la documentación en `/docs`

### ❌ "500 Internal Server Error"
- Revisar los logs del servidor
- Verificar que los archivos existan en las rutas especificadas
- Comprobar formato del JSON

## 📱 EXPORTAR RESULTADOS

Para compartir resultados:
1. Ejecutar la colección completa: **Collection Runner**
2. Exportar resultados: **Export Results**
3. Generar reporte: **Generate Report**

---

## 🎯 ¡LISTO PARA PROBAR!

Con esta colección podrás:
- ✅ Probar todos los endpoints de manera organizada
- ✅ Ver tests automáticos en acción
- ✅ Experimentar con diferentes parámetros
- ✅ Generar reportes de pruebas
- ✅ Documentar casos de uso

**¡Importa la colección y comienza a probar tu API inmediatamente!** 🚀 