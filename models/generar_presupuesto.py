import asyncio
from odoo import models, fields
from fpdf import FPDF
from PIL import Image
import base64
import os
from io import BytesIO
from odoo.exceptions import UserError
from playwright.async_api import async_playwright
from .funciones import *



class SaleOrder(models.Model):
    _inherit = "sale.order"

    payment_method = fields.Char(
        string="Forma de pago",
        required=True,
        help="Especifica la forma de pago para este presupuesto.",
    )
    text_pagina1 = fields.Char(
        string="Texto editable pagina 1",
        required=True,
        size=164,
        help="Especifica el texto de la pagina 1 ESPECIFICACIONES TECNICAS.",
    )
    text_pagina2 = fields.Char(
        string="Texto editable pagina 2",
        required=True,
        size=354,
        help="Especifica el texto de la pagina 2.",
    )
    async def cargarNavegador(modified_html_path, output_pdf_path):
        async with async_playwright() as p:
            browser = await p.firefox.launch(args=['--no-sandbox', '--disable-setuid-sandbox'])
            page = await browser.new_page()
            await page.goto(f"file:///{modified_html_path}", timeout=600000)
            print("Página cargada con éxito. Generando PDF...")
            
            await page.pdf(
                path=output_pdf_path,
                format="A4",
                landscape=True,
                margin={"top": "2cm", "bottom": "2cm", "left": "2cm", "right": "2cm"},
                display_header_footer=False,
            )
            
            print("PDF generado con éxito.")
            await browser.close()

    def generar_presupuesto_pdf(self):
        for record in self:
            if not record.partner_id or not record.order_line:
                raise ValueError("La orden de venta no tiene cliente o líneas de productos.")

            # Datos necesarios para el PDF
            nombre_cliente = record.partner_id.name or "-"
            contacto = record.partner_id.parent_id.name or "-"
            numero_cotizacion = record.name
            forma_pago = record.payment_method
            nombre_servicio = record.order_line[0].product_id.name or "No disponible"
            descripcion_servicio = record.order_line[0].name or "No disponible"
            precio = record.order_line[0].price_unit
            plazo_validez = record.validity_date or "No disponible"
            plazo_pago = record.payment_term_id.name if record.payment_term_id else "No disponible"
            condiciones_generales = (
                "Los precios no incluyen IVA. Forma de pago: 50% al inicio, 50% al finalizar. "
                "Plazo de ejecución: 30-45 días corridos. Incluye entrevistas virtuales y una reunión presencial."
            )
            #Esto varia segun la etiqueta asociada a cada producto.

            # Cargar el archivo HTML
            html_path = buscarPlantillaPresupuesto(record)
            if html_path is None:
                raise UserError("No se encontró una plantilla HTML para el producto seleccionado.")

            #Se debe cambiar el html_path segun la etiqueta asociada a cada producto.

            with open(html_path, "r", encoding="UTF-8") as file:
                html_content = file.read()

            # Agregar estilo con Google Fonts
            font_style = """
            <head>
                <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
                <style>
                body {
                    font-family: 'Roboto', sans-serif;
                }
                h1, h2 {
                    font-weight: 700;
                }
                p {
                    font-weight: 400;
                }
                </style>
            </head>
            """

            if "<head>" in html_content:
                html_content = html_content.replace("<head>", font_style, 1)
            else:
                html_content = font_style + html_content

            # Reemplazar variables en el HTML
            variables = {
                "{{NOMBRE_CLIENTE}}": contacto.split(" ")[0],
                "{{restoNombreEmpresa}}": " ".join(contacto.split(" ")[1:]),
                "{{nombre_contacto}}": nombre_cliente,
                "{{ precio_total }}": f"{precio} + IVA",
                "{{plazo_validez}}": str(plazo_validez),
                "{{forma_pago}}": forma_pago,
                "{{plazo_prederteminado}}": plazo_pago,
                "{{numero-presupuesto}}": numero_cotizacion,
                "{{numero_presupuesto}}": numero_cotizacion,
                #Horaciones editables PAGINA 1
                "{{ oracionEditable1_____________________________________________________________}}": "",
                "{{ oracionEditable2_____________________________________________________________}}": "", 
                #Horaciones editables PAGINA 2
                "{{ oracion_1______________________________________________________________________________________________}}": "",
                "{{ oracion_2______________________________________________________________________________________________}}": "",
                "{{ oracion_3______________________________________________________________________________________________}}": ""
            }

            for variable, placeholder in variables.items():
                html_content = html_content.replace(variable.strip(), placeholder.strip())

            # Guardar el HTML modificado
            modified_html_path = "/opt/odoo2/odoo/addons/GenerarPresupuesto/models/Hoja_Cotizaciones_Veo_para_Odoo_modificado4.html"
            with open(modified_html_path, "w", encoding="utf-8") as file:
                file.write(html_content)

            # Convertir HTML a PDF
            output_pdf_path = "/opt/odoo2/odoo/addons/GenerarPresupuesto/models/Presupuesto.pdf"

            #asyncio.run(cargarNavegador(modified_html_path, output_pdf_path))
            # Crear el archivo HTML como adjunto en Odoo
            with open(modified_html_path, "r", encoding="utf-8") as html_file:
               attachment = self.env["ir.attachment"].create({
                   "name": f"{record.name}_presupuesto.html",  # Nombre del archivo
                   "type": "binary",
                   "datas": base64.b64encode(html_file.read().encode("utf-8")).decode("utf-8"),  # Codificar el contenido HT>
                   "res_model": "sale.order",  # Relacionar el adjunto con el modelo 'sale.order'
                   "res_id": record.id,  # ID del registro relacionado
                   "mimetype": "text/html",  # Tipo MIME para HTML
               })

            # Enviar mensaje al chatter
            record.message_post(
                body="Presupuesto generado correctamente.",
                subject="Presupuesto Generado",
                attachment_ids=[attachment.id],
            )
            return attachment
