from flask import Flask, render_template_string, request

app = Flask(__name__)

MENU = {
    "lomitos": [
        {
            "id": "lomito_clasico",
            "nombre": "Lomito Clásico (Carne Mixta y ensalada)",
            "precio": 4500,
        },
        {
            "id": "lomito_solo_mixto",
            "nombre": "Lomito solo carne mixta (Carne vacuna y carne de vaca)",
            "precio": 5000,
        },
    ],
    "hamburguesas": [
        {"id": "hamburguesa_simple", "nombre": "Hamburguesa Simple", "precio": 3900},
        {"id": "hamburguesa_doble", "nombre": "Hamburguesa Doble", "precio": 5200},
        {"id": "hamburguesa_bacon", "nombre": "Hamburguesa Bacon", "precio": 5700},
    ],
}

TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Lomi & Burger - Pedidos</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      background: #f7f4ef;
      color: #2b2b2b;
    }
    header {
      background: #8b1e3f;
      color: white;
      padding: 24px;
      text-align: center;
    }
    main {
      max-width: 900px;
      margin: 24px auto;
      background: white;
      border-radius: 12px;
      padding: 20px;
      box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    }
    h2 {
      border-left: 5px solid #8b1e3f;
      padding-left: 10px;
    }
    .item {
      display: grid;
      grid-template-columns: 1fr auto auto;
      gap: 8px;
      align-items: center;
      border-bottom: 1px solid #ececec;
      padding: 10px 0;
    }
    input[type="number"], input[type="text"], textarea {
      width: 100%;
      border: 1px solid #bbb;
      border-radius: 8px;
      padding: 8px;
      font-size: 14px;
    }
    .customer {
      margin-top: 20px;
      display: grid;
      gap: 10px;
    }
    button {
      margin-top: 20px;
      width: 100%;
      border: none;
      background: #238636;
      color: white;
      font-size: 16px;
      padding: 12px;
      border-radius: 8px;
      cursor: pointer;
    }
    .resultado {
      margin-top: 24px;
      border-top: 2px dashed #ddd;
      padding-top: 16px;
      background: #fcfcfc;
      border-radius: 8px;
    }
    .error {
      color: #b00020;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <header>
    <h1>Lomi & Burger</h1>
    <p>Tomá pedidos de lomitos y hamburguesas de forma rápida</p>
  </header>

  <main>
    <form method="post">
      <h2>Lomitería</h2>
      {% for item in menu.lomitos %}
        <div class="item">
          <label for="{{ item.id }}">{{ item.nombre }} (${{ item.precio }})</label>
          <span>Cantidad:</span>
          <input id="{{ item.id }}" name="{{ item.id }}" type="number" min="0" value="{{ values.get(item.id, 0) }}" />
        </div>
      {% endfor %}

      <h2>Hamburguesería</h2>
      {% for item in menu.hamburguesas %}
        <div class="item">
          <label for="{{ item.id }}">{{ item.nombre }} (${{ item.precio }})</label>
          <span>Cantidad:</span>
          <input id="{{ item.id }}" name="{{ item.id }}" type="number" min="0" value="{{ values.get(item.id, 0) }}" />
        </div>
      {% endfor %}

      <div class="customer">
        <label>Nombre del cliente
          <input type="text" name="cliente" value="{{ values.get('cliente', '') }}" required />
        </label>
        <label>Dirección de entrega
          <input type="text" name="direccion" value="{{ values.get('direccion', '') }}" required />
        </label>
        <label>Notas para el pedido
          <textarea name="notas" rows="3">{{ values.get('notas', '') }}</textarea>
        </label>
      </div>

      <button type="submit">Confirmar pedido</button>
    </form>

    {% if error %}
      <p class="error">{{ error }}</p>
    {% endif %}

    {% if resumen %}
      <div class="resultado">
        <h3>Pedido confirmado para {{ resumen.cliente }}</h3>
        <p><strong>Dirección:</strong> {{ resumen.direccion }}</p>
        <p><strong>Notas:</strong> {{ resumen.notas or 'Sin notas' }}</p>
        <ul>
          {% for linea in resumen.detalle %}
            <li>{{ linea }}</li>
          {% endfor %}
        </ul>
        <p><strong>Total:</strong> ${{ resumen.total }}</p>
      </div>
    {% endif %}
  </main>
</body>
</html>
"""


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
                    detalle.append(f"{cantidad} x {item['nombre']} = ${subtotal}")

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

    return render_template_string(TEMPLATE, menu=MENU, resumen=resumen, error=error, values=values)


if __name__ == "__main__":
    app.run(debug=True)
