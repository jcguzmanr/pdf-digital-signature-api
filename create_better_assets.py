"""
Script para crear assets más realistas para el demo de TikTok
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_realistic_signature():
    """Crear una rúbrica más realista"""
    # Crear imagen de 120x60 con fondo transparente
    img = Image.new('RGBA', (120, 60), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Simular una firma manuscrita con curvas
    # Línea principal de la firma
    draw.ellipse([10, 15, 110, 45], outline=(0, 0, 139, 180), width=2)
    draw.line([20, 30, 100, 30], fill=(0, 0, 139, 180), width=3)
    draw.line([30, 20, 90, 40], fill=(0, 0, 139, 180), width=2)
    draw.line([40, 35, 80, 25], fill=(0, 0, 139, 180), width=2)
    
    # Agregar "flourish" al final
    draw.arc([80, 10, 110, 40], start=0, end=180, fill=(0, 0, 139, 180), width=2)
    
    img.save('assets/rubrica_realista.png')
    print("✅ Rúbrica realista creada")

def create_realistic_qr():
    """Crear un QR más realista con patrón"""
    # Crear imagen de 80x80
    img = Image.new('RGB', (80, 80), 'white')
    draw = ImageDraw.Draw(img)
    
    # Crear patrón tipo QR básico
    size = 4
    for x in range(0, 80, size):
        for y in range(0, 80, size):
            # Patrón pseudo-aleatorio basado en posición
            if (x + y) % 12 < 6:
                draw.rectangle([x, y, x+size-1, y+size-1], fill='black')
    
    # Esquinas características del QR
    # Esquina superior izquierda
    draw.rectangle([0, 0, 20, 20], outline='black', width=2)
    draw.rectangle([4, 4, 16, 16], fill='black')
    draw.rectangle([8, 8, 12, 12], fill='white')
    
    # Esquina superior derecha
    draw.rectangle([60, 0, 80, 20], outline='black', width=2)
    draw.rectangle([64, 4, 76, 16], fill='black')
    draw.rectangle([68, 8, 72, 12], fill='white')
    
    # Esquina inferior izquierda
    draw.rectangle([0, 60, 20, 80], outline='black', width=2)
    draw.rectangle([4, 64, 16, 76], fill='black')
    draw.rectangle([8, 68, 12, 72], fill='white')
    
    img.save('assets/qr_realista.png')
    print("✅ QR realista creado")

def create_seal_stamp():
    """Crear un sello oficial"""
    img = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Círculo exterior
    draw.ellipse([5, 5, 95, 95], outline=(139, 0, 0, 200), width=3)
    # Círculo interior
    draw.ellipse([15, 15, 85, 85], outline=(139, 0, 0, 150), width=2)
    
    # Texto simulado (rectangulitos que parecen letras)
    # "OFICIAL"
    positions = [(25, 25), (35, 25), (45, 25), (55, 25), (65, 25), (75, 25)]
    for pos in positions:
        draw.rectangle([pos[0], pos[1], pos[0]+5, pos[1]+8], fill=(139, 0, 0, 180))
    
    # "2025"
    positions = [(30, 65), (40, 65), (50, 65), (60, 65)]
    for pos in positions:
        draw.rectangle([pos[0], pos[1], pos[0]+5, pos[1]+8], fill=(139, 0, 0, 180))
    
    # Centro
    draw.ellipse([40, 40, 60, 60], fill=(139, 0, 0, 100))
    
    img.save('assets/sello_oficial.png')
    print("✅ Sello oficial creado")

def create_watermark():
    """Crear una marca de agua"""
    img = Image.new('RGBA', (200, 50), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Texto tipo marca de agua
    try:
        # Intentar usar una fuente del sistema
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    draw.text((10, 10), "VERIFICADO", font=font, fill=(0, 128, 0, 120))
    
    img.save('assets/marca_agua.png')
    print("✅ Marca de agua creada")

if __name__ == "__main__":
    print("🎨 Creando assets realistas para el demo de TikTok...")
    
    # Asegurar que existe el directorio assets
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    create_realistic_signature()
    create_realistic_qr()
    create_seal_stamp()
    create_watermark()
    
    print("\n🎬 ¡Assets listos para el video de TikTok!")
    print("📁 Archivos creados:")
    print("   - rubrica_realista.png")
    print("   - qr_realista.png") 
    print("   - sello_oficial.png")
    print("   - marca_agua.png") 