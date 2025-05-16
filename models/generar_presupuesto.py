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
import re



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
        size=150,
        help="Especifica el texto de la pagina 1 ESPECIFICACIONES TECNICAS.",
    )
    text_pagina2 = fields.Char(
        string="Texto editable pagina 2",
        required=True,
        size=315,
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
            # Agregar espacio antes de cada mayúscula en el nombre del cliente (excepto la primera letra)
            nombre_cliente = separar_mayusculas(nombre_cliente)
            contacto = record.partner_id.parent_id.name or "-"
            numero_cotizacion = record.name
            forma_pago = record.payment_method
            nombre_servicio = record.order_line[0].product_id.name or "No disponible"
            descripcion_servicio = record.order_line[0].name or "No disponible"
            precio = record.order_line[0].price_unit



            ##################################################### CASO EXCEPCIONAL #######################################################
            # Inicializar valores por defecto
            cantidad_unidades1 = ""
            cantidad_unidades2 = ""
            cantidad_unidades3 = ""

            precio1 = ""
            precio2 = ""
            precio3 = ""

            precioTotal1 = ""
            precioTotal2 = ""
            precioTotal3 = ""
            # Impresion de Boletin, Libro, Pieza Editorial, Revista
            if nombre_servicio.startswith("Impresión"):
                cantidad_unidades1 = record.order_line[0].product_uom_qty or 1
                cantidad_unidades2 = record.order_line[1].product_uom_qty or 1
                cantidad_unidades3 = record.order_line[2].product_uom_qty or 1

                precio1 = round(record.order_line[0].price_unit, 0) or 0.0
                precio2 = round(record.order_line[1].price_unit, 0) or 0.0
                precio3 = round(record.order_line[2].price_unit, 0) or 0.0

                precioTotal1 = round(precio1 * cantidad_unidades1, 0)
                precioTotal2 = round(precio2 * cantidad_unidades2, 0)
                precioTotal3 = round(precio3 * cantidad_unidades3, 0)


            plazo_validez = record.validity_date or "No disponible"
            plazo_pago = record.payment_term_id.name if record.payment_term_id else "No disponible"

            # Oraciones editables
            texto1 = record.text_pagina1
            texto2 = record.text_pagina2

            #Divido en oraciones editables
            oraciones_texto1 = dividir_en_oraciones(texto1, max_len=75)

            # Divido en oraciones editables
            oracion_editable1 = oraciones_texto1[0] if len(oraciones_texto1) > 0 else ""
            oracion_editable2 = oraciones_texto1[1] if len(oraciones_texto1) > 1 else ""
            
        
            oraciones_texto2 = dividir_en_oraciones(texto2, max_len=105)


            # Se asignan las oraciones editables a variables
            oracion_1 = oraciones_texto2[0] if len(oraciones_texto2) > 0 else ""
            oracion_2 = oraciones_texto2[1] if len(oraciones_texto2) > 1 else ""
            oracion_3 = oraciones_texto2[2] if len(oraciones_texto2) > 2 else ""
            # Se asignan las oraciones editables a variables
            record.message_post(
                body=f"oracion_1: {oracion_1}, oracion_2: {oracion_2}, oracion_3: {oracion_3}, nombre_cliente: {nombre_cliente}, contacto: {contacto}, numero_cotizacion: {numero_cotizacion}, forma_pago: {forma_pago}, plazo_validez: {plazo_validez}, plazo_pago: {plazo_pago}",
                subject="Texto editable"
            )

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
                "{{NOMBRE_CLIENTE}}": f'<span style="white-space: pre-wrap;">{contacto.split(" ")[0]}</span>',
                "{{restoNombreEmpresa}}": " ".join(contacto.split(" ")[1:]),
                "{{nombre_contacto}}": f'<span style="white-space: pre-wrap;">{nombre_cliente}</span>',
                "{{ precio_total }}": f"<span style='font-family: Roboto, sans-serif; font-weight: 700;'>{round(precio, 0)} + IVA</span>",
                "{{numero_presupuesto}}": f"<span style='font-family: Roboto, sans-serif; font-weight: 700;'>{numero_cotizacion}</span>",
                "{{plazo_validez}}": str(plazo_validez),
                "{{forma_pago}}": forma_pago,
                "{{plazo_prederteminado}}": plazo_pago,
                "{{numero-presupuesto}}": f"<span style='font-family: Roboto, sans-serif; font-weight: 700;'>{numero_cotizacion}</span>",
                #Horaciones editables PAGINA 1
                "{{oracionEditable1_______________________________________________________}}": oracion_editable1,
                "{{oracionEditable2_______________________________________________________}}": oracion_editable2, 
                #Horaciones editables PAGINA 2
                "{{oracion_1______________________________________________________________________________________________}}": oracion_1,
                "{{oracion_2______________________________________________________________________________________________}}": oracion_2,
                "{{oracion_3______________________________________________________________________________________________}}": oracion_3,
                
                ###########################################EXCEPCIONALES#######################################################
                # Impresion de Boletin, Libro, Pieza Editorial, Revista
                "{{ cantidad_unidades1 }}": str(cantidad_unidades1),
                "{{ cantidad_unidades2 }}": str(cantidad_unidades2),
                "{{ cantidad_unidades3 }}": str(cantidad_unidades3),
                "{{ precio_cantidad_1 }}": str(precio1),
                "{{ precio_cantidad_2 }}": str(precio2),
                "{{ precio_cantidad_3 }}": str(precio3),
                "{{ precio_total1 }}": str(precioTotal1) + " + IVA",
                "{{ precio_total2 }}": str(precioTotal2) + " + IVA",
                "{{ precio_total3 }}": str(precioTotal3) + " + IVA",
            
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
