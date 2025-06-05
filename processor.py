"""
PDF Processor Module
Maneja la inserción de texto e imágenes en PDFs usando PyMuPDF
"""

import fitz  # PyMuPDF
import os
from typing import List, Dict, Any, Union
from PIL import Image
import io


class PDFProcessor:
    """Clase para procesar y modificar PDFs"""
    
    def __init__(self):
        self.doc = None
    
    def process_pdf(self, pdf_data: Dict[str, Any]) -> str:
        """
        Procesa un PDF según las instrucciones proporcionadas
        
        Args:
            pdf_data: Diccionario con las instrucciones de procesamiento
            
        Returns:
            str: Ruta del archivo de salida procesado
        """
        pdf_path = pdf_data.get("pdf_path")
        output_path = pdf_data.get("output_path")
        insertions = pdf_data.get("insertions", [])
        
        if not pdf_path or not output_path:
            raise ValueError("pdf_path y output_path son requeridos")
        
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"El archivo PDF no existe: {pdf_path}")
        
        # Crear directorio de salida si no existe
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Abrir el PDF
        self.doc = fitz.open(pdf_path)
        
        try:
            # Aplicar cada inserción
            for insertion in insertions:
                self._apply_insertion(insertion)
            
            # Guardar el PDF modificado
            self.doc.save(output_path)
            return output_path
            
        except Exception as e:
            raise Exception(f"Error procesando PDF: {str(e)}")
        
        finally:
            if self.doc:
                self.doc.close()
    
    def _apply_insertion(self, insertion: Dict[str, Any]):
        """
        Aplica una inserción específica al PDF
        
        Args:
            insertion: Diccionario con los datos de la inserción
        """
        insertion_type = insertion.get("type")
        pages = insertion.get("pages")
        position = insertion.get("position", [0, 0])
        
        if insertion_type not in ["text", "image"]:
            raise ValueError(f"Tipo de inserción no válido: {insertion_type}")
        
        target_pages = self._get_target_pages(pages)
        
        for page_num in target_pages:
            if 0 <= page_num < len(self.doc):
                page = self.doc[page_num]
                
                if insertion_type == "text":
                    self._insert_text(page, insertion, position)
                elif insertion_type == "image":
                    self._insert_image(page, insertion, position)
    
    def _get_target_pages(self, pages: Union[str, int, List[int]]) -> List[int]:
        """
        Determina qué páginas deben ser modificadas
        
        Args:
            pages: Especificación de páginas ("all", "first", "last", número, o lista)
            
        Returns:
            List[int]: Lista de números de página (0-indexados)
        """
        total_pages = len(self.doc)
        
        if pages == "all":
            return list(range(total_pages))
        elif pages == "first":
            return [0] if total_pages > 0 else []
        elif pages == "last":
            return [total_pages - 1] if total_pages > 0 else []
        elif isinstance(pages, int):
            # Convertir de 1-indexado a 0-indexado
            page_index = pages - 1
            return [page_index] if 0 <= page_index < total_pages else []
        elif isinstance(pages, list):
            # Convertir lista de 1-indexados a 0-indexados
            return [p - 1 for p in pages if isinstance(p, int) and 1 <= p <= total_pages]
        else:
            return []
    
    def _insert_text(self, page: fitz.Page, insertion: Dict[str, Any], position: List[int]):
        """
        Inserta texto en una página
        
        Args:
            page: Página de PyMuPDF
            insertion: Datos de la inserción de texto
            position: Posición [x, y] donde insertar
        """
        content = insertion.get("content", "")
        font_size = insertion.get("font_size", 12)
        color = insertion.get("color", [0, 0, 0])  # Negro por defecto
        font_name = insertion.get("font_name", "helv")  # Helvetica por defecto
        
        # Crear punto de inserción
        point = fitz.Point(position[0], position[1])
        
        # Insertar texto
        page.insert_text(
            point,
            content,
            fontsize=font_size,
            color=color,
            fontname=font_name
        )
    
    def _insert_image(self, page: fitz.Page, insertion: Dict[str, Any], position: List[int]):
        """
        Inserta una imagen en una página
        
        Args:
            page: Página de PyMuPDF
            insertion: Datos de la inserción de imagen
            position: Posición [x, y] donde insertar
        """
        source = insertion.get("source")
        width = insertion.get("width")
        height = insertion.get("height")
        
        if not source:
            raise ValueError("source es requerido para inserción de imagen")
        
        if not os.path.exists(source):
            raise FileNotFoundError(f"Archivo de imagen no encontrado: {source}")
        
        # Abrir imagen para obtener dimensiones originales
        with Image.open(source) as img:
            original_width, original_height = img.size
        
        # Si no se especifican dimensiones, usar las originales pero escaladas apropiadamente
        if not width and not height:
            # Escalar a un tamaño razonable (máximo 200px de ancho)
            scale_factor = min(200 / original_width, 200 / original_height, 1.0)
            width = int(original_width * scale_factor)
            height = int(original_height * scale_factor)
        elif width and not height:
            # Mantener proporción basada en el ancho
            height = int(original_height * (width / original_width))
        elif height and not width:
            # Mantener proporción basada en la altura
            width = int(original_width * (height / original_height))
        
        # Crear rectángulo para la imagen
        rect = fitz.Rect(
            position[0], 
            position[1], 
            position[0] + width, 
            position[1] + height
        )
        
        # Insertar imagen
        page.insert_image(rect, filename=source)


def create_sample_assets():
    """
    Crea imágenes de ejemplo para testing
    """
    assets_dir = "assets"
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    
    # Crear una imagen simple de rúbrica (rectángulo azul)
    rubrica_img = Image.new('RGB', (100, 50), color='blue')
    rubrica_img.save(os.path.join(assets_dir, 'rubrica.png'))
    
    # Crear una imagen simple de QR (rectángulo verde)
    qr_img = Image.new('RGB', (80, 80), color='green')
    qr_img.save(os.path.join(assets_dir, 'qr.png'))
    
    print("Imágenes de ejemplo creadas en assets/")


if __name__ == "__main__":
    # Crear imágenes de ejemplo
    create_sample_assets() 