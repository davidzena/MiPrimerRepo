from flask import Flask, render_template, request

app = Flask(__name__)

MENU = {
    "lomitos": [
        {
            "id": "lomito_clasico",
            "nombre": "Lomito Clásico (Carne Mixta y ensalada)",
            "precio": 25000,
        },
        {
            "id": "lomito_solo_mixto",
            "nombre": "Lomito solo carne mixta (Carne vacuna y carne de vaca)",
            "precio": 30000,
        },
    ],
    "hamburguesas": [
        {"id": "hamburguesa_simple", "nombre": "Hamburguesa Simple", "precio": 3900},
    ],
}

def parse_quantity(value: str) -> int:
    try:
        quantity = int(value)
        return max(quantity, 0)
    except (TypeError, ValueError):
        return 0


@app.route("/", methods=["GET", "POST"])
def index():
    resumen = None
    error = None
    values = {}

    if request.method == "POST":
        values = request.form.to_dict()
        detalle = []
        total = 0

        for categoria in MENU.values():
            for item in categoria:
                cantidad = parse_quantity(request.form.get(item["id"]))
                values[item["id"]] = cantidad
                if cantidad > 0:
                    subtotal = cantidad * item["precio"]
                    total += subtotal
                    detalle.append(f"{cantidad} x {item['nombre']} = Gs {subtotal:,}".replace(",", "."))

        if total == 0:
            error = "Debes seleccionar al menos un producto para confirmar el pedido."
        else:
            resumen = {
                "cliente": request.form.get("cliente", "Cliente"),
                "direccion": request.form.get("direccion", "Sin dirección"),
                "notas": request.form.get("notas", ""),
                "detalle": detalle,
                "total": total,
            }

    return render_template("index.html", menu=MENU, resumen=resumen, error=error, values=values)


if __name__ == "__main__":
    app.run(debug=True)
