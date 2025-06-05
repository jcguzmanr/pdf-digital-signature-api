#!/usr/bin/env python3
"""
🎬 DEMO COMPLETO PARA TIKTOK
Script que demuestra todo el proceso de firma digital paso a paso
"""

import requests
import json
import time
import os
from datetime import datetime

def print_banner(text):
    """Imprimir banner colorido"""
    print(f"\n{'='*60}")
    print(f"🎬 {text}")
    print(f"{'='*60}")

def print_step(step, description):
    """Imprimir paso del proceso"""
    print(f"\n📍 PASO {step}: {description}")
    print("-" * 40)

def show_files_status():
    """Mostrar estado de archivos"""
    try:
        response = requests.get("http://localhost:8000/list-files")
        if response.status_code == 200:
            files = response.json()
            print("📁 ARCHIVOS DISPONIBLES:")
            print(f"   📄 INPUT: {files['input']}")
            print(f"   ✅ OUTPUT: {files['output']}")
            print(f"   🖼️  ASSETS: {files['assets']}")
        else:
            print("❌ Error obteniendo lista de archivos")
    except Exception as e:
        print(f"❌ Error: {e}")

def process_pdf(test_file, demo_name):
    """Procesar PDF con archivo de test específico"""
    print(f"🚀 Procesando: {demo_name}")
    
    try:
        # Leer archivo de test
        with open(test_file, 'r') as f:
            test_data = json.load(f)
        
        print(f"📋 Configuración cargada:")
        print(f"   📄 PDF: {test_data['pdf_path']}")
        print(f"   📤 Salida: {test_data['output_path']}")
        print(f"   🎯 Inserciones: {len(test_data['insertions'])}")
        
        # Enviar petición
        response = requests.post(
            "http://localhost:8000/process-pdf",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result['message']}")
            print(f"📁 Archivo generado: {result['output_path']}")
            print(f"⏰ Procesado en: {result['processed_at']}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📝 Detalle: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error procesando PDF: {e}")
        return False

def check_server():
    """Verificar que el servidor esté funcionando"""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            health = response.json()
            print("✅ Servidor funcionando correctamente")
            print(f"🕐 Timestamp: {health['timestamp']}")
            print(f"📁 Directorios: {health['directories']}")
            return True
        else:
            print("❌ Servidor no responde correctamente")
            return False
    except Exception as e:
        print(f"❌ No se puede conectar al servidor: {e}")
        return False

def main():
    """Función principal del demo"""
    print_banner("DEMO COMPLETO PARA TIKTOK - FIRMA DIGITAL PDF")
    
    print("🎯 Este demo mostrará:")
    print("   1️⃣ Verificación del sistema")
    print("   2️⃣ Procesamiento básico")
    print("   3️⃣ Procesamiento completo") 
    print("   4️⃣ Procesamiento para TikTok")
    print("   5️⃣ Resultados finales")
    
    # PASO 1: Verificar servidor
    print_step(1, "VERIFICACIÓN DEL SISTEMA")
    if not check_server():
        print("❌ El servidor no está funcionando. Ejecuta primero:")
        print("   python3 main.py")
        return
    
    # PASO 2: Mostrar archivos iniciales
    print_step(2, "ESTADO INICIAL DE ARCHIVOS")
    show_files_status()
    
    # PASO 3: Procesamiento básico
    print_step(3, "PROCESAMIENTO BÁSICO")
    time.sleep(1)
    success1 = process_pdf("test.json", "Firma Digital Básica")
    
    # PASO 4: Procesamiento completo
    print_step(4, "PROCESAMIENTO COMPLETO CON MÚLTIPLES ELEMENTOS")
    time.sleep(1)
    success2 = process_pdf("test_completo.json", "Firma Digital Completa")
    
    # PASO 5: Procesamiento para TikTok
    print_step(5, "PROCESAMIENTO ESPECIAL PARA TIKTOK 🎬")
    time.sleep(1)
    success3 = process_pdf("test_tiktok.json", "Demo TikTok con Assets Realistas")
    
    # PASO 6: Resultados finales
    print_step(6, "RESULTADOS FINALES")
    show_files_status()
    
    # Resumen
    print_banner("RESUMEN DEL DEMO")
    print(f"✅ Procesamiento básico: {'✓' if success1 else '✗'}")
    print(f"✅ Procesamiento completo: {'✓' if success2 else '✗'}")
    print(f"✅ Demo TikTok: {'✓' if success3 else '✗'}")
    
    if all([success1, success2, success3]):
        print("\n🎉 ¡DEMO COMPLETADO EXITOSAMENTE! 🎉")
        print("\n📱 Para el video de TikTok, muestra:")
        print("   🎬 El PDF original vs los PDFs firmados")
        print("   🔍 Los diferentes elementos agregados")
        print("   ⚡ La velocidad del procesamiento")
        print("   📋 La API funcionando en tiempo real")
        print("\n📁 Archivos generados disponibles en: ./output/")
    else:
        print("\n❌ Algunos procesos fallaron. Revisa los errores arriba.")
    
    print_banner("¡LISTO PARA TIKTOK! 🎬✨")

if __name__ == "__main__":
    main() 