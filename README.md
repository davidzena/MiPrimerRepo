# MiPrimerRepo

Aplicación web para una **lomitería y hamburguesería** donde el cliente puede ver el menú y hacer su pedido online.

## Funcionalidades
- Menú con precios en guaraníes.
- Pedido online con cantidades, datos del cliente y notas.
- Opción de delivery con costo adicional de 10.000 Gs.
- Resumen final con total del pedido.
- Página de menú separada y navegación web simple.
- Página para compartir el enlace con clientes (`/compartir`).

## Rutas
- `/` : formulario para crear pedido.
- `/menu` : página de menú con precios.
- `/compartir` : página para copiar/compartir el enlace de pedidos.

## Estructura
- `app.py`: lógica de Flask y rutas.
- `templates/base.html`: layout base de la web.
- `templates/index.html`: página de pedidos.
- `templates/menu.html`: página de menú.
- `templates/share.html`: página para compartir el enlace a clientes.
- `static/styles.css`: estilos.

## Ejecutar
```bash
pip install flask
python app.py
```

Abrir: http://127.0.0.1:5000

## Publicar para clientes
Cuando publiques tu web (por ejemplo en Render/Railway), configurá la variable:

```bash
PUBLIC_URL=https://tu-dominio-publico.com
```

Así, en `/compartir` se mostrará el enlace correcto para enviar a tus clientes.
