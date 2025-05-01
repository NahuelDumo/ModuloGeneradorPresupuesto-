import asyncio
from odoo import models, fields, api, _
from fpdf import FPDF
from PIL import Image
import base64
from io import BytesIO
from odoo.exceptions import UserError
from playwright.async_api import async_playwright
from .funciones import *
import asyncio
import base64
import tempfile
import os



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
    async def cargarNavegador(self, modified_html_path, output_pdf_path):
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

            # Datos
            nombre_cliente = record.partner_id.name or "-"
            contacto = record.partner_id.parent_id.name or "-"
            numero_cotizacion = record.name
            forma_pago = record.payment_method
            nombre_servicio = record.order_line[0].product_id.name or "No disponible"
            descripcion_servicio = record.order_line[0].name or "No disponible"
            precio = record.order_line[0].price_unit
            plazo_validez = record.validity_date or "No disponible"
            plazo_pago = record.payment_term_id.name if record.payment_term_id else "No disponible"

            # Oraciones editables
            texto1 = record.text_pagina1
            texto2 = record.text_pagina2

            oraciones_texto1 = dividir_en_oraciones(texto1, max_len=82)
            oracion_editable1 = oraciones_texto1[0] if len(oraciones_texto1) > 0 else ""
            oracion_editable2 = oraciones_texto1[1] if len(oraciones_texto1) > 1 else ""

            oraciones_texto2 = dividir_en_oraciones(texto2, max_len=118)
            oracion_1 = oraciones_texto2[0] if len(oraciones_texto2) > 0 else ""
            oracion_2 = oraciones_texto2[1] if len(oraciones_texto2) > 1 else ""
            oracion_3 = oraciones_texto2[2] if len(oraciones_texto2) > 2 else ""

            # Buscar HTML base
            html_path = buscarPlantillaPresupuesto(record)
            if html_path is None:
                raise UserError("No se encontró una plantilla HTML para el producto seleccionado.")

            with open(html_path, "r", encoding="UTF-8") as file:
                html_content = file.read()

            # Agregar Google Fonts
            font_style = """
            <head>
                <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
                <style>
                body { font-family: 'Roboto', sans-serif; }
                h1, h2 { font-weight: 700; }
                p { font-weight: 400; }
                </style>
            </head>
            """
            html_content = html_content.replace("<head>", font_style, 1) if "<head>" in html_content else font_style + html_content

            # Reemplazar variables
            variables = {
                "{{NOMBRE_CLIENTE}}": contacto.split(" ")[0],
                "{{restoNombreEmpresa}}": " ".join(contacto.split(" ")[1:]),
                "{{nombre_contacto}}": nombre_cliente,
                "{{ precio_total }}": f"<b>{precio} + IVA</b>",
                "{{plazo_validez}}": str(plazo_validez),
                "{{forma_pago}}": forma_pago,
                "{{plazo_prederteminado}}": plazo_pago,
                "{{numero-presupuesto}}": numero_cotizacion,
                "{{numero_presupuesto}}": f"<b>{numero_cotizacion}</b>",
                "{{ oracionEditable1_____________________________________________________________}}": oracion_editable1,
                "{{ oracionEditable2_____________________________________________________________}}": oracion_editable2,
                "{{ oracion_1______________________________________________________________________________________________}}": oracion_1,
                "{{ oracion_2______________________________________________________________________________________________}}": oracion_2,
                "{{ oracion_3______________________________________________________________________________________________}}": oracion_3,
            }

            for var, val in variables.items():
                html_content = html_content.replace(var.strip(), val.strip())

            # Crear archivo HTML temporal
            with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8") as html_file:
                html_file.write(html_content)
                temp_html_path = html_file.name

            # Crear archivo PDF temporal
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
                temp_pdf_path = pdf_file.name

            # Generar PDF con Playwright
            asyncio.run(self.cargarNavegador(temp_html_path, temp_pdf_path))

            # Leer el contenido del PDF para adjuntarlo
            with open(temp_pdf_path, "rb") as pdf_file:
                attachment = self.env["ir.attachment"].create({
                    "name": f"{record.name}_presupuesto.pdf",
                    "type": "binary",
                    "datas": base64.b64encode(pdf_file.read()).decode("utf-8"),
                    "res_model": "sale.order",
                    "res_id": record.id,
                    "mimetype": "application/pdf",
                })

            # Publicar en el chatter
            record.message_post(
                body="Presupuesto generado correctamente.",
                subject="Presupuesto Generado",
                attachment_ids=[attachment.id],
            )

            # Limpiar archivos temporales (opcional)
            os.remove(temp_html_path)
            os.remove(temp_pdf_path)

            return attachment