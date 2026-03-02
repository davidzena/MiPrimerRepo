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
  <title>El Rey del Lomito - Pedidos Online</title>
  <style>
    :root {
      --vino: #7e1632;
      --dorado: #f0b429;
      --crema: #fff8ef;
      --verde: #1f8b4c;
      --texto: #2a2522;
    }
    body {
      font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
      margin: 0;
      background: linear-gradient(180deg, #fffdf9 0%, #f9efe0 60%, #fff7ec 100%);
      color: var(--texto);
    }
    header {
      background: radial-gradient(circle at top right, #a42f56 0%, var(--vino) 60%);
      color: white;
      padding: 36px 24px;
      text-align: center;
      position: relative;
      overflow: hidden;
    }
    header::after {
      content: "";
      position: absolute;
      width: 220px;
      height: 220px;
      right: -70px;
      top: -90px;
      border-radius: 50%;
      background: rgba(240, 180, 41, 0.24);
    }
    header h1 {
      margin: 0;
      font-size: 2.1rem;
      letter-spacing: 0.04em;
    }
    header p {
      margin: 10px 0 0;
      font-size: 1.05rem;
    }
    .hero-badges {
      margin-top: 16px;
      display: flex;
      justify-content: center;
      gap: 10px;
      flex-wrap: wrap;
    }
    .badge {
      background: rgba(255, 255, 255, 0.18);
      border: 1px solid rgba(255, 255, 255, 0.38);
      border-radius: 999px;
      padding: 6px 14px;
      font-size: 0.9rem;
    }
    main {
      max-width: 980px;
      margin: 24px auto;
      padding: 0 16px 30px;
    }
    .bloque {
      background: white;
      border-radius: 14px;
      padding: 20px;
      box-shadow: 0 8px 24px rgba(45, 22, 12, 0.08);
      margin-bottom: 18px;
      border: 1px solid #f3dfc4;
    }
    h2 {
      border-left: 5px solid var(--vino);
      padding-left: 10px;
      margin-top: 0;
    }
    .menu-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 10px;
    }
    .item {
      display: grid;
      grid-template-columns: 1fr auto auto;
      gap: 8px;
      align-items: center;
      border-bottom: 1px solid #f4ece2;
      padding: 10px 0;
    }
    .item label {
      font-weight: 600;
    }
    .item span {
      color: #5f5247;
      font-size: 0.94rem;
    }
    input[type="number"], input[type="text"], textarea {
      width: 100%;
      border: 1px solid #cebba5;
      border-radius: 8px;
      padding: 8px;
      font-size: 14px;
      box-sizing: border-box;
      background: #fffdf9;
    }
    .customer {
      margin-top: 20px;
      display: grid;
      gap: 10px;
    }
    .customer label {
      font-weight: 600;
      color: #4f443c;
    }
    button {
      margin-top: 20px;
      width: 100%;
      border: none;
      background: linear-gradient(90deg, #218943, var(--verde));
      color: white;
      font-size: 16px;
      padding: 12px;
      border-radius: 8px;
      cursor: pointer;
      font-weight: 600;
    }
    button:hover {
      filter: brightness(1.05);
    }
    .resultado {
      margin-top: 24px;
      border-top: 2px dashed #e9d7c1;
      padding-top: 16px;
      background: var(--crema);
      border-radius: 8px;
    }
    .error {
      color: #b00020;
      font-weight: bold;
    }
    .info {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 10px;
    }
    .info-card {
      background: #fff6ea;
      border: 1px solid #f0dcc1;
      border-radius: 10px;
      padding: 12px;
      font-size: 0.95rem;
    }
    .info-card strong {
      color: var(--vino);
      display: block;
      margin-bottom: 6px;
    }
    footer {
      text-align: center;
      color: #5e5147;
      margin: 16px 0 32px;
    }
  </style>
</head>
<body>
  <header>
    <h1>El Rey del Lomito</h1>
    <p>Sabores bien cordobeses, porciones abundantes y entrega rápida</p>
    <div class="hero-badges">
      <span class="badge">🍔 Ingredientes frescos</span>
      <span class="badge">🚚 Delivery de 20:00 a 00:30</span>
      <span class="badge">🔥 Promo 2x1 los miércoles</span>
    </div>
  </header>

  <main>
    <div class="bloque">
      <div class="info">
        <div class="info-card">
          <strong>📍 Estamos en</strong>
          Av. Siempre Viva 123, Barrio Centro
        </div>
        <div class="info-card">
          <strong>📞 Pedidos por WhatsApp</strong>
          +54 9 351 555-0101
        </div>
        <div class="info-card">
          <strong>💳 Medios de pago</strong>
          Efectivo, débito, crédito y transferencias
        </div>
      </div>
    </div>

    <div class="bloque">
      <form method="post">
        <h2>Lomitos</h2>
        <div class="menu-grid">
          {% for item in menu.lomitos %}
            <div class="item">
              <label for="{{ item.id }}">{{ item.nombre }} (${{ item.precio }})</label>
              <span>Cantidad:</span>
              <input id="{{ item.id }}" name="{{ item.id }}" type="number" min="0" value="{{ values.get(item.id, 0) }}" />
            </div>
          {% endfor %}
        </div>

        <h2>Hamburguesas</h2>
        <div class="menu-grid">
          {% for item in menu.hamburguesas %}
            <div class="item">
              <label for="{{ item.id }}">{{ item.nombre }} (${{ item.precio }})</label>
              <span>Cantidad:</span>
              <input id="{{ item.id }}" name="{{ item.id }}" type="number" min="0" value="{{ values.get(item.id, 0) }}" />
            </div>
          {% endfor %}
        </div>

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
    </div>

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
  <footer>
    Hecho con ❤️ para potenciar tu lomitería.
  </footer>
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
