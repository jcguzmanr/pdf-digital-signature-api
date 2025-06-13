import fitz  # PyMuPDF
import requests
import tempfile
import os
import json

def debug_pdf_dimensions(pdf_url):
    """Analiza las dimensiones reales del PDF y sistema de coordenadas"""
    
    print("🔍 ANÁLISIS DE DIMENSIONES PDF")
    print("=" * 50)
    
    # Descargar PDF temporal
    print(f"📥 Descargando PDF desde: {pdf_url}")
    response = requests.get(pdf_url)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        temp_file.write(response.content)
        temp_path = temp_file.name
    
    try:
        # Abrir PDF con PyMuPDF
        doc = fitz.open(temp_path)
        
        print(f"📄 Número de páginas: {len(doc)}")
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            print(f"\n📖 PÁGINA {page_num + 1}")
            print("-" * 30)
            
            # Obtener dimensiones de la página
            rect = page.rect
            print(f"📐 Rectángulo de página: {rect}")
            print(f"📏 Ancho: {rect.width} puntos")
            print(f"📏 Alto: {rect.height} puntos")
            print(f"📍 Esquina inferior izquierda: ({rect.x0}, {rect.y0})")
            print(f"📍 Esquina superior derecha: ({rect.x1}, {rect.y1})")
            
            # Información del sistema de coordenadas
            print(f"\n🎯 SISTEMA DE COORDENADAS:")
            print(f"   • Origen (0,0): Esquina inferior izquierda")
            print(f"   • X máximo: {rect.width}")
            print(f"   • Y máximo: {rect.height}")
            
            # Detectar formato de página
            if abs(rect.width - 595) < 10 and abs(rect.height - 842) < 10:
                format_name = "A4 Portrait"
            elif abs(rect.width - 842) < 10 and abs(rect.height - 595) < 10:
                format_name = "A4 Landscape"
            elif abs(rect.width - 612) < 10 and abs(rect.height - 792) < 10:
                format_name = "Letter Portrait"
            else:
                format_name = "Formato personalizado"
            
            print(f"📋 Formato detectado: {format_name}")
            
            # Probar inserción de texto en esquinas para verificar coordenadas
            print(f"\n🧪 PRUEBA DE COORDENADAS:")
            test_coordinates = [
                (0, 0, "Esquina inferior izquierda"),
                (rect.width, 0, "Esquina inferior derecha"),
                (0, rect.height, "Esquina superior izquierda"),
                (rect.width, rect.height, "Esquina superior derecha"),
                (rect.width/2, rect.height/2, "Centro"),
            ]
            
            for x, y, description in test_coordinates:
                print(f"   • {description}: ({x:.0f}, {y:.0f})")
            
            # Crear template de prueba con coordenadas de esquinas
            test_template = {
                "pdf_path": pdf_url,
                "output_path": "output/debug_coordinates_test.pdf",
                "insertions": []
            }
            
            colors = [
                [1, 0, 0],    # Rojo
                [0, 1, 0],    # Verde
                [0, 0, 1],    # Azul
                [1, 1, 0],    # Amarillo
                [1, 0, 1],    # Magenta
            ]
            
            for i, (x, y, description) in enumerate(test_coordinates):
                # Ajustar coordenadas para que el texto sea visible
                adj_x = int(max(10, min(x, rect.width - 50)))
                adj_y = int(max(10, min(y, rect.height - 10)))
                
                insertion = {
                    "type": "text",
                    "content": f"{description}\n({adj_x},{adj_y})",
                    "position": [adj_x, adj_y],
                    "font_size": 8,
                    "color": colors[i % len(colors)],
                    "font_name": "helv",
                    "pages": "all"
                }
                test_template["insertions"].append(insertion)
            
            # Guardar template de prueba
            with open("debug_coordinates_test.json", "w", encoding="utf-8") as f:
                json.dump(test_template, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Template de prueba guardado: debug_coordinates_test.json")
            
            # Generar recomendaciones para cuadrícula
            print(f"\n💡 RECOMENDACIONES PARA CUADRÍCULA:")
            
            # Calcular intervalos óptimos
            optimal_x_step = max(10, int(rect.width / 25))  # ~25 divisiones en X
            optimal_y_step = max(10, int(rect.height / 35)) # ~35 divisiones en Y
            
            print(f"   • Intervalo X recomendado: {optimal_x_step} puntos")
            print(f"   • Intervalo Y recomendado: {optimal_y_step} puntos")
            print(f"   • Coordenadas totales estimadas: {int(rect.width/optimal_x_step) * int(rect.height/optimal_y_step)}")
            
            # Márgenes seguros
            safe_margin = 20
            print(f"   • Margen seguro recomendado: {safe_margin} puntos")
            print(f"   • Área útil: ({safe_margin}, {safe_margin}) a ({rect.width-safe_margin:.0f}, {rect.height-safe_margin:.0f})")
            
        doc.close()
        
    finally:
        # Limpiar archivo temporal
        os.unlink(temp_path)
        print(f"\n🗑️ Archivo temporal eliminado")

def generate_optimal_grid(pdf_url):
    """Genera una cuadrícula optimizada basada en las dimensiones reales del PDF"""
    
    print(f"\n🎯 GENERANDO CUADRÍCULA OPTIMIZADA")
    print("=" * 50)
    
    # Obtener dimensiones del PDF
    response = requests.get(pdf_url)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        temp_file.write(response.content)
        temp_path = temp_file.name
    
    try:
        doc = fitz.open(temp_path)
        page = doc[0]  # Primera página
        rect = page.rect
        doc.close()
        
        # Parámetros optimizados
        margin = 15  # Margen seguro
        x_step = 20  # Intervalo X
        y_step = 20  # Intervalo Y
        
        # Área útil
        start_x = margin
        end_x = rect.width - margin
        start_y = margin
        end_y = rect.height - margin
        
        template = {
            "pdf_path": pdf_url,
            "output_path": "output/template_coordenadas_optimized.pdf",
            "insertions": []
        }
        
        # Colores por zonas Y
        colors = {
            (0, rect.height * 0.2): [1, 0, 0],        # Rojo - Zona inferior
            (rect.height * 0.2, rect.height * 0.4): [1, 0.5, 0],  # Naranja
            (rect.height * 0.4, rect.height * 0.6): [1, 1, 0],    # Amarillo
            (rect.height * 0.6, rect.height * 0.8): [0, 1, 0],    # Verde
            (rect.height * 0.8, rect.height): [0, 0, 1],          # Azul
        }
        
        # Generar cuadrícula
        coord_count = 0
        for y in range(int(start_y), int(end_y) + 1, y_step):
            for x in range(int(start_x), int(end_x) + 1, x_step):
                # Seleccionar color
                color = [0.5, 0, 0.5]  # Morado por defecto
                for (y_min, y_max), col in colors.items():
                    if y_min <= y < y_max:
                        color = col
                        break
                
                insertion = {
                    "type": "text",
                    "content": f"({x},{y})",
                    "position": [x, y],
                    "font_size": 4,
                    "color": color,
                    "font_name": "helv",
                    "pages": "all"
                }
                template["insertions"].append(insertion)
                coord_count += 1
        
        # Guardar template optimizado
        with open("template_coordinates_optimized.json", "w", encoding="utf-8") as f:
            json.dump(template, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Template optimizado generado con {coord_count} coordenadas")
        print(f"📍 Área cubierta: ({start_x}, {start_y}) a ({end_x:.0f}, {end_y:.0f})")
        print(f"📏 Dimensiones PDF: {rect.width:.0f} x {rect.height:.0f} puntos")
        print(f"💾 Archivo: template_coordinates_optimized.json")
        
    finally:
        os.unlink(temp_path)

if __name__ == "__main__":
    pdf_url = "https://thelegalbinder.com/version-test/fileupload/f1749447582865x354337285212396500/Acta%20de%20acuerdo%20de%20compromiso.pdf"
    
    # Análisis completo
    debug_pdf_dimensions(pdf_url)
    
    # Generar cuadrícula optimizada
    generate_optimal_grid(pdf_url) 