# Sistemas · automatización y agentes

**Dueño:** Facu, con Teo en la app. **Qué es:** todo lo que hace que Cáscara corra con menos manos:
los agentes programados, la torre de control, la app de clientes, el cerebro en n8n y este registro.

## Lo vigente

- **Los agentes que corren:** "el día y el pulso" (L–V 9:00), la revisión semanal (viernes), el
  cierre del día (L–V 20:00). El detalle está en `sistema/20-tareas-programadas.md`.
- **La torre** se genera desde este repo; Facu hace el `git push` a mano.
- **La app y el cerebro:** Lovable + Supabase para la app, n8n para el cerebro que junta Fathom,
  Slack y Notion. El mapa está en `sistema/30-mapa-del-cerebro.md`.
- **Este registro** es la memoria escrita que después importa la base de datos del cerebro.
- Las claves de API no se pegan nunca en el chat ni en el repo: van solo en n8n y en los secrets de
  GitHub.

## Fuentes

`sistema/` en el Project, `CLAUDE.md` del repo, las tareas programadas.
