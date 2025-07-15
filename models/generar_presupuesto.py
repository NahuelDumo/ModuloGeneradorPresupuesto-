
from odoo import models, fields
import base64
from odoo.exceptions import UserError
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
        string="Esp. Técnicas editables.",
        required=True,
        size=162,
        help="Especifica el texto de la pagina 1 ESPECIFICACIONES TECNICAS.",
    )
    text_pagina2 = fields.Char(
        string="Condiciones editables.",
        required=True,
        size=315,
        help="Especifica el texto de la pagina 2. Condiciones editables",
    )
    
    def generar_presupuesto_pdf(self):
        for record in self:
            if not record.partner_id or not record.order_line:
                raise ValueError("La orden de venta no tiene cliente o líneas de productos.")

            # Datos necesarios para el PDF
            nombre_cliente = f"<span style='font-family: Roboto, sans-serif; word-spacing: 0px;'>{record.partner_id.name or '-'}</span>"
            contacto = record.partner_id.parent_id.name or ""
            
            if len(contacto) <= 19:
                contacto = f"<span style='font-family: Roboto, sans-serif;'>{(contacto)}</span>"
            else:
                contacto = f"<span style='font-family: Roboto, sans-serif ;font-size: 80px;'>{cadena_reformada(contacto)}</span>"
                nombre_cliente = f"<span style='font-family: Roboto, sans-serif; word-spacing: 0px;font-size: 75px; '><br>{record.partner_id.name or ''}</span>"
            
            numero_cotizacion = record.name
            forma_pago = f"<span style='font-family: Roboto, sans-serif; word-spacing: 0px;'>{record.payment_method}</span>"
            nombre_servicio = record.order_line[0].product_id.name or "No disponible"
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
                def get_cantidad(line):
                    val = round(line.product_uom_qty)
                    return "" if val < 2 else val

                def get_precio(line):
                    val = round(line.price_unit)
                    return "" if val < 2 else val

                lineas = record.order_line

                cantidad_unidades1 = get_cantidad(lineas[0])
                cantidad_unidades2 = get_cantidad(lineas[1])
                cantidad_unidades3 = get_cantidad(lineas[2])

                precio1 = get_precio(lineas[0])
                precio2 = get_precio(lineas[1])
                precio3 = get_precio(lineas[2])

                precioTotal1 = round(precio1 * cantidad_unidades1) if precio1 != "" and cantidad_unidades1 != "" else ""
                precioTotal2 = round(precio2 * cantidad_unidades2) if precio2 != "" and cantidad_unidades2 != "" else ""
                precioTotal3 = round(precio3 * cantidad_unidades3) if precio3 != "" and cantidad_unidades3 != "" else ""



            plazo_validez = record.validity_date or "No disponible"
            plazo_pago = record.payment_term_id.name if record.payment_term_id else "No disponible"

            # Oraciones editables
            texto1 = record.text_pagina1
            texto2 = record.text_pagina2
            # Inicializacion de variables para oraciones editables
            oracion_editable1 = ""
            oracion_editable2 = ""
            item1 = ""
            item2 = ""
            item3 = ""
            item4 = ""
            item5 = ""
            item6 = ""

            for line in record.order_line:
                categ_name = line.product_id.categ_id.name if line.product_id.categ_id else ""
                if categ_name not in ["Editorial", "Grafica"]:
                    #Divido en oraciones editables
                    oraciones_texto1 = dividir_en_oraciones(texto1, max_len=75)

                    # Divido en oraciones editables
                    oracion_editable1 = f"<span style='font-family: Roboto, sans-serif ; word-spacing: 0px;'>{oraciones_texto1[0]}</span>" if len(oraciones_texto1) > 0 else ""
                    oracion_editable2 = f"<span style='font-family: Roboto, sans-serif ; word-spacing: 0px;'>{oraciones_texto1[1]}</span>" if len(oraciones_texto1) > 1 else ""
                
                else:
                    oraciones_texto1 = dividir_en_items(texto1)

                    # Divido en oraciones editables
                    items = [oraciones_texto1[i] if len(oraciones_texto1) > i else "" for i in range(6)]
                    item1, item2, item3, item4, item5, item6 = items
                
        
            oraciones_texto2 = dividir_en_oraciones(texto2, max_len=105)


            # Se asignan las oraciones editables a variables
            oracion_1 = oraciones_texto2[0] if len(oraciones_texto2) > 0 else ""
            oracion_2 = oraciones_texto2[1] if len(oraciones_texto2) > 1 else ""
            oracion_3 = oraciones_texto2[2] if len(oraciones_texto2) > 2 else ""
            # Se asignan las oraciones editables a variables
           

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
        @media print {
        #page-container {
            display: flex;
            flex-direction: column;
        }
        #page-container > div[id^="pf"] {
            height: 100vh;              /* Usa el alto máximo visible de la hoja */
            overflow: hidden !important; /* Corta el contenido que se pasa */
            page-break-inside: avoid !important; /* Evita cortes dentro */
            page-break-before: auto;
            page-break-after: auto;
            }
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
                
                "{{NOMBRE_CLIENTE}}": contacto,
                "{{nombre_contacto}}": nombre_cliente,
                "{{ precio_total }}": f"<span style='font-family: Roboto, sans-serif; font-weight: 700;'>{round(precio, 0)} + IVA</span>",
                "{{numero_presupuesto}}": f"<span style='font-family: Roboto, sans-serif; font-weight: 700;'>{numero_cotizacion}</span>",
                "{{plazo_validez}}": str(plazo_validez),
                "{{forma_pago}}": forma_pago,
                "{{plazo_prederteminado}}": plazo_pago,
                "{{numero-presupuesto}}": f"<span style='font-family: Roboto, sans-serif; font-weight: 700;'>{numero_cotizacion}</span>",
                #Horaciones editables PAGINA 1
                "{{oracionEditable1_______________________________________________________}}": oracion_editable1,
                "{{oracionEditable2_______________________________________________________}}": oracion_editable2, 

                
                "{{item1}}": f"<span style='font-family: Roboto, sans-serif; word-spacing: 0px; display:inline-block; width: 680px;'> {item1}</span>",
                "{{item2}}": f"<span style='font-family: Roboto, sans-serif; word-spacing: 0px; display:inline-block; width: 680px;'> {item2}</span>",
                "{{item3}}": f"<span style='font-family: Roboto, sans-serif; word-spacing: 0px; display:inline-block; width: 680px;'> {item3}</span>",
                "{{item4}}": f"<span style='font-family: Roboto, sans-serif; word-spacing: 0px; display:inline-block; width: 680px;'> {item4}</span>",
                "{{item5}}": f"<span style='font-family: Roboto, sans-serif; word-spacing: 0px; display:inline-block; width: 680px;'> {item5}</span>",
                "{{item6}}": f"<span style='font-family: Roboto, sans-serif; word-spacing: 0px; display:inline-block; width: 680px;'> {item6}</span>",
                #Horaciones editables PAGINA 2
                "{{oracion_1______________________________________________________________________________________________}}": oracion_1,
                "{{oracion_2______________________________________________________________________________________________}}": oracion_2,
                "{{oracion_3______________________________________________________________________________________________}}": oracion_3,
                
                ###########################################EXCEPCIONALES#######################################################
                # Impresion de Boletin, Libro, Pieza Editorial, Revista
                # Impresion de Boletin, Libro, Pieza Editorial, Revista

                "{{ cantidad_unidades1 }}": f"<span style='font-family: Roboto, sans-serif;'>{str(cantidad_unidades1)}</span>",
                "{{ cantidad_unidades2 }}": f"<span style='font-family: Roboto, sans-serif;'>{str(cantidad_unidades2)}</span>",
                "{{ cantidad_unidades3 }}": f"<span style='font-family: Roboto, sans-serif;'>{str(cantidad_unidades3)}</span>",
                "{{ precio_cantidad_1 }}": f"<span style='font-family: Roboto, sans-serif;'>{str(precio1)}</span>",
                "{{ precio_cantidad_2 }}": f"<span style='font-family: Roboto, sans-serif;'>{str(precio2)}</span>",
                "{{ precio_cantidad_3 }}": f"<span style='font-family: Roboto, sans-serif;'>{str(precio3)}</span>",
                "{{ precio_total1 }}": f"<span style='font-family: Roboto, sans-serif;'>{str(precioTotal1) + ' + IVA'}</span>",
                "{{ precio_total2 }}": f"<span style='font-family: Roboto, sans-serif;'>{str(precioTotal2) + ' + IVA'}</span>",
                "{{ precio_total3 }}": f"<span style='font-family: Roboto, sans-serif;'>{str(precioTotal3) + ' + IVA'}</span>"
            }


            for variable, placeholder in variables.items():
                html_content = html_content.replace(variable.strip(), placeholder.strip())

            # Guardar el HTML modificado (pero no lo adjuntamos)
            modified_html_path = "/opt/odoo2/odoo/addons/GenerarPresupuesto/models/Hoja_Cotizaciones_Veo_para_Odoo_modificado4.html"
            with open(modified_html_path, "w", encoding="utf-8") as file:
                file.write(html_content)

            # Convertir HTML a PDF usando API externa
            import requests
            try:
                # Extraer IDs de página automáticamente (ej: pf1,pf2,pf3)
                with open(modified_html_path, "r", encoding="utf-8") as html_file:
                    content = html_file.read()
                    import re
                    page_ids = ",".join(re.findall(r'id="(pf\d+)"', content)) or "pf1"

                with open(modified_html_path, "rb") as f:
                    files = {'html_file': ('presupuesto.html', f, 'text/html')}
                    data = {'page_ids': page_ids}

                    response = requests.post("https://apiconversorpdf.onrender.com/convert-html-to-pdf", files=files, data=data)
                    response.raise_for_status()
                    pdf_content = response.content
            except Exception as e:
                raise UserError(f"Error al generar el PDF desde la API externa: {str(e)}")

            # Guardar solo el PDF como adjunto
            attachment_pdf = self.env["ir.attachment"].create({
                "name": f"{record.name}_presupuesto.pdf",
                "type": "binary",
                "datas": base64.b64encode(pdf_content).decode("utf-8"),
                "res_model": "sale.order",
                "res_id": record.id,
                "mimetype": "application/pdf",
            })

            # Enviar mensaje al chatter con solo el PDF adjunto
            record.message_post(
                body="Presupuesto generado correctamente.",
                subject="Presupuesto Generado",
                attachment_ids=[attachment_pdf.id],
            )

            return attachment_pdf
