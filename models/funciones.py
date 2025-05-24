def buscarPlantillaPresupuesto(record):
    # Diccionario con rutas por categoría y nombre del producto
    productoCategoria = {
        "Branding": {
            "Creación isologotipo": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaBranding/PlantillaCreacionDeIsologotipo.html",
            "Diseño Manual de Estilo": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaBranding/PlantillaDiseñoManualDeEstilo.html",
            "Rediseño Isologotipo": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaBranding/PlantillaRediseñoIsologotipo.html"
        },
        "Desarrollo Web": {},
        "Editorial": {
            "Diseño gráfico de Boletín o News":"/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaEditorial/PlantillaDiseñoGraficoBoletin.html",
            "Diseño gráfico de Libro": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaEditorial/PlantillaDiseñoGraficoLibro.html",
            "Diseño gráfico de Revista": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaEditorial/PlantillaDiseñoGraficoPiezaEditorialEspecial.html",
            "Diseño gráfico de pieza editorial especial": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaEditorial/PlantillaDiseñoGraficoRevista.html",
            "Impresión de Boletín o News": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaEditorial/PlantillaDiseñoImpresionBoletin.html",
            "Impresión de Libro": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaEditorial/PlantillaDiseñoImpresionLibro.html",
            "Impresión de Revista": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaEditorial/PlantillaDiseñoImpresionRevista.html",
            "Impresión de pieza editorial especial": "/opt/odoo2/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaEditorial/PlantillaDiseñoImpresionPiezaEditorial.html",
        },
        "Gestion I&C": {},
        "Grafica": {},
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
    # Separar la cadena en palabras
    palabras = nombre.split(" ")
    
    # Reemplazar el ultimo por un \n + el mismo
    ultima = palabras[-1]
    palabras[-1] =  "<br>" + ultima   
    # Unir las palabras nuevamente
    nombre_reformado = " ".join(palabras)
    
    return nombre_reformado
