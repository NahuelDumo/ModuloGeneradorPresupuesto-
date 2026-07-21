import re

with open('Plantillas/PlantillaDesarrolloWeb/Plantilla-Desarrollo-Web.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

html_content = re.sub(r'\{\{(.*?)\}\}', lambda m: '{{' + re.sub(r'<[^>]+>', '', m.group(1)).strip() + '}}', html_content)

matches = re.findall(
    r'<div class=\"[^\"]*\">Valor Cuota:<span class=\"[^\"]*\"><\/span><span class=\"[^\"]*\">(En 2 pagos [^<]*)<span class=\"[^\"]*\"> <\/span>Valor total: \{\{total_1\}\}<span class=\"[^\"]*\"><\/span><span class=\"[^\"]*\">\{\{valor_cuota1\}\}<\/span><\/span><\/div>',
    html_content
)
print('MATCHES ROBUST:', matches)
