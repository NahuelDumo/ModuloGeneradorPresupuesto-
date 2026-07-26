import re

def buscarPlantillaPresupuesto(record):
    base_dir = "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas"
    default_path = f"{base_dir}/PlantillaDesarrolloWeb/Plantilla-Desarrollo-Web.html"

    # Diccionario con rutas por categoría y nombre del producto
    productoCategoria = {
        "Branding": {
            "Creación isologotipo": f"{base_dir}/PlantillaBranding/PlantillaCreacionDeIsologotipoBRANDING.html",
            "Diseño Manual de Estilo": f"{base_dir}/PlantillaBranding/PlantillaDiseñoManualDeEstiloBRANDING.html",
            "Rediseño Isologotipo": f"{base_dir}/PlantillaBranding/PlantillaRediseñoDeIsologotipoBRANDING.html"
        },
        "Desarrollo Web": {
            "Creación de Sitio Web Basico": f"{base_dir}/PlantillaDesarrolloWeb/Plantilla-Desarrollo-Web.html",
            "Actualización Sitio Web": f"{base_dir}/PlantillaDesarrolloWeb/Plantilla-Actualizacion-de-Sitio-Web.html",
            "Creación de sitio web especial": f"{base_dir}/PlantillaDesarrolloWeb/Plantilla-Desarrollo-Web-Especial.html",
            "Creación de tienda on-line": f"{base_dir}/PlantillaDesarrolloWeb/Plantilla-Desarrollo-Web-Especial.html",
            "Servicio de Hosting": f"{base_dir}/PlantillaDesarrolloWeb/Plantilla-Hosting.html",
            "Espacio de Hosting": f"{base_dir}/PlantillaDesarrolloWeb/Plantilla-Hosting.html",
            "Hosting": f"{base_dir}/PlantillaDesarrolloWeb/Plantilla-Hosting.html",
            "Creación de Landing Page": f"{base_dir}/PlantillaDesarrolloWeb/Plantilla-Creación-Landing-Page.html",
            "Creación de Landing page": f"{base_dir}/PlantillaDesarrolloWeb/Plantilla-Creación-Landing-Page.html",
            "Landing Page": f"{base_dir}/PlantillaDesarrolloWeb/Plantilla-Creación-Landing-Page.html",
        },
        "Editorial": {
            "Diseño gráfico de Boletín o News": f"{base_dir}/PlantillaEditorial/PlantillaDIseñoGraficoBoletin.html",
            "Diseño gráfico de Libro": f"{base_dir}/PlantillaEditorial/PlantillaDIseñoGraficoLibro.html",
            "Diseño gráfico de Revista": f"{base_dir}/PlantillaEditorial/PlantillaDIseñoGraficoRevista.html",
            "Diseño gráfico de pieza editorial especial": f"{base_dir}/PlantillaEditorial/PlantillaDIseñoGraficoRevista.html",
            "Impresión de Boletín o News": f"{base_dir}/PlantillaEditorial/PlantillaDiseñoImpresionBoletin.html",
            "Impresión de Libro": f"{base_dir}/PlantillaEditorial/PlantillaDiseñoImpresionLibro.html",
            "Impresión de Revista": f"{base_dir}/PlantillaEditorial/PlantillaDiseñoImpresionRevista.html",
            "Impresión de pieza editorial especial": f"{base_dir}/PlantillaEditorial/PlantillaDiseñoImpresionPiezaEditorial.html",
        },
        "Grafica": {
            "Diseño gráfico de Bolsas o Cajas": f"{base_dir}/PlantillaGrafica/plantillaGrafica_G1_DGBolsas.html",
            "Diseño gráfico de Brochure": f"{base_dir}/PlantillaGrafica/plantillaGrafica_G1_DGBrochure.html",
            "Diseño gráfico de Carpetas o Carátulas Notariales": f"{base_dir}/PlantillaGrafica/plantillaGrafica_G1_DGCarpetas.html",
            "Diseño gráfico de Carteles o Banners": f"{base_dir}/PlantillaGrafica/plantillaGrafica_G1_DGBanners.html",  
            "Diseño gráfico de Certificados": f"{base_dir}/PlantillaGrafica/plantillaGrafica_G1_DGCertificados.html",
            "Diseño gráfico de Etiquetas": f"{base_dir}/PlantillaGrafica/plantillaGrafica_G1_DGEtiquetas.html",
            "Diseño gráfico de Flyer o Afiche": f"{base_dir}/PlantillaGrafica/plantillaGrafica_G1_DGFlyer.html",
            "Diseño gráfico de Folletos": f"{base_dir}/PlantillaGrafica/plantillaGrafica_G1_DGFolletos.html",
            "Diseño gráfico de Membretes o Formularios": f"{base_dir}/PlantillaGrafica/plantillaGrafica_G1_DGFormularios.html",
            "Diseño gráfico de Sobres": f"{base_dir}/PlantillaGrafica/plantillaGrafica_G1_DGSobres.html",
            "Diseño gráfico de Tarjetas": f"{base_dir}/PlantillaGrafica/plantillaGrafica_G1_DGTarjetas.html",
            "Diseño gráfico de pieza gráfica especial": f"{base_dir}/PlantillaGrafica/plantillaGrafica_G1_DGPiezaGEspecial.html",
            "Impresión de Bolsas o Cajas": f"{base_dir}/PlantillaGrafica/plantillaGrafica_G2_DGBolsas.html",
            "Impresión de Brochure": f"{base_dir}/PlantillaGrafica/plantillaGrafica_G2_DGBrochure.html",
            "Impresión de Carpetas o Carátulas Notariales": f"{base_dir}/PlantillaGrafica/plantillaGrafica_G2_DGCarpetas.html",
            "Impresión de Certificados": f"{base_dir}/PlantillaGrafica/plantillaGrafica_G2_DGCertificados.html",
            "Impresión de Etiquetas": f"{base_dir}/PlantillaGrafica/plantillaGrafica_G2_DGEtiquetas.html",
            "Impresión de Flyer o Afiche": f"{base_dir}/PlantillaGrafica/plantillaGrafica_G2_DGFlyer.html",
            "Impresión de Folletos": f"{base_dir}/PlantillaGrafica/plantillaGrafica_G2_DGFolletos.html",
            "Impresión de Membretes o Formularios": f"{base_dir}/PlantillaGrafica/plantillaGrafica_G2_DGFormularios.html",
            "Impresión de Sobres": f"{base_dir}/PlantillaGrafica/plantillaGrafica_G2_DGSobres.html",
            "Impresión de Tarjetas": f"{base_dir}/PlantillaGrafica/plantillaGrafica_G2_DGTarjetas.html",
            "Impresión de pieza gráfica especial": f"{base_dir}/PlantillaGrafica/plantillaGrafica_G2_DGPiezaGEspecial.html"
        }
    }

    # Iterar sobre las líneas del pedido
    for line in record.order_line:
        if line.product_id:
            producto_nombre = line.product_id.name or ""
            etiqueta = line.product_id.categ_id.name if line.product_id.categ_id else ""

            # Coincidencia exacta
            rutas_categoria = productoCategoria.get(etiqueta, {})
            ruta_plantilla = rutas_categoria.get(producto_nombre)
            if ruta_plantilla:
                return ruta_plantilla

            # Coincidencia insensible a mayúsculas/minúsculas
            for cat, prods in productoCategoria.items():
                if cat.lower() in etiqueta.lower() or etiqueta.lower() in cat.lower():
                    for p_name, p_route in prods.items():
                        if p_name.lower() == producto_nombre.lower():
                            return p_route

            # Fallback por palabras clave en el nombre del producto
            prod_lower = producto_nombre.lower()
            if "hosting" in prod_lower:
                return f"{base_dir}/PlantillaDesarrolloWeb/Plantilla-Hosting.html"
            if "landing" in prod_lower:
                return f"{base_dir}/PlantillaDesarrolloWeb/Plantilla-Creación-Landing-Page.html"
            if "actualizaci" in prod_lower:
                return f"{base_dir}/PlantillaDesarrolloWeb/Plantilla-Actualizacion-de-Sitio-Web.html"
            if "especial" in prod_lower or "tienda" in prod_lower or "on-line" in prod_lower:
                return f"{base_dir}/PlantillaDesarrolloWeb/Plantilla-Desarrollo-Web-Especial.html"
            
            # Fallback por categoría
            if "web" in etiqueta.lower():
                return default_path

    # Si no encuentra ninguna coincidencia
    return default_path

def dividir_en_oraciones(texto, max_len):
        oraciones_finales = []
        texto = texto.strip()
        
        while len(texto) > 0:
            if len(texto) <= max_len:
                oraciones_finales.append(texto.strip())
                break

            corte = texto.rfind(" ", 0, max_len + 1)
            if corte == -1:
                corte = max_len  # Si no hay espacios, cortar exactamente en 118
            oracion = texto[:corte].strip()
            oraciones_finales.append(oracion)
            texto = texto[corte:].strip()

        return oraciones_finales

def cadena_reformada(nombre):
    # Separar en palabras
    palabras = nombre.split()

    # Calcular índice del medio
    mitad = (len(palabras) // 2)+1

    # Insertar <br> en el medio
    palabras.insert(mitad, "<br>")

    # Unir las partes sin agregar espacio alrededor del <br>
    resultado = ""
    for i, palabra in enumerate(palabras):
        if palabra == "<br>":
            resultado += palabra  # sin espacio
        elif i > 0 and palabras[i - 1] != "<br>":
            resultado += " " + palabra
        else:
            resultado += palabra

    return resultado

def dividir_en_items(texto, max_len_total=33, cantidad_items=6):
    items = ["" *cantidad_items]
    
    # Dividir en oraciones usando punto como separador
    texto = texto.strip().split(".")
    oraciones = [o.strip() + "." for o in texto if o.strip()]
    itemIndice = 0 
    for oracion in oraciones[:cantidad_items]:
        
        # Rellenar con espacios si es más corta, o cortar si es más larga
        item = verificarEspacios(oracion, max_len_total)
        items.insert(itemIndice, item)
        itemIndice += 1
    
    return items

def verificarEspacios(oracion, max_len_total):

    if len(oracion) < max_len_total:
        # Rellenar con espacios
        espacios_faltantes = max_len_total - len(oracion)
        oracion += " " * espacios_faltantes
    elif len(oracion) > max_len_total:
        # Cortar la oración
        oracion = oracion[:max_len_total]
    
    return oracion

def formatear_item(item):
    return f"<span style='font-family: Roboto, sans-serif; word-spacing: 0px; display:inline-block; width: 680px;'> • {item}</span>" if item else ""


def obtener_cantidad_idiomas(idiomas_str):
    if not idiomas_str:
        return 0
    text = str(idiomas_str).strip()
    if not text:
        return 0
    cleaned = re.sub(r'\b(y|e|and)\b', ',', text, flags=re.IGNORECASE)
    cleaned = re.sub(r'[/;&\-]', ',', cleaned)
    parts = [p.strip() for p in cleaned.split(',') if p.strip()]
    return len(parts)


