#!/usr/bin/env python3
"""
HTML to PDF Converter - Renderizado Exacto
Convierte archivos HTML a PDF manteniendo el renderizado exacto del navegador

Uso:
    python html_to_pdf.py archivo.html salida.pdf
    
O importar las funciones:
    from html_to_pdf import convertir_html_a_pdf
    convertir_html_a_pdf('archivo.html', 'salida.pdf')
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import base64
import os
import time
import sys
import argparse

def convertir_html_a_pdf(archivo_html, archivo_pdf, configuracion=None):
    """
    Función principal - Convierte HTML a PDF con renderizado exacto
    
    Args:
        archivo_html (str): Ruta al archivo HTML
        archivo_pdf (str): Ruta donde guardar el PDF
        configuracion (dict): Configuración personalizada (opcional)
    
    Returns:
        bool: True si la conversión fue exitosa
    """
    
    # Configuración por defecto
    config_defecto = {
        'viewport': (1920, 1080),
        'tiempo_espera': 5,
        'pdf_formato': 'A4',
        'orientacion': 'horizontal',  # 'vertical' o 'horizontal'
        'margenes': 0,
        'escala': 1.0,
        'fondo': True
    }
    
    # Combinar configuración
    if configuracion:
        config_defecto.update(configuracion)
    
    config = config_defecto
    
    # Configurar opciones de Chrome
    chrome_options = Options()

    # Headless optimizado
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument(f'--window-size={config["viewport"][0]},{config["viewport"][1]}')

    # Renderizado exacto
    chrome_options.add_argument('--force-device-scale-factor=1')
    chrome_options.add_argument('--device-scale-factor=1')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-plugins')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument('--disable-features=VizDisplayCompositor')
    chrome_options.add_argument('--aggressive-cache-discard')
    chrome_options.add_argument('--disable-background-timer-throttling')
    chrome_options.add_argument('--disable-backgrounding-occluded-windows')
    chrome_options.add_argument('--disable-renderer-backgrounding')

    # Configuración de recursos
    prefs = {
        "profile.managed_default_content_settings.images": 1,
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_setting_values.media_stream": 2,
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Opciones del PDF
    pdf_options = {
        'format': config['pdf_formato'],
        'landscape': config['orientacion'] == 'horizontal',
        'printBackground': config['fondo'],
        'marginTop': config['margenes'],
        'marginBottom': config['margenes'],
        'marginLeft': config['margenes'],
        'marginRight': config['margenes'],
        'displayHeaderFooter': False,
        'preferCSSPageSize': True,
        'generateTaggedPDF': False,
        'generateDocumentOutline': False,
        'scale': config['escala']
    }

    driver = None
    try:
        print(f"🔄 Iniciando conversión de {archivo_html} a {archivo_pdf}")

        # Inicializar Chrome
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(config['viewport'][0], config['viewport'][1])

        # Cargar archivo HTML
        if os.path.isabs(archivo_html):
            url = f'file://{archivo_html}'
        else:
            url = f'file://{os.path.abspath(archivo_html)}'

        print(f"📄 Cargando: {url}")
        driver.get(url)

        # Esperar carga básica
        print("⏳ Esperando carga del DOM...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Esperar imágenes
        print("🖼️  Esperando carga de imágenes...")
        try:
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script(
                    """
                    const images = Array.from(document.images);
                    return images.length === 0 || images.every(img => img.complete && img.naturalHeight !== 0);
                    """
                )
            )
        except:
            print("⚠️  Timeout en imágenes, continuando...")

        # Esperar fuentes
        print("🔤 Esperando carga de fuentes...")
        try:
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.fonts.ready")
            )
        except:
            print("⚠️  Timeout en fuentes, continuando...")

        # Scroll para activar lazy loading
        print("📜 Activando lazy loading...")
        driver.execute_script("""
            return new Promise((resolve) => {
                let totalHeight = 0;
                const distance = 100;
                const timer = setInterval(() => {
                    const scrollHeight = document.body.scrollHeight;
                    window.scrollBy(0, distance);
                    totalHeight += distance;
                    
                    if(totalHeight >= scrollHeight) {
                        clearInterval(timer);
                        window.scrollTo(0, 0);
                        setTimeout(resolve, 500);
                    }
                }, 50);
            });
        """)

        # Espera adicional
        print(f"⏱️  Esperando {config['tiempo_espera']} segundos para renderizado completo...")
        time.sleep(config['tiempo_espera'])

        # Forzar repaint
        driver.execute_script("""
            document.body.style.display = 'none';
            document.body.offsetHeight;
            document.body.style.display = '';
        """)

        time.sleep(1)

        # Generar PDF
        print("📋 Generando PDF...")
        pdf_data = driver.execute_cdp_cmd('Page.printToPDF', pdf_options)

        # Guardar archivo
        with open(archivo_pdf, 'wb') as f:
            f.write(base64.b64decode(pdf_data['data']))

        print(f"✅ PDF guardado exitosamente: {archivo_pdf}")
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    finally:
        if driver:
            driver.quit()

def convertir_html_string_a_pdf(html_string, archivo_pdf, configuracion=None):
    """
    Convierte un string HTML a PDF

    Args:
        html_string (str): Código HTML como string
        archivo_pdf (str): Ruta donde guardar el PDF
        configuracion (dict): Configuración personalizada (opcional)

    Returns:
        bool: True si la conversión fue exitosa
    """

    # Crear archivo temporal
    temp_file = 'temp_conversion.html'

    # Asegurar estructura HTML completa
    if not html_string.strip().startswith('<!DOCTYPE'):
        html_string = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
{html_string}
</body>
</html>"""

    try:
        # Escribir archivo temporal
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(html_string)

        # Convertir usando la función principal
        resultado = convertir_html_a_pdf(temp_file, archivo_pdf, configuracion)
        return resultado

    finally:
        # Limpiar archivo temporal
        if os.path.exists(temp_file):
            os.remove(temp_file)

def main():
    """Función principal para uso desde línea de comandos"""

    parser = argparse.ArgumentParser(description='Convierte HTML a PDF con renderizado exacto')
    parser.add_argument('html', help='Archivo HTML de entrada')
    parser.add_argument('pdf', help='Archivo PDF de salida')
    parser.add_argument('--viewport', default='1920x1080', help='Tamaño del viewport (ej: 1920x1080)')
    parser.add_argument('--wait', type=int, default=5, help='Tiempo de espera en segundos')
    parser.add_argument('--format', default='A4', help='Formato del PDF (A4, A3, Letter, etc.)')
    parser.add_argument('--landscape', action='store_true', help='Orientación horizontal')
    parser.add_argument('--margin', type=float, default=0, help='Márgenes en pulgadas')
    parser.add_argument('--scale', type=float, default=1.0, help='Escala del contenido')

    args = parser.parse_args()

    # Parsear viewport
    try:
        width, height = map(int, args.viewport.split('x'))
        viewport = (width, height)
    except:
        print("❌ Formato de viewport inválido. Use: 1920x1080")
        sys.exit(1)

    # Configuración desde argumentos
    configuracion = {
        'viewport': viewport,
        'tiempo_espera': args.wait,
        'pdf_formato': args.format,
        'orientacion': 'horizontal' if args.landscape else 'vertical',
        'margenes': args.margin,
        'escala': args.scale,
        'fondo': True
    }

    # Verificar que existe el archivo HTML
    if not os.path.exists(args.html):
        print(f"❌ No se encontró el archivo: {args.html}")
        sys.exit(1)

    # Realizar conversión
    exito = convertir_html_a_pdf(args.html, args.pdf, configuracion)

    if exito:
        print("🎉 ¡Conversión completada exitosamente!")
        sys.exit(0)
    else:
        print("💥 La conversión falló")
        sys.exit(1)

# Ejemplos de uso programático
def ejemplos():
    """Ejemplos de cómo usar las funciones"""

    # Ejemplo 1: Conversión básica
    convertir_html_a_pdf('mi_archivo.html', 'salida.pdf')

    # Ejemplo 2: Con configuración personalizada
    config_personalizada = {
        'viewport': (1366, 768),
        'tiempo_espera': 8,
        'pdf_formato': 'A3',
        'orientacion': 'horizontal',
        'margenes': 0.5,
        'escala': 0.8
    }

    convertir_html_a_pdf('mi_archivo.html', 'salida_custom.pdf', config_personalizada)

    # Ejemplo 3: Desde string HTML
    html_code = """
    <h1>Mi Documento</h1>
    <p>Este es un ejemplo de conversión desde string HTML</p>
    <style>
        body { font-family: Arial; padding: 20px; }
        h1 { color: blue; }
    </style>
    """

    convertir_html_string_a_pdf(html_code, 'desde_string.pdf')

if __name__ == "__main__":
    # Si no hay argumentos, mostrar ejemplo de uso
    if len(sys.argv) == 1:
        print("🚀 HTML to PDF Converter")
        print("\n📋 Uso desde línea de comandos:")
        print("python Borrar.py archivo.html salida.pdf")
        print("\n📋 Ejemplo:")
        print("python Borrar.py S00003_presupuesto.html S00003_presupuesto.pdf")
        print("\n📋 Con opciones:")
        print("python Borrar.py S00003_presupuesto.html output.pdf --landscape --wait 8")
        print("\n📋 Uso programático:")
        print("Descomenta las líneas al final del archivo para usar directamente\n")

        # EJEMPLO DIRECTO - Configuración en landscape como tu código original
        print("🔄 Ejecutando conversión de ejemplo en landscape...")

        config_landscape = {
            'orientacion': 'horizontal',  # landscape: True
            'pdf_formato': 'A4',
            'margenes': 0,
            'escala': 1.0,
            'tiempo_espera': 5,
            'fondo': True
        }

        try:
            resultado = convertir_html_a_pdf('S00003_presupuesto.html', 'S00003_presupuesto.pdf', config_landscape)
            if resultado:
                print("✅ ¡Conversión completada en formato landscape!")
            else:
                print("❌ Error en la conversión")
        except Exception as e:
            print(f"❌ Error: {e}")
            print("💡 Asegúrate de que el archivo S00003_presupuesto.html existe")
    else:
        main()
