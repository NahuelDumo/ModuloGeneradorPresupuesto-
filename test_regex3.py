import re

with open('Plantillas/PlantillaDesarrolloWeb/Plantilla-Actualizacion-de-Sitio-Web.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

html_content = re.sub(r'\{\{(.*?)\}\}', lambda m: '{{' + re.sub(r'<[^>]+>', '', m.group(1)).strip() + '}}', html_content)

new_content = re.sub(
    r'<div class=\"t m0 x5 ha (y18|yf) ff2 fs8 fc3 sc0 lsb ws7\">Valor Cuota:<span class=\"_ _3\"><\/span><span class=\"fs9 lsa\">(En 2 pagos [^<]*)<span class=\"_ _4\"> <\/span>Valor total: \{\{total_1\}\}<span class=\"_ _5\"><\/span><span class=\"ff3 fs8 lsb ws3\">\{\{valor_cuota1\}\}<\/span><\/span><\/div>',
    lambda m: (
        r'foo'
    ),
    html_content
)
if html_content != new_content:
    print('CHANGED ACTUALIZACION')
else:
    print('NOT CHANGED ACTUALIZACION')
