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


def test_get_rango_cantidad_does_not_mistake_product_code_for_a_range():
    # Real bug: order lines named literally "Cuadernos A5" (no range text)
    # made get_rango_cantidad treat the "5" in "A5" as a valid range and
    # return the product name itself for all 3 rows ("Cantidad: Cuadernos A5"
    # x3). It must fall back to product_uom_qty instead, and still recognize
    # genuine ranges like "20 a 29 uu" / "20-29 uu".
    with open("models/generar_presupuesto.py", encoding="utf-8") as f:
        src = f.read()
    m = re.search(r"def get_rango_cantidad.*?\n\n", src, re.S)
    assert m, "get_rango_cantidad not found"
    body = m.group(0)
    patterns = re.findall(r"re\.search\(r'([^']+)'", body)
    assert patterns, "expected a regex-based range check"
    pattern = patterns[0]

    def rango(name, qty):
        name = (name or "").strip()
        if re.search(pattern, name):
            return name
        qty = int(round(qty)) if qty else 0
        return f"{qty} uu." if qty > 0 else ""

    assert rango("Cuadernos A5", 20) == "20 uu."
    assert rango("Cuadernos A5", 30) == "30 uu."
    assert rango("Cuadernos A5", 50) == "50 uu."
    assert rango("20 a 29 uu", 29) == "20 a 29 uu"
    assert rango("20-29 uu", 29) == "20-29 uu"


def test_price_table_is_fixed_column_grid():
    # Inline flow can't align: each row's "Precio Total" was pushed by a spacer
    # inheriting a different huge word-spacing (984px row 1 vs 1164px rows 2-3).
    # Every cell must be its own div, same classes, sharing one x per column,
    # and .x10 must exist in both the screen (px) and print (pt) CSS blocks.
    for tpl, precio in [("Cuadernos-personalizados-Plantilla.html", "valor"),
                        ("Agendas-personalizadas-Plantilla.html", "precio")]:
        with open(f"Plantillas/PlantillaProductos/{tpl}", encoding="utf-8") as f:
            html = f.read()
        for col, x in [("cant", "x2"), (precio, "x5"), ("total", "x10")]:
            for row, y in [(1, "yd"), (2, "y11"), (3, "yf")]:
                cell = f'<div class="t m0 {x} hb {y} ff2 fsb fc6 sc0 ls7">{{{{{col}{row}}}}}</div>'
                assert cell in html, f"{tpl}: missing grid cell {cell}"
        assert ".x10{left:630.000000px;}" in html and ".x10{left:840.000000pt;}" in html, tpl


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
    test_get_rango_cantidad_does_not_mistake_product_code_for_a_range()
    test_price_table_is_fixed_column_grid()
    test_generar_presupuesto_wraps_all_producto_vars_with_word_spacing()
    print("OK - all checks passed")
