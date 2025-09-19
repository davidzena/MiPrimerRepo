"""Herramienta de línea de comandos para agendar citas de colocación de pestañas.

Este módulo permite gestionar clientes, agendar citas y generar recordatorios
para las próximas citas. Los datos se almacenan en un archivo JSON sencillo para
facilitar su uso sin dependencias externas.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import Dict, List, Optional


DATA_FILE = "citas.json"
REMINDER_THRESHOLD_HOURS = 24


@dataclass
class Client:
    """Representa a una clienta de colocación de pestañas."""

    nombre: str
    contacto: str


@dataclass
class Appointment:
    """Representa una cita agendada."""

    client_name: str
    datetime_iso: str
    servicio: str
    recordatorio_enviado: bool = False

    @property
    def fecha(self) -> datetime:
        """Devuelve la fecha y hora de la cita como ``datetime``."""

        return datetime.fromisoformat(self.datetime_iso)


def load_data() -> Dict[str, List[Dict[str, str]]]:
    """Carga los datos de clientes y citas desde el archivo JSON."""

    if not os.path.exists(DATA_FILE):
        return {"clients": [], "appointments": []}

    with open(DATA_FILE, "r", encoding="utf-8") as fh:
        return json.load(fh)


def save_data(data: Dict[str, List[Dict[str, str]]]) -> None:
    """Guarda los datos de clientes y citas en el archivo JSON."""

    with open(DATA_FILE, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)


def find_client(data: Dict[str, List[Dict[str, str]]], nombre: str) -> Optional[Client]:
    """Busca una clienta por su nombre."""

    for client_raw in data.get("clients", []):
        if client_raw["nombre"].lower() == nombre.lower():
            return Client(**client_raw)
    return None


def ensure_client(data: Dict[str, List[Dict[str, str]]], nombre: str, contacto: str) -> Client:
    """Obtiene una clienta existente o la crea si no existe."""

    client = find_client(data, nombre)
    if client:
        return client

    client = Client(nombre=nombre, contacto=contacto)
    data.setdefault("clients", []).append(asdict(client))
    return client


def add_client(nombre: str, contacto: str) -> Client:
    """Crea una nueva clienta."""

    data = load_data()
    client = ensure_client(data, nombre, contacto)
    save_data(data)
    return client


def schedule_appointment(nombre: str, contacto: str, fecha: str, servicio: str) -> Appointment:
    """Agenda una nueva cita."""

    try:
        fecha_dt = datetime.fromisoformat(fecha)
    except ValueError as exc:
        raise SystemExit(
            "La fecha debe estar en formato ISO 8601, por ejemplo 2024-08-05T15:30"
        ) from exc

    data = load_data()
    client = ensure_client(data, nombre, contacto)

    appointment = Appointment(
        client_name=client.nombre,
        datetime_iso=fecha_dt.isoformat(),
        servicio=servicio,
    )
    data.setdefault("appointments", []).append(asdict(appointment))
    save_data(data)
    return appointment


def list_appointments(show_all: bool = False) -> List[Appointment]:
    """Obtiene las citas registradas, filtrando las pasadas si se desea."""

    data = load_data()
    appointments: List[Appointment] = [Appointment(**app) for app in data.get("appointments", [])]

    if show_all:
        return sorted(appointments, key=lambda app: app.fecha)

    now = datetime.now()
    upcoming = [app for app in appointments if app.fecha >= now]
    return sorted(upcoming, key=lambda app: app.fecha)


def generate_reminders() -> List[str]:
    """Genera mensajes de recordatorio para las citas próximas."""

    data = load_data()
    appointments = [Appointment(**raw) for raw in data.get("appointments", [])]
    now = datetime.now()
    reminder_limit = now + timedelta(hours=REMINDER_THRESHOLD_HOURS)

    reminder_messages: List[str] = []
    for appointment in appointments:
        if appointment.recordatorio_enviado:
            continue
        if not now <= appointment.fecha <= reminder_limit:
            continue

        client = find_client(data, appointment.client_name)
        contacto = client.contacto if client else "(contacto no registrado)"
        reminder_messages.append(
            (
                f"Recordatorio: {appointment.client_name} tiene cita de {appointment.servicio} "
                f"el {appointment.fecha.strftime('%d/%m/%Y a las %H:%M')} (contacto: {contacto})."
            )
        )
        appointment.recordatorio_enviado = True

    if reminder_messages:
        data["appointments"] = [asdict(app) for app in appointments]
        save_data(data)

    return reminder_messages


def parse_args() -> argparse.Namespace:
    """Configura y analiza los argumentos de la línea de comandos."""

    parser = argparse.ArgumentParser(
        description="Gestor de citas para colocación de pestañas",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    cliente_parser = subparsers.add_parser("agregar-cliente", help="Registrar una nueva clienta")
    cliente_parser.add_argument("nombre", help="Nombre completo de la clienta")
    cliente_parser.add_argument("contacto", help="Dato de contacto (teléfono, WhatsApp, email, etc.)")

    cita_parser = subparsers.add_parser("agendar", help="Agendar una nueva cita")
    cita_parser.add_argument("nombre", help="Nombre completo de la clienta")
    cita_parser.add_argument(
        "contacto",
        help="Dato de contacto. Si la clienta ya existe se ignorará este valor",
    )
    cita_parser.add_argument(
        "fecha",
        help="Fecha y hora en formato ISO 8601 (ej. 2024-08-05T15:30)",
    )
    cita_parser.add_argument("servicio", help="Tipo de servicio o nota de la cita")

    listar_parser = subparsers.add_parser(
        "listar",
        help="Mostrar citas próximas. Use --todas para incluir las pasadas",
    )
    listar_parser.add_argument(
        "--todas",
        action="store_true",
        dest="todas",
        help="Mostrar todas las citas, incluso las ya realizadas",
    )

    subparsers.add_parser("recordatorios", help="Generar recordatorios para citas próximas")

    return parser.parse_args()


def main() -> None:
    """Punto de entrada principal del script."""

    args = parse_args()

    if args.command == "agregar-cliente":
        client = add_client(args.nombre, args.contacto)
        print(f"Clienta registrada: {client.nombre} (contacto: {client.contacto})")
        return

    if args.command == "agendar":
        appointment = schedule_appointment(args.nombre, args.contacto, args.fecha, args.servicio)
        print(
            "Cita agendada para "
            f"{appointment.client_name} el {appointment.fecha.strftime('%d/%m/%Y %H:%M')} "
            f"({appointment.servicio})."
        )
        return

    if args.command == "listar":
        appointments = list_appointments(show_all=args.todas)
        if not appointments:
            print("No hay citas registradas.")
            return

        for appointment in appointments:
            estado = "(recordatorio enviado)" if appointment.recordatorio_enviado else ""
            print(
                f"- {appointment.client_name}: {appointment.fecha.strftime('%d/%m/%Y %H:%M')} "
                f"para {appointment.servicio} {estado}".strip()
            )
        return

    if args.command == "recordatorios":
        reminders = generate_reminders()
        if not reminders:
            print(
                "No hay citas dentro de las próximas "
                f"{REMINDER_THRESHOLD_HOURS} horas o ya se enviaron los recordatorios."
            )
            return

        for message in reminders:
            print(message)


if __name__ == "__main__":
    main()

