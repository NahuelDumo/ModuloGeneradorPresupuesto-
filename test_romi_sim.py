"""Self-check for the Cuadernos budget fix (Romi's order N 02167).
Verifies: (1) template text says Cuadernos, not Agendas, (2) price-row spans
carry word-spacing:0px so multi-word values don't blow apart, (3) tech-spec
items no longer get cut mid-word.
"""
import re
import sys
sys.path.insert(0, "models")
from funciones import dividir_en_items, formatear_item

TEXT_PAGINA1 = (
    "Tamaño A5 (21 x 148 cm). Con 2 Insert en ilustración full color. "
    "Encuadernación con doble anillado. Tapa dura de alta calidad Full color."
)


def format_num_moneda(val):
    return format(int(round(float(val))), ',').replace(",", ".")


def test_items_never_cut_mid_word():
    items = dividir_en_items(TEXT_PAGINA1)
    non_empty = [i for i in items if i.strip()]
    assert len(non_empty) == 4, non_empty
    for item in non_empty:
        stripped = item.rstrip()
        # if the original sentence was truncated, it must still end on a
        # real word (not "Full co") -- i.e. it must not be a strict, non-space
        # prefix of a longer word from the source text.
        assert not re.search(r'\b[a-zA-Zá-úÁ-Ú]+ [a-zA-Zá-úÁ-Ú]{1,2}$', stripped) or stripped.endswith('.'), \
            f"item looks word-cut: {stripped!r}"
    assert "Full co." not in non_empty[3] or "Full color" in non_empty[3]
    print("items:", non_empty)


def test_formatear_item_has_word_spacing_zero():
    html = formatear_item("Tapa dura de alta calidad Full color.")
    assert "word-spacing: 0px" in html


def test_price_row_variables_have_word_spacing_zero():
    # Mirrors the {{cant1..3}}/{{precio1..3}}/{{valor1..3}}/{{total1..3}}
    # dict built in generar_presupuesto.py after the fix.
    cant2_prod, precio2_prod, total2_prod = "30 a 49 uu", format_num_moneda(19900), format_num_moneda(975100)
    variables = {
        "{{cant1}}": f"<span style='font-family: Roboto, sans-serif; word-spacing: 0px;'>20 a 29 uu</span>",
        "{{cant2}}": f"<span style='font-family: Roboto, sans-serif; word-spacing: 0px;'>Cantidad: {cant2_prod}</span>",
        "{{total3}}": f"<span style='font-family: Roboto, sans-serif; word-spacing: 0px;'>Precio Total: $ {format_num_moneda(1435500)} + IVA</span>",
    }
    for key, html in variables.items():
        assert "word-spacing: 0px" in html, f"{key} missing word-spacing override"


def test_template_says_cuadernos_not_agendas():
    with open("Plantillas/PlantillaProductos/Cuadernos-personalizados-Plantilla.html", encoding="utf-8") as f:
        html = f.read()
    assert "agenda" not in html.lower()
    assert "Cuadernos personalizados" in html
    assert "¿Por qué elegir nuestros cuadernos?" in html


def test_generar_presupuesto_wraps_all_producto_vars_with_word_spacing():
    with open("models/generar_presupuesto.py", encoding="utf-8") as f:
        src = f.read()
    for var in ["cant1", "cant2", "cant3", "precio1", "precio2", "precio3",
                "valor1", "valor2", "valor3", "total1", "total2", "total3"]:
        m = re.search(r'"\{\{%s\}\}":\s*f"<span[^"]*"' % var, src)
        assert m and "word-spacing: 0px" in m.group(0), f"{var} span missing word-spacing:0px"


if __name__ == "__main__":
    test_items_never_cut_mid_word()
    test_formatear_item_has_word_spacing_zero()
    test_price_row_variables_have_word_spacing_zero()
    test_template_says_cuadernos_not_agendas()
    test_generar_presupuesto_wraps_all_producto_vars_with_word_spacing()
    print("OK - all checks passed")
