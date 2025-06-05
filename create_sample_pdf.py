"""
Script para crear un PDF de ejemplo para testing
"""

import fitz  # PyMuPDF
import os

def create_sample_pdf():
    """Crear un PDF de ejemplo con múltiples páginas"""
    
    # Crear documento
    doc = fitz.open()
    
    # Página 1
    page1 = doc.new_page()
    page1.insert_text((50, 100), "DOCUMENTO DE PRUEBA", fontsize=20, color=(0, 0, 0))
    page1.insert_text((50, 150), "Página 1 de 3", fontsize=14, color=(0.5, 0.5, 0.5))
    page1.insert_text((50, 200), "Este es un documento de ejemplo para probar", fontsize=12)
    page1.insert_text((50, 220), "la funcionalidad de inserción de texto e imágenes.", fontsize=12)
    page1.insert_text((50, 260), "Lorem ipsum dolor sit amet, consectetur adipiscing elit.", fontsize=10)
    page1.insert_text((50, 280), "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", fontsize=10)
    
    # Página 2
    page2 = doc.new_page()
    page2.insert_text((50, 100), "PÁGINA 2", fontsize=18, color=(0, 0, 0))
    page2.insert_text((50, 150), "Contenido de la segunda página", fontsize=14)
    page2.insert_text((50, 200), "Ut enim ad minim veniam, quis nostrud exercitation", fontsize=12)
    page2.insert_text((50, 220), "ullamco laboris nisi ut aliquip ex ea commodo consequat.", fontsize=12)
    page2.insert_text((50, 260), "Duis aute irure dolor in reprehenderit in voluptate", fontsize=10)
    page2.insert_text((50, 280), "velit esse cillum dolore eu fugiat nulla pariatur.", fontsize=10)
    
    # Página 3
    page3 = doc.new_page()
    page3.insert_text((50, 100), "PÁGINA FINAL", fontsize=18, color=(0, 0, 0))
    page3.insert_text((50, 150), "Esta es la última página del documento", fontsize=14)
    page3.insert_text((50, 200), "Excepteur sint occaecat cupidatat non proident,", fontsize=12)
    page3.insert_text((50, 220), "sunt in culpa qui officia deserunt mollit anim id est laborum.", fontsize=12)
    page3.insert_text((50, 280), "Firma digital:", fontsize=10, color=(0.7, 0.7, 0.7))
    page3.insert_text((50, 300), "_________________________", fontsize=10, color=(0.7, 0.7, 0.7))
    
    # Guardar el PDF
    output_path = "input/documento.pdf"
    doc.save(output_path)
    doc.close()
    
    print(f"PDF de ejemplo creado: {output_path}")
    return output_path

if __name__ == "__main__":
    create_sample_pdf() 