"""Corre el _compute_web_product_flags y buscarPlantillaPresupuesto REALES con un `odoo` falso.
Uso: python test_flags_especial.py   (desde la raíz del módulo)"""
import importlib, sys, types

odoo = types.ModuleType('odoo')
odoo.models = types.SimpleNamespace(Model=object)
odoo.fields = types.SimpleNamespace(**{n: (lambda *a, **k: None) for n in
    ['Boolean', 'Char', 'Text', 'Many2one', 'One2many', 'Integer', 'Float', 'Binary', 'Selection', 'Date', 'Datetime', 'Html']})
odoo.api = types.SimpleNamespace(depends=lambda *a, **k: (lambda f: f), model=lambda f: f,
                                 onchange=lambda *a, **k: (lambda f: f), model_create_multi=lambda f: f)
exc = types.ModuleType('odoo.exceptions'); exc.UserError = Exception
sys.modules.update({'odoo': odoo, 'odoo.exceptions': exc})
pkg = types.ModuleType('mod'); pkg.__path__ = ['models']; sys.modules['mod'] = pkg
gp = importlib.import_module('mod.generar_presupuesto')
buscar = importlib.import_module('mod.funciones').buscarPlantillaPresupuesto


class Lista(list):  # imita recordset.mapped('a.b')
    def mapped(self, path):
        out = self
        for attr in path.split('.'):
            out = Lista(getattr(o, attr) for o in out if o is not None)
        return out


def orden(*lineas):
    def prod(n, c):
        return types.SimpleNamespace(name=n, categ_id=types.SimpleNamespace(name=c))
    return types.SimpleNamespace(order_line=Lista(types.SimpleNamespace(product_id=prod(n, c)) for n, c in lineas))


def especial(*lineas):
    r = orden(*lineas); gp.SaleOrder._compute_web_product_flags([r]); return r.is_desarrollo_web_especial


# Bug de Romi: producto gráfico "especial" NO es web especial
assert not especial(("Impresión de pieza gráfica especial", "Grafica"))
assert not especial(("Diseño gráfico de pieza gráfica especial", "Grafica"))
assert not especial(("Impresión de pieza editorial especial", "Editorial"))
assert not especial(("Creación de Sitio Web Basico", "Desarrollo Web"), ("Impresión de pieza gráfica especial", "Grafica"))
# Lo web especial sigue funcionando
assert especial(("Creación de sitio web especial", "Desarrollo Web"))
assert especial(("Creación de tienda on-line", "Desarrollo Web"))
assert especial(("Creación de sitio web especial", "Grafica"))  # por nombre exacto, como antes

# Plantilla: sin coincidencia exacta, "especial" fuera de web no debe caer en Web Especial
assert not buscar(orden(("Pieza rara especial", "Grafica"))).endswith("Plantilla-Desarrollo-Web-Especial.html")
assert buscar(orden(("Sitio a medida especial", "Desarrollo Web"))).endswith("Plantilla-Desarrollo-Web-Especial.html")
assert buscar(orden(("Impresión de pieza gráfica especial", "Grafica"))).endswith("plantillaGrafica_G2_DGPiezaGEspecial.html")

# Ruteo Servicios Web
assert buscar(orden(("Cloud Server", "Servicios Web"))).endswith("Cloud-Plantilla.html")
assert buscar(orden(("Soporte y Mantenimiento Web", "Servicios Web"))).endswith("Soporte-y-Mantenimiento-Web-Plantilla.html")
assert buscar(orden(("Registro o actualización de dominios", "Servicios Web"))).endswith("Gestión-de-Dominio-Plantilla.html")
assert buscar(orden(("Registro o Actualizacion de dominios", "Servicios Web"))).endswith("Gestión-de-Dominio-Plantilla.html")
assert buscar(orden(("Servicio de Hosting", "Servicios Web"))).endswith("Plantilla-Hosting.html")

# Flags Servicios Web
def flags(*lineas):
    r = orden(*lineas)
    gp.SaleOrder._compute_web_product_flags([r])
    return r

r_cloud = flags(("Cloud Server", "Servicios Web"))
assert r_cloud.is_cloud
assert r_cloud.is_servicios_web

r_soporte = flags(("Soporte y Mantenimiento Web", "Servicios Web"))
assert r_soporte.is_soporte_web
assert r_soporte.is_servicios_web

r_dominio = flags(("Registro o actualización de dominios", "Servicios Web"))
assert r_dominio.is_servicios_web

r_hosting = flags(("Servicio de Hosting", "Servicios Web"))
assert r_hosting.is_hosting
assert r_hosting.is_servicios_web

r_basico = flags(("Creación de Sitio Web Basico", "Desarrollo Web"))
assert not r_basico.is_servicios_web

assert buscar(orden(("Certificado SSL", "Servicios Web"))).endswith("SSL-Plantilla.html")
r_ssl = flags(("Certificado SSL", "Servicios Web"))
assert r_ssl.is_ssl
assert r_ssl.is_servicios_web
assert not flags(("Cloud Server", "Servicios Web")).is_ssl

PACK = "Servicios-Web-_Completo_-Plantilla.html"
assert buscar(orden(("Servicio Web Completo", "Servicios Web"))).endswith(PACK)
assert buscar(orden(("Pack Servicios Web", "Servicios Web"))).endswith(PACK)
# combinar productos sueltos ya NO activa el pack
assert not buscar(orden(("Servicio de Hosting", "Servicios Web"), ("Certificado SSL", "Servicios Web"))).endswith(PACK)
assert buscar(orden(("Servicio de Hosting", "Servicios Web"))).endswith("Plantilla-Hosting.html")
assert not buscar(orden(("Cloud Server", "Servicios Web"))).endswith(PACK)
assert flags(("Servicio Web Completo", "Servicios Web")).is_pack_web
assert not flags(("Servicio de Hosting", "Servicios Web"), ("Certificado SSL", "Servicios Web")).is_pack_web
assert not flags(("Registro o actualización de dominios", "Servicios Web")).is_actualizacion_web
assert flags(("Actualización Sitio Web", "Desarrollo Web")).is_actualizacion_web
assert not flags(("Creación de Sitio Web Basico", "Desarrollo Web")).is_pack_web

print("OK")
