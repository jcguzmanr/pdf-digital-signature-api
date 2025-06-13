# 📍 Templates de Coordenadas para PDF

Este proyecto incluye varios templates de coordenadas que forman cuadrículas perfectas para posicionamiento preciso en PDFs A4.

## 🎯 Templates Disponibles

### 1. Template Básico (25x25 puntos)
- **Archivo:** `template_coordinates_grid.json`
- **Coordenadas:** 816 puntos
- **Intervalos:** 25x25 puntos
- **Cobertura:** (0,0) a (595,842)
- **Fuente:** 4pt
- **Uso:** Posicionamiento general con buena precisión

### 2. Template Ultra-Denso (10x10 puntos)
- **Archivo:** `template_coordinates_ultra_dense.json`
- **Coordenadas:** 5,100 puntos
- **Intervalos:** 10x10 puntos
- **Cobertura:** (0,0) a (595,842)
- **Fuente:** 3pt
- **Uso:** Máxima precisión para posicionamiento fino

## 📐 Especificaciones Técnicas

### Dimensiones PDF A4
- **Ancho:** 595 puntos
- **Alto:** 842 puntos
- **Origen:** (0,0) esquina inferior izquierda
- **Sistema:** Coordenadas PDF estándar

### Sistema de Colores por Zonas
```
Y: 0-100   → Rojo        (zona inferior)
Y: 100-200 → Rojo-Naranja
Y: 200-300 → Naranja
Y: 300-400 → Amarillo-Naranja
Y: 400-500 → Verde-Amarillo
Y: 500-600 → Verde
Y: 600-700 → Verde-Azul
Y: 700-800 → Azul
Y: 800-842 → Azul-Morado  (zona superior)
```

## 🚀 Uso de los Templates

### Generar Template Básico
```bash
python generate_grid_template.py
```

### Generar Template Ultra-Denso
```bash
python generate_ultra_dense_grid.py
```

### Procesar PDF con Template
```bash
curl -X POST "http://localhost:8000/process-pdf" \
  -H "Content-Type: application/json" \
  -d @template_coordinates_grid.json
```

## 📊 Comparación de Templates

| Template | Coordenadas | Intervalos | Precisión | Tamaño Archivo |
|----------|-------------|------------|-----------|----------------|
| Básico   | 816         | 25x25      | Alta      | ~685KB         |
| Ultra-Denso | 5,100    | 10x10      | Máxima    | ~2-3MB         |

## 💡 Recomendaciones

- **Template Básico:** Ideal para la mayoría de casos de uso
- **Template Ultra-Denso:** Para trabajos que requieren precisión milimétrica
- **Colores:** Facilitan la identificación visual de zonas en el PDF
- **Coordenadas:** Formato (x,y) donde x=horizontal, y=vertical

## 🔧 Personalización

Para crear templates personalizados, modifica los parámetros en los scripts:
- `x_step`, `y_step`: Intervalos de la cuadrícula
- `max_x`, `max_y`: Dimensiones máximas
- `font_size`: Tamaño del texto de coordenadas
- `colors`: Esquema de colores por zonas 