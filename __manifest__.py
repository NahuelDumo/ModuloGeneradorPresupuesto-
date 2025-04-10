{
    'name': 'Generar Presupuesto PDF',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Genera un presupuesto en PDF a partir de una cotización',
    'author': 'Tu Nombre o Empresa',
    'depends': ['sale'],
    'data': [
        'views/sale_order_views.xml',
        'views/Hoja_Cotizaciones_Veo_para_Odoo_modificado3.xml',  # Agregamos tu plantilla
        'data/actions.xml',  # Asegúrate de añadir tu archivo aquí
     ],

    'installable': True,
    'application': False,
}
