
def buscarPlantillaPresupuesto(record):
    # Defino un diccionario para guardar todas las direcciones por categoria
    productoCategoria = {
        "Branding": {
            "Creacion Isologotipo": "/opt/odoo2/odoo/addons/GenerarPresupuesto/models/Plantillas/Branding/PlantillaCreacionIsologotipo.html",
            "Diseño Manual De Estilo": "/opt/odoo2/odoo/addons/GenerarPresupuesto/models/Plantillas/Branding/PlantillaDisenoManualDeEstilo.html",
            "Rediseño Isologotipo": "/opt/odoo2/odoo/addons/GenerarPresupuesto/models/Plantillas/Branding/PlantillaRediseñoIsologotipo.html"
        },
        "Desarrollo Web": {},
        "Editorial": {},
        "Gestion I&C": {},
        "Grafica": {},
        "Marketing Digital": {},
        "Productos": {}
    }

    # Obtener la etiqueta asociada al producto
    etiqueta = record.product_id.categ_id.name
    producto_nombre = record.product_id.name

    # Obtener las rutas si la categoría existe, y si el producto está definido
    rutas_categoria = productoCategoria.get(etiqueta, {})
    ruta_plantilla = rutas_categoria.get(producto_nombre)

    return ruta_plantilla


    