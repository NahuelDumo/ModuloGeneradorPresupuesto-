def buscarPlantillaPresupuesto(record):
    # Diccionario con rutas por categoría y nombre del producto
    productoCategoria = {
        "Branding": {
            "Creación isologotipo": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaBranding/PlantillaCreacionDeIsologotipoBRANDING.html",
            "Diseño Manual de Estilo": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaBranding/PlantillaDiseñoManualDeEstiloBRANDING.html",
            "Rediseño Isologotipo": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaBranding/PlantillaRediseñoIsologotipoBRANDING.html"
        },
        "Desarrollo Web": {},
        "Editorial": {
            "Diseño gráfico de Boletín o News":"/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaEditorial/PlantillaDIseñoGraficoBoletin.html",
            "Diseño gráfico de Libro": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaEditorial/PlantillaDIseñoGraficoLibro.html",
            "Diseño gráfico de Revista": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaEditorial/PlantillaDIseñoGraficoRevista.html",
            "Diseño gráfico de pieza editorial especial": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaEditorial/PlantillaDIseñoGraficoRevista.html",
            "Impresión de Boletín o News": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaEditorial/PlantillaDiseñoImpresionBoletin.html",
            "Impresión de Libro": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaEditorial/PlantillaDiseñoImpresionLibro.html",
            "Impresión de Revista": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaEditorial/PlantillaDiseñoImpresionRevista.html",
            "Impresión de pieza editorial especial": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaEditorial/PlantillaDiseñoImpresionPiezaEditorial.html",
        },
        "Gestion I&C": {},
        "Grafica": {
            "Diseño gráfico de Bolsas o Cajas": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaGrafica/plantillaGrafica_G1_DGBolsas.html",
            "Diseño gráfico de Brochure": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaGrafica/plantillaGrafica_G1_DGBrochure.html",
            "Diseño gráfico de Carpetas o Carátulas Notariales": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaGrafica/plantillaGrafica_G1_DGCarpetas.html",
            "Diseño gráfico de Carteles o Banners": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaGrafica/plantillaGrafica_G1_DGBanners.html",  
            "Diseño gráfico de Certificados" : "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaGrafica/plantillaGrafica_G1_DGCertificados.html",
            "Diseño gráfico de Etiquetas" : "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaGrafica/plantillaGrafica_G1_DGEtiquetas.html",
            "Diseño gráfico de Flyer o Afiche": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaGrafica/plantillaGrafica_G1_DGFlyer.html",
            "Diseño gráfico de Folletos": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaGrafica/plantillaGrafica_G1_DGFolletos.html",
            "Diseño gráfico de Membretes o Formularios": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaGrafica/plantillaGrafica_G1_DGFormularios.html",
            "Diseño gráfico de Sobres" : "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaGrafica/plantillaGrafica_G1_DGSobres.html",
            "Diseño gráfico de Tarjetas" : "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaGrafica/plantillaGrafica_G1_DGTarjetas.html",
            "Diseño gráfico de pieza gráfica especial": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaGrafica/plantillaGrafica_G1_DGPiezaGEspecial.html",
            "Impresión de Bolsas o Cajas": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaGrafica/plantillaGrafica_G2_DGBolsas.html",
            "Impresión de Brochure": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaGrafica/plantillaGrafica_G2_DGBrochure.html",
            "Impresión de Carpetas o Carátulas Notariales": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaGrafica/plantillaGrafica_G2_DGCarpetas.html",
            "Impresión de Certificados": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaGrafica/plantillaGrafica_G2_DGCertificados.html",
            "Impresión de Etiquetas": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaGrafica/plantillaGrafica_G2_DGEtiquetas.html",
            "Impresión de Flyer o Afiche": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaGrafica/plantillaGrafica_G2_DGFlyer.html",
            "Impresión de Folletos": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaGrafica/plantillaGrafica_G2_DGFolletos.html",
            "Impresión de Membretes o Formularios"  : "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaGrafica/plantillaGrafica_G2_DGFormularios.html",
            "Impresión de Sobres": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaGrafica/plantillaGrafica_G2_DGSobres.html",
            "Impresión de Tarjetas": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaGrafica/plantillaGrafica_G2_DGTarjetas.html",
            "Impresión de pieza gráfica especial": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaGrafica/plantillaGrafica_G2_DGPiezaGEspecial.html"
        },
        "Marketing Digital": {},
        "Productos": {}
    }

    # Iterar sobre las líneas del pedido
    for line in record.order_line:
        if line.product_id and line.product_id.categ_id:
            etiqueta = line.product_id.categ_id.name
            producto_nombre = line.product_id.name
            rutas_categoria = productoCategoria.get(etiqueta, {})
            ruta_plantilla = rutas_categoria.get(producto_nombre)

            if ruta_plantilla:
                return ruta_plantilla  # Devuelve la primera que encuentra
        else:
            return "No se encontro nada"

    # Si no encuentra ninguna coincidencia
    return "/opt/odoo2/odoo/addons/GenerarPresupuesto/models/Plantillas/PlantillaDefault.html"

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

