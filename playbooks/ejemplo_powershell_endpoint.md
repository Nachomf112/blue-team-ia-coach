# Blue Team IA Coach

Playbook: PowerShell sospechoso en un endpoint
----------------------------------------------

1. Aislar temporalmente el equipo de la red si es posible (EDR / VLAN / VPN).
2. Recopilar información del proceso: comando completo, usuario, host, hora de inicio.
3. Extraer hash del fichero asociado (si lo hay) y comprobarlo en VirusTotal / sandbox.
4. Revisar el historial de eventos: PowerShell Operational, Security, Sysmon (si está desplegado).
5. Buscar actividad relacionada en otros hosts (mismo hash, misma IP, mismo usuario).
6. Si confirmas que es malicioso, abrir incidente, bloquear IoC y documentar evidencias.

(Consejo) Copia estos pasos a tu ticket / herramienta de IR y añade evidencias concretas (hashes, IPs, capturas, etc.).
