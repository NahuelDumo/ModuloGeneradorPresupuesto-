import re

html = open(r"d:\Cosas Nahuel\TrabajoVeo\Modulos Personalizados\ModuloGeneradorPresupuesto(actual)\Plantillas\PlantillaDesarrolloWeb\Plantilla-Desarrollo-Web.html", 'r', encoding='utf-8').read()
html = re.sub(r'\{\{(.*?)\}\}', lambda m: '{{' + re.sub(r'<[^>]+>', '', m.group(1)).strip() + '}}', html)
res = re.search(r'<div class="t m0 x5 ha y18 ff2 fs8 fc3 sc0 lsb ws7">Valor Cuota:<span class="_ _3"></span><span class="fs9 lsa">(En 2 pagos [^<]*)<span class="_ _4"> </span>Valor total: \{\{total_1\}\}<span class="_ _5"></span><span class="ff3 fs8 lsb ws3">\{\{valor_cuota1\}\}</span></span></div>', html)

print('MATCHED:', res is not None)
if res:
    print('GROUP 1:', res.group(1))
