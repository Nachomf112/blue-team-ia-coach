#!/usr/bin/env python3

"""
Blue Team IA Coach – versión 0.2
CLI para guiar a analistas SOC junior en la respuesta a alertas típicas.
Ahora permite exportar el playbook a un fichero Markdown.
"""

from datetime import datetime
from textwrap import dedent
import os

ALERTS = {
    "1": {
        "name": "PowerShell sospechoso en un endpoint",
        "steps": [
            "Aislar temporalmente el equipo de la red si es posible (EDR / VLAN / VPN).",
            "Recopilar información del proceso: comando completo, usuario, host, hora de inicio.",
            "Extraer hash del fichero asociado (si lo hay) y comprobarlo en VirusTotal / sandbox.",
            "Revisar el historial de eventos: PowerShell Operational, Security, Sysmon (si está desplegado).",
            "Buscar actividad relacionada en otros hosts (mismo hash, misma IP, mismo usuario).",
            "Si confirmas que es malicioso, abrir incidente, bloquear IoC y documentar evidencias.",
        ],
    },
    "2": {
        "name": "Posible phishing (correo sospechoso)",
        "steps": [
            "Pedir al usuario el correo original (no reenviado) o extraerlo del buzón.",
            "Revisar remitente, dominios, enlaces y adjuntos sospechosos.",
            "Analizar cabeceras (Received, SPF, DKIM, DMARC) para ver si hay spoofing.",
            "Abrir los enlaces en un entorno seguro / sandbox, nunca desde el equipo del usuario.",
            "Buscar otros correos iguales en la organización (mismo remitente/asunto).",
            "Si es phishing, bloquear dominios/IP, borrar mensajes similares y concienciar al usuario.",
        ],
    },
    "3": {
        "name": "Fuerza bruta / login anómalo en VPN o SSH",
        "steps": [
            "Identificar el usuario afectado y el origen de los intentos (IP, país, ASN).",
            "Revisar si hubo accesos exitosos después de los intentos fallidos.",
            "Comprobar si la IP de origen es conocida (VPN legítima, proveedor cloud, TOR, etc.).",
            "Forzar cambio de contraseña y revisar uso de MFA para esa cuenta.",
            "Buscar actividad con la misma IP en otros servicios (correo, RDP, paneles web…).",
            "Si hay compromiso, revocar sesiones, tokens y seguir el procedimiento de IR.",
        ],
    },
    "4": {
        "name": "Posible beacon de malware (salida a C2)",
        "steps": [
            "Revisar en el proxy/EDR el patrón de tráfico (intervalos, dominios, rutas).",
            "Resolver el dominio/IP y buscar reputación en fuentes OSINT / CTI.",
            "Comprobar si hay más hosts hablando con el mismo destino.",
            "Capturar tráfico (pcap) si es posible para análisis más profundo.",
            "Aislar el host sospechoso y lanzar escaneos específicos (EDR/AV, YARA, etc.).",
            "Si se confirma C2, seguir el runbook de contención y erradicación de la organización.",
        ],
    },
    "5": {
        "name": "Elevación de privilegios sospechosa en un servidor",
        "steps": [
            "Identificar qué cuenta ha elevado privilegios y desde dónde.",
            "Revisar el historial reciente de esa cuenta (logons, cambios de grupo, etc.).",
            "Comprobar si se han creado cuentas locales o modificaciones en grupos admins.",
            "Revisar eventos de seguridad y Sysmon alrededor de la hora del evento.",
            "Buscar herramientas sospechosas (psexec, mimikatz, frameworks de post-explotación).",
            "Si parece compromiso, seguir el procedimiento de IR y aislar el servidor si aplica.",
        ],
    },
}


def show_menu() -> str:
    print("\n" + "=" * 60)
    print(" Blue Team · IA Coach (versión 0.2)")
    print("=" * 60 + "\n")
    print("Selecciona el tipo de alerta para ver un mini-playbook:\n")

    for key, data in ALERTS.items():
        print(f"{key}. {data['name']}")
    print("\n0. Salir\n")

    choice = input("Elige una opción (0-5): ").strip()
    return choice


def build_playbook_text(alert_key: str) -> str:
    data = ALERTS[alert_key]
    title = data["name"]
    steps = data["steps"]

    header = f"Playbook: {title}"
    sep = "-" * len(header)

    lines = [header, sep, ""]
    for i, step in enumerate(steps, start=1):
        lines.append(f"{i}. {step}")
    lines.append("")
    lines.append(
        "(Consejo) Copia estos pasos a tu ticket / herramienta de IR "
        "y añade evidencias concretas (hashes, IPs, capturas, etc.)."
    )
    return "\n".join(lines)


def maybe_export_to_file(text: str, alert_key: str) -> None:
    answer = input(
        "\n¿Quieres guardar este playbook en un fichero .md? (s/n): "
    ).strip().lower()

    if answer not in ("s", "si", "sí"):
        return

    # Crear carpeta playbooks si no existe
    os.makedirs("playbooks", exist_ok=True)

    # Timestamp legible
    now = datetime.now().strftime("%Y%m%d-%H%M")
    filename = f"playbooks/playbook_{alert_key}_{now}.md"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("# Blue Team IA Coach\n\n")
            f.write(text)
            f.write("\n")
        print(f"\n✅ Playbook guardado en: {filename}")
    except OSError as e:
        print(f"\n[!] No se pudo guardar el fichero: {e}")


def main() -> None:
    while True:
        choice = show_menu()

        if choice == "0":
            print("\nHasta luego. ¡Buen hunting! 👋")
            break

        if choice not in ALERTS:
            print("\n[!] Opción no válida, prueba otra vez.")
            continue

        text = build_playbook_text(choice)
        print("\n" + text)
        maybe_export_to_file(text, choice)


if __name__ == "__main__":
    main()
