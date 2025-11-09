# Blue Team IA Coach

Blue Team IA Coach es una herramienta en línea de comandos pensada para analistas de ciberseguridad junior.

Ayuda a investigar alertas típicas de Blue Team ofreciendo:

- ✅ Checklists de actuación paso a paso  
- 💻 Comandos recomendados (Linux, herramientas comunes, etc.)  
- 📁 Evidencias que conviene recoger (logs, PCAP, artefactos forenses)  
- 📝 Puntos clave para documentar el incidente

### Alertas soportadas (v1)

- Sospecha de malware en endpoint
- Escaneo de puertos / actividad Nmap sospechosa
- Intento de fuerza bruta (SSH / RDP / Web)

---

## Uso rápido

```bash
python -m coach.main

## Exportar playbook a Markdown

A partir de la versión **0.2**, la herramienta permite guardar el playbook en un fichero `.md`
para documentar mejor el incidente o pegarlo en un ticket del SOC.

1. Ejecuta la herramienta:

   ```bash
   python -m coach.main
