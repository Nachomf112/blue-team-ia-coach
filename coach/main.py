#!/usr/bin/env python3
"""
Blue Team IA Coach
Asistente en terminal para responder a distintos tipos de alertas de seguridad.
"""

from textwrap import dedent


ALERT_PLAYBOOKS = {
    "1": {
        "name": "PowerShell sospechoso en un endpoint",
        "steps": [
            "1. Aislar temporalmente el equipo de la red si es posible (EDR / VLAN / VPN).",
            "2. Recopilar información del proceso: comando completo, usuario, host, hora de inicio.",
            "3. Extraer hash del fichero asociado (si lo hay) y comprobarlo en VirusTotal / sandbox.",
            "4. Revisar el historial de eventos: PowerShell Operational, Security, Sysmon (si está desplegado).",
            "5. Buscar actividad relacionada en otros hosts (mismo hash, misma IP, mismo usuario).",
            "6. Si confirmas que es malicioso, abrir incidente, bloquear IoC y documentar evidencias.",
        ],
    },
    "2": {
        "name": "Posible phishing (correo sospechoso)",
        "steps": [
            "1. Pedir copia del correo en formato original (eml) o cabeceras completas.",
            "2. Analizar dominio del remitente, enlaces y adjuntos en herramientas de reputación.",
            "3. Comprobar si otros usuarios han recibido el mismo correo (búsqueda en el servidor).",
            "4. Bloquear el remitente / dominio y añadir reglas en el gateway de correo.",
            "5. Enviar comunicación interna avisando del phishing y cómo identificarlo.",
            "6. Documentar el caso en el registro de incidentes.",
        ],
    },
    "3": {
        "name": "Fuerza bruta / login anómalo en VPN o SSH",
        "steps": [
            "1. Identificar origen de los intentos: IP, geolocalización, ASN.",
            "2. Revisar si ha habido autenticaciones exitosas del mismo origen o usuario.",
            "3. Forzar cambio de contraseña al usuario afectado y revisar MFA.",
            "4. Bloquear temporalmente la IP / rango en el firewall o WAF si procede.",
            "5. Buscar actividad lateral desde las sesiones exitosas (si las hay).",
            "6. Registrar el incidente y ajustar umbrales de alertas si es necesario.",
        ],
    },
    "4": {
        "name": "Posible beacon de malware (salida a C2)",
        "steps": [
            "1. Identificar el host afectado, proceso y destino (IP/DOMINIO/PUERTO).",
            "2. Aislar el host de la red para evitar más comunicación.",
            "3. Extraer muestras (ficheros, memoria, registros) para análisis forense.",
            "4. Bloquear el destino en proxy, firewall y DNS.",
            "5. Buscar en logs si hay más hosts contactando al mismo destino.",
            "6. Crear ticket de incidente mayor, seguir playbook de contención y erradicación.",
        ],
    },
    "5": {
        "name": "Elevación de privilegios sospechosa en un servidor",
        "steps": [
            "1. Identificar cuenta, host y momento exacto de la elevación.",
            "2. Revisar qué acciones se realizaron tras obtener privilegios elevados.",
            "3. Validar si la actividad estaba planificada (cambio, mantenimiento, etc.).",
            "4. Si no estaba prevista, revocar sesiones, resetear credenciales y revisar GPO / sudoers.",
            "5. Buscar otras elevaciones similares en el mismo periodo de tiempo.",
            "6. Documentar el incidente y refinar controles (MFA, segmentación, registros).",
        ],
    },
}


def mostrar_banner() -> None:
    print(
        dedent(
            """
            ============================================
                Blue Team · IA Coach (versión 0.1)
            ============================================
            Selecciona el tipo de alerta para ver
            un mini-playbook con los siguientes pasos.
            """
        )
    )


def pedir_opcion() -> str:
    print("Tipos de alerta disponibles:\n")
    for key, data in ALERT_PLAYBOOKS.items():
        print(f"  {key}. {data['name']}")
    print("\n  0. Salir\n")

    while True:
        opcion = input("Elige una opción (0-5): ").strip()
        if opcion in ALERT_PLAYBOOKS or opcion == "0":
            return opcion
        print("❌ Opción no válida, prueba de nuevo.\n")


def mostrar_playbook(opcion: str) -> None:
    data = ALERT_PLAYBOOKS[opcion]
    print("\n" + "=" * 60)
    print(f"Playbook para: {data['name']}")
    print("=" * 60 + "\n")

    for linea in data["steps"]:
        print(linea)
    print("\n(Consejo) Copia estos pasos a tu ticket / herramienta de IR.\n")


def main() -> None:
    mostrar_banner()
    while True:
        opcion = pedir_opcion()
        if opcion == "0":
            print("\nHasta luego, ¡buen hunting! 🕵️‍♂️")
            break
        mostrar_playbook(opcion)


if __name__ == "__main__":
    main()
