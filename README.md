# MiPrimerRepo

## Bienvenido

Esta herramienta en Python te permite gestionar citas para colocación de
pestañas desde la línea de comandos. Puedes registrar clientas, agendar citas y
generar recordatorios para las próximas 24 horas.

### Requisitos

- Python 3.9 o superior.

### Uso básico

1. **Registrar una clienta**

   ```bash
   python app.py agregar-cliente "Nombre de la clienta" "Contacto"
   ```

2. **Agendar una cita**

   ```bash
   python app.py agendar "Nombre de la clienta" "Contacto" 2024-08-05T15:30 "Servicio"
   ```

   La fecha debe estar en formato ISO 8601 (`AAAA-MM-DDTHH:MM`). Si la clienta ya
   está registrada, el dato de contacto no se modifica.

3. **Listar citas**

   ```bash
   python app.py listar
   ```

   Agrega `--todas` para incluir citas pasadas.

4. **Generar recordatorios**

   ```bash
   python app.py recordatorios
   ```

   Esta opción muestra los recordatorios para citas dentro de las próximas 24
   horas y marca esas citas como notificadas para evitar duplicados.

Los datos se almacenan en el archivo `citas.json` dentro del directorio del
proyecto.

Autor: David Zena
