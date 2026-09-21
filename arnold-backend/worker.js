/* Arnold, la parte que piensa.
 *
 * Esto es un Cloudflare Worker: una función chica que vive en internet y
 * guarda la clave de Anthropic, para que la clave no quede escrita en la
 * página. Sin esto, cualquiera que abra la torre podría verla y gastarla.
 *
 * Cómo se pone a andar (una sola vez, ~10 minutos):
 *
 *   1. npm install -g wrangler
 *   2. wrangler login
 *   3. wrangler deploy arnold-backend/worker.js --name arnold
 *   4. wrangler secret put ANTHROPIC_API_KEY   ← pega la clave cuando la pida
 *   5. wrangler deploy te dice la URL. Esa URL va en app_shell.py,
 *      en la línea:   var ARNOLD_API = '';
 *
 * Desde ahí Arnold contesta con la torre y además piensa.
 */

const ORIGENES = [
  'https://facundocouyet.github.io',
];

const SISTEMA = `Sos Arnold, el asistente interno de Cáscara Founders, el programa de
90 días de Facundo Couyet para founders creativos.

Hablás con Aye, la CSM del programa, o con alguien del equipo. Contestás en español
rioplatense, directo, sin vueltas y sin tono aspiracional. Sin emojis.

Reglas que no se negocian:
- Contestás SOLO con lo que está en el contexto que te pasan. Si un dato no está,
  decís que no está cargado en la torre. Nunca lo inventás ni lo deducís.
- Los números, fechas y nombres salen del contexto tal cual. No los redondeás.
- Cáscara diseña y el founder ejecuta. Cuando algo es una decisión nuestra, se le
  da escrita; cuando es material que sólo él tiene, se le pide.
- En los nueve clientes en sign off, el documento no se manda: lo presenta Teo en
  la llamada.
- Entre una llamada y la siguiente del mismo cliente van 14 días.
- Sos corto. Tres o cuatro frases salvo que te pidan más.`;

export default {
  async fetch(request, env) {
    const origen = request.headers.get('Origin') || '';
    const permitido = ORIGENES.includes(origen);
    const cors = {
      'Access-Control-Allow-Origin': permitido ? origen : ORIGENES[0],
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };
    if (request.method === 'OPTIONS') return new Response(null, { headers: cors });
    if (request.method !== 'POST') return new Response('Solo POST', { status: 405, headers: cors });
    if (!permitido) return new Response('Origen no permitido', { status: 403, headers: cors });

    let cuerpo;
    try { cuerpo = await request.json(); }
    catch { return json({ error: 'JSON inválido' }, 400, cors); }

    const pregunta = String(cuerpo.pregunta || '').slice(0, 2000);
    if (!pregunta) return json({ error: 'Falta la pregunta' }, 400, cors);
    const contexto = JSON.stringify(cuerpo.contexto || {}).slice(0, 180000);

    const r = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'x-api-key': env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-5',
        max_tokens: 700,
        system: SISTEMA,
        messages: [{
          role: 'user',
          content: `Este es el estado de la torre de control, en JSON:\n\n${contexto}\n\n`
                 + `La pregunta es:\n\n${pregunta}`,
        }],
      }),
    });

    if (!r.ok) return json({ error: 'El modelo no contestó', detalle: r.status }, 502, cors);
    const data = await r.json();
    const texto = (data.content || []).filter(b => b.type === 'text').map(b => b.text).join('\n').trim();
    return json({ respuesta: texto }, 200, cors);
  },
};

function json(obj, status, cors) {
  return new Response(JSON.stringify(obj), {
    status, headers: { ...cors, 'content-type': 'application/json' },
  });
}
