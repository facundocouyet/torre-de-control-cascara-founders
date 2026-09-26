---
id: 2026-09-26-la-base-de-la-app-queda-lista
fecha: 2026-09-26
tipo: decision
depto: sistemas
sobre: [app-founders]
quien: [teo]
temas: [supabase, cartas, sesiones, revision]
fuente: WhatsApp de Teo a Facu, 26/9 19:07; sistema/30-mapa-del-cerebro.md
certeza: dicho
estado: vigente
---
# La base de la app queda lista y las cartas entran solo por el sync de GitHub

Teo sumó lo que pedía el mapa del cerebro: `cartas` con `cliente_slug`, `variante_de` y `url` (cada
cliente ve las genéricas y las suyas), los estados de revisión en `asignaciones` (el cliente solo
la manda a revisión, el resto lo cambia el equipo) y `sesiones` con estado y la vista
`proxima_sesion`. Sacó su carga de cartas desde la base: la única vía es `sync_cartas.py`. El
acceso de clientes sale lunes o martes.
