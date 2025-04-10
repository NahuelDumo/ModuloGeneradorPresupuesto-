def buscarPlantillaPresupuesto(record):
    # Diccionario con rutas por categoría y nombre del producto
    productoCategoria = {
        "Branding": {
            "Creación isologotipo": "/opt/odoo2/odoo/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaBranding/PlantillaCreacionIsologotipo.html",
            "Diseño Manual de Estilo": "/opt/odoo2/odoo/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaBranding/PlantillaDisenoManualDeEstilo.html",
            "Rediseño Isologotipo": "/opt/odoo2/odoo/odoo-custom-addons/ModuloGeneradorPresupuesto-/Plantillas/PlantillaBranding/PlantillaRediseñoIsologotipo.html"
        },
        "Desarrollo Web": {},
        "Editorial": {},
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
