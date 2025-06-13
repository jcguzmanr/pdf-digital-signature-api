import json

def generate_ultra_dense_grid():
    """Genera un template ultra-denso con intervalos de 10 puntos"""
    
    template = {
        "pdf_path": "https://thelegalbinder.com/version-test/fileupload/f1749447582865x354337285212396500/Acta%20de%20acuerdo%20de%20compromiso.pdf",
        "output_path": "output/template_coordenadas_ultra_dense.pdf",
        "insertions": []
    }
    
    # Intervalos ultra-pequeños para máxima precisión
    x_step = 10  # 10 puntos
    y_step = 10  # 10 puntos
    max_x = 595  # A4 width
    max_y = 842  # A4 height
    
    # Colores más sutiles para no saturar visualmente
    colors = {
        (0, 100): [0.8, 0, 0],      # Rojo suave
        (100, 200): [0.8, 0.2, 0],  # Rojo-naranja suave
        (200, 300): [0.8, 0.4, 0],  # Naranja suave
        (300, 400): [0.8, 0.6, 0],  # Amarillo-naranja suave
        (400, 500): [0.6, 0.8, 0],  # Verde-amarillo suave
        (500, 600): [0.4, 0.8, 0],  # Verde suave
        (600, 700): [0, 0.8, 0.4],  # Verde-azul suave
        (700, 800): [0, 0.6, 0.8],  # Azul suave
        (800, 900): [0.2, 0.4, 0.8] # Azul-morado suave
    }
    
    # Generar cuadrícula ultra-densa
    for y in range(0, max_y + 1, y_step):
        for x in range(0, max_x + 1, x_step):
            # Color basado en zona Y
            color = [0.4, 0, 0.4]  # Morado suave por defecto
            for (y_min, y_max), col in colors.items():
                if y_min <= y < y_max:
                    color = col
                    break
            
            insertion = {
                "type": "text",
                "content": f"({x},{y})",
                "position": [x, y],
                "font_size": 3,  # Fuente muy pequeña
                "color": color,
                "font_name": "helv",
                "pages": "all"
            }
            template["insertions"].append(insertion)
    
    # Guardar template
    with open("template_coordinates_ultra_dense.json", "w", encoding="utf-8") as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Template ultra-denso generado con {len(template['insertions'])} coordenadas")
    print(f"📍 Intervalos: {x_step}x{y_step} puntos (máxima precisión)")
    print(f"📄 Cobertura: PDF A4 completo (595x842 puntos)")
    
    return template

if __name__ == "__main__":
    generate_ultra_dense_grid() 