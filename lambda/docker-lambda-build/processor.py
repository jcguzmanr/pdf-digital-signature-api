"""
PDF Processor Module
Maneja la inserción de texto e imágenes en PDFs usando PyMuPDF
"""

import fitz  # PyMuPDF
import os
import requests
import tempfile
from typing import List, Dict, Any, Union
from PIL import Image, ImageOps
import io
from urllib.parse import urlparse
import sys


class PDFProcessor:
    """Clase para procesar y modificar PDFs"""
    
    def __init__(self):
        self.doc = None
    
    def _is_url(self, path: str) -> bool:
        """
        Verifica si una ruta es una URL
        
        Args:
            path: Ruta a verificar
            
        Returns:
            bool: True si es una URL, False si es un archivo local
        """
        try:
            result = urlparse(path)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def _download_file(self, url: str, temp_dir: str = None) -> str:
        """
        Descarga un archivo desde una URL
        
        Args:
            url: URL del archivo a descargar
            temp_dir: Directorio temporal donde guardar el archivo
            
        Returns:
            str: Ruta del archivo descargado
        """
        if not temp_dir:
            temp_dir = tempfile.gettempdir()
            
        # Extraer nombre del archivo de la URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        # Si no hay nombre de archivo en la URL, generar uno
        if not filename or not filename.endswith('.pdf'):
            filename = f"downloaded_pdf_{os.getpid()}.pdf"
            
        temp_path = os.path.join(temp_dir, filename)
        
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            return temp_path
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error descargando archivo desde {url}: {str(e)}")
    
    def _download_image(self, url: str, temp_dir: str = None) -> str:
        """
        Descarga una imagen desde una URL
        
        Args:
            url: URL de la imagen a descargar
            temp_dir: Directorio temporal donde guardar el archivo
            
        Returns:
            str: Ruta del archivo descargado
        """
        if not temp_dir:
            temp_dir = tempfile.gettempdir()
            
        # Extraer nombre del archivo de la URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        # Si no hay nombre de archivo en la URL, generar uno
        if not filename or '.' not in filename:
            filename = f"downloaded_image_{os.getpid()}.png"
            
        temp_path = os.path.join(temp_dir, filename)
        
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            return temp_path
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error descargando imagen desde {url}: {str(e)}")
    
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
        
        # Manejar archivos remotos (URLs)
        temp_file = None
        actual_pdf_path = pdf_path
        
        if self._is_url(pdf_path):
            print(f"📥 Descargando PDF desde URL: {pdf_path}")
            try:
                actual_pdf_path = self._download_file(pdf_path)
                temp_file = actual_pdf_path
                print(f"✅ PDF descargado a: {actual_pdf_path}")
            except Exception as e:
                raise FileNotFoundError(f"No se pudo descargar el archivo desde {pdf_path}: {str(e)}")
        
        # Verificar que el archivo existe (local o descargado)
        if not os.path.exists(actual_pdf_path):
            raise FileNotFoundError(f"El archivo PDF no existe: {actual_pdf_path}")
        
        # Crear directorio de salida si no existe
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Abrir el PDF
        self.doc = fitz.open(actual_pdf_path)
        
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
            
            # Limpiar archivo temporal si se descargó
            if temp_file and os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                    print(f"🗑️ Archivo temporal eliminado: {temp_file}")
                except:
                    pass  # Ignorar errores al eliminar temporales
    
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
        
        # PyMuPDF usa el sistema de coordenadas PDF nativo (origen en esquina inferior izquierda)
        # Las coordenadas de entrada ya están en el sistema correcto
        x, y = position[0], position[1]
        
        # Crear punto de inserción con coordenadas directas
        point = fitz.Point(x, y)
        
        # APLICAR CORRECCIÓN:
        # PyMuPDF invierte el texto verticalmente de forma automática. Para contrarrestar esto,
        # aplicamos una matriz de transformación (morph) que realiza un flip vertical.
        # La matriz Matrix(1, -1) invierte el eje Y.
        # El punto de pivote para la transformación es el mismo punto de inserción.
        matrix = fitz.Matrix(1, -1)
        
        print(f"📍 Insertando texto en: ({x}, {y}) con flip vertical - Contenido: '{content}'")
        
        # Insertar texto
        page.insert_text(
            point,
            content,
            fontsize=font_size,
            color=color,
            fontname=font_name,
            morph=(point, matrix)  # Aplicar la corrección de volteo
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
        rotate = insertion.get("rotate", 0)  # Grados de rotación (horario) opcional
        flip = insertion.get("flip")  # "horizontal", "vertical" o "both"
        correct_orientation = insertion.get("correct_orientation", True)
        flip_type = insertion.get("flip_type", "horizontal")  # Tipo específico de transformación
        
        print(f"🔧 correct_orientation = {correct_orientation}")
        print(f"🔧 flip_type = {flip_type}")
        
        # Descargar imagen
        temp_file = None
        temp_file_path = source  # Inicializar con el source original
        
        try:
            if source.startswith(('http://', 'https://')):
                response = requests.get(source, timeout=30)
                response.raise_for_status()
                
                # Crear archivo temporal
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                
                # Si correct_orientation es False, aplicar flip vertical para corregir
                # la inversión automática que hace PyMuPDF
                if not correct_orientation:
                    print("🔄 Aplicando flip vertical para corregir inversión de PyMuPDF")
                    try:
                        from PIL import Image
                        import io
                        
                        # Cargar imagen con PIL
                        img = Image.open(io.BytesIO(response.content))
                        
                        # Aplicar flip vertical para corregir la inversión de PyMuPDF
                        img_flipped = img.transpose(Image.FLIP_TOP_BOTTOM)
                        
                        # Guardar imagen corregida
                        img_flipped.save(temp_file.name, format='PNG')
                        temp_file.close()
                        temp_file_path = temp_file.name
                        print("✅ Flip vertical aplicado para corregir PyMuPDF")
                        
                    except ImportError:
                        print("❌ PIL/Pillow no está instalado")
                        # Fallback: usar imagen original
                        temp_file.write(response.content)
                        temp_file.close()
                        temp_file_path = temp_file.name
                else:
                    # Guardar imagen original sin modificaciones
                    temp_file.write(response.content)
                    temp_file.close()
                    temp_file_path = temp_file.name
            
            else:
                # Es un archivo local
                temp_file_path = source
                
                # Si correct_orientation es False y es archivo local, también aplicar flip
                if not correct_orientation:
                    print("🔄 Aplicando flip horizontal a archivo local con PIL...")
                    try:
                        from PIL import Image
                        
                        # Crear archivo temporal para la imagen modificada
                        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                        
                        # Cargar, voltear y guardar
                        img = Image.open(source)
                        img = img.transpose(Image.FLIP_LEFT_RIGHT)
                        img.save(temp_file.name, format='PNG')
                        temp_file.close()
                        
                        temp_file_path = temp_file.name
                        print("✅ Flip horizontal aplicado a archivo local")
                        
                    except ImportError:
                        print("❌ PIL/Pillow no está instalado para archivo local")
                        temp_file_path = source
            
            # PyMuPDF usa el sistema de coordenadas PDF nativo (origen en esquina inferior izquierda)
            # Las coordenadas de entrada ya están en el sistema correcto
            x, y = position[0], position[1]
            print(f"📍 Insertando imagen en: ({x}, {y})")
            
            # Determinar dimensiones
            if width and height:
                # Usar dimensiones especificadas
                rect = fitz.Rect(x, y, x + width, y + height)
            else:
                # Usar dimensiones por defecto (100x100)
                rect = fitz.Rect(x, y, x + 100, y + 100)
            
            print(f"📐 Rectángulo de inserción: {rect}")
            
            # Insertar imagen
            page.insert_image(
                rect,
                filename=temp_file_path,
                rotate=rotate,
                keep_proportion=True,
                overlay=True
            )
            
            print(f"✅ Imagen insertada exitosamente")
            
        except Exception as e:
            print(f"❌ Error al insertar imagen: {str(e)}")
            raise
        finally:
            # Limpiar archivo temporal
            if temp_file and os.path.exists(temp_file.name):
                try:
                    os.unlink(temp_file.name)
                    print(f"🗑️ Archivo temporal eliminado: {temp_file.name}")
                except:
                    pass


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