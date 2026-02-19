# MiPrimerRepo

Aplicación web para una **lomitería y hamburguesería** donde el cliente puede armar y confirmar su pedido online.

## Funcionalidades
- Menú con productos y precios en guaraníes (hamburguesa a 38.000 Gs).
- Formulario web para cantidades, nombre, dirección y notas.
- Opción de delivery con costo adicional de 10.000 Gs.
- Resumen final con detalle y total del pedido.
- Estructura separada en `templates/` y `static/` para una web más mantenible.

## Estructura
- `app.py`: lógica de la aplicación Flask.
- `templates/index.html`: plantilla principal de la página.
- `static/styles.css`: estilos de la interfaz.

## Ejecutar el proyecto
1. Instalar dependencias:
   ```bash
   pip install flask
   ```
2. Iniciar la app:
   ```bash
   python app.py
   ```
3. Abrir en navegador:
   - http://127.0.0.1:5000
