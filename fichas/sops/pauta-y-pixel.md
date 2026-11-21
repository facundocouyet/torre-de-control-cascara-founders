---
nombre: La pauta y el pixel, como en Cáscara
va_con: calendario-lanzamiento
bajada: Cómo armamos la pauta de un lanzamiento: para qué sirve el pixel y cómo se configura, cómo saber de dónde viene cada registro, la estructura de campañas y públicos, y cómo se lee. Con los números reales de La Revolución del Ocio.
cuando: Cuando tenés un evento, un registro o una preventa con fecha y ya hay algo en orgánico que trae gente.
lista_cuando: El pixel marca el registro, cada link tiene su origen y la campaña de registro está corriendo con sus conjuntos.
---

# La pauta y el pixel, como en Cáscara

La pauta no reemplaza al orgánico: lo amplifica. Primero se prueba en orgánico qué pieza y qué ángulo traen gente, y después se le pone plata a eso. Antes de gastar un dólar tiene que estar el pixel midiendo el resultado que te importa, porque sin él Meta optimiza a clics y no a personas que se registran o compran.

## Para qué sirve el pixel

El pixel es un código de Meta que va en tu web. Le avisa a Meta quién la visitó y quién hizo lo que te importa (registrarse, comprar). Sirve para tres cosas:

- **Que Meta busque a la gente correcta.** Si la campaña optimiza al registro, Meta le muestra el anuncio a gente parecida a la que ya se registró. Sin pixel, busca a los que hacen clic, que no es lo mismo.
- **Volver a hablarle a quien casi.** Las visitas que no se registraron quedan como público para retargeting, que suele ser el más barato de los últimos días.
- **Saber cuánto te cuesta cada resultado.** El costo por registro de cada anuncio es lo que te dice qué pausar y a qué ponerle más.

## Los eventos que medimos

- **PageView**, en todas las páginas: cada visita.
- **CompleteRegistration**, solo cuando el registro se guardó: es la conversión de la campaña. Va en la página de gracias, nunca en la landing, porque contaría visitas como registros.
- **Uno propio, opcional**, cuando entran al grupo de WhatsApp o tocan el botón importante de la página de gracias.

En Cáscara usamos un solo pixel por marca, con la página de gracias como evento de conversión, y otro evento en la página de gracias después de agendar una llamada.

## El pixel, paso a paso

1. **Crealo en tu Business Manager.** Administrador de eventos → Conectar orígenes de datos → Web → nombre y URL de tu sitio → instalar el código manualmente. Copiá el ID. Tiene que estar en el mismo Business Manager que tu cuenta publicitaria.
2. **Pegá el código base en todas las páginas**, dentro del head. Con código o Lovable, en el index.html; con Webflow, Framer, WordPress o Wix, en Configuración → Código personalizado → Head.

<pre class="cod">&lt;!-- Meta Pixel Code --&gt;&#10;&lt;script&gt;&#10;!function(f,b,e,v,n,t,s)&#10;{if(f.fbq)return;n=f.fbq=function(){n.callMethod?&#10;n.callMethod.apply(n,arguments):n.queue.push(arguments)};&#10;if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version=&#x27;2.0&#x27;;&#10;n.queue=[];t=b.createElement(e);t.async=!0;&#10;t.src=v;s=b.getElementsByTagName(e)[0];&#10;s.parentNode.insertBefore(t,s)}(window, document,&#x27;script&#x27;,&#10;&#x27;https://connect.facebook.net/en_US/fbevents.js&#x27;);&#10;fbq(&#x27;init&#x27;, &#x27;TU_ID_DE_PIXEL&#x27;);&#10;fbq(&#x27;track&#x27;, &#x27;PageView&#x27;);&#10;&lt;/script&gt;&#10;&lt;!-- End Meta Pixel Code --&gt;</pre>
3. **Marcá el registro en la página de gracias.** Además del código base, va esto. Si el gracias aparece en la misma página del formulario, va en el código que corre cuando el envío salió bien.

<pre class="cod">&lt;script&gt;&#10;  fbq(&#x27;track&#x27;, &#x27;CompleteRegistration&#x27;);&#10;&lt;/script&gt;</pre>
4. **Verificá el dominio.** Configuración del negocio → Seguridad de la marca → Dominios: meta-etiqueta en el head o registro TXT en el DNS. Después, en el Administrador de eventos, dejá CompleteRegistration como evento prioritario.
5. **Probalo antes de pautar.** Extensión Meta Pixel Helper en Chrome, un registro de prueba y, en Administrador de eventos → Probar eventos, tienen que aparecer PageView y CompleteRegistration. Borrá la fila de prueba de tu base.

## De dónde viene cada registro

El formulario guarda una columna «origen» que sale del link. Cada canal tiene su valor, siempre escrito igual: `?origen=ig-bio`, `?origen=ig-historias`, `?origen=manychat`, `?origen=wsp-directo`, `?origen=mail`, `?origen=referido`. En los anuncios, Meta lo completa solo con los parámetros de URL de cada anuncio:

<pre class="cod">origen=meta-{{ad.name}}&amp;utm_source={{site_source_name}}&amp;utm_campaign={{campaign.name}}&amp;utm_term={{adset.name}}&amp;utm_content={{ad.name}}</pre>
Con eso, en tu base ves qué pieza o qué anuncio trajo a cada persona. Para lo que llega sin parámetro, sumá al formulario una pregunta cerrada: «¿Por dónde te enteraste?».

## La estructura que usamos

Dos campañas, con objetivos distintos.

**La de registro** es la que llena el evento o la preventa. Objetivo Clientes potenciales, conversión en el sitio web, evento Completar registro. El presupuesto va en cada conjunto, así controlás cuánto gasta cada público.

<table class="tabla-carta"><thead><tr><th>Conjunto</th><th>Público</th><th>Para qué</th></tr></thead><tbody><tr><td>Interacción 365 días</td><td>Quienes interactuaron con tus cuentas de Instagram en el último año</td><td>Tu audiencia más fácil</td></tr><tr><td>Video 50%, 30 días</td><td>Quienes vieron al menos la mitad de los reels de la campaña</td><td>Los que ya conocen el mensaje</td></tr><tr><td>Similar</td><td>Público similar armado con tu base de registrados y clientes (al menos 100 personas)</td><td>Gente nueva parecida a la que ya te compró</td></tr><tr><td>Visitas sin registro, 30 días</td><td>Quienes entraron a la landing y no se registraron (público del pixel)</td><td>Retargeting, desde que el pixel junta visitas</td></tr></tbody></table>

**La de seguidores (Follow Me Ad)** es para gente que no te conoce: un video tuyo contando quién sos, qué hacés y qué resolvés, para que te siga. No trae registros esa semana; agranda la audiencia que después se vuelve tibia. Va aparte y con poco presupuesto.

## Los anuncios

- **Se suben de cero, no se potencia el orgánico.** Descargás el video y lo cargás como anuncio nuevo. Así controlás el texto, el botón y los primeros segundos, ponés los parámetros de URL y los comentarios de la pauta no se mezclan con tu orgánico. Además, si el posteo pide «comentá una palabra», en el anuncio la gente comenta en vez de hacer clic.
- **El texto pesa más que la estética.** Lo que hace que alguien se registre es entender en dos líneas qué es, para quién, cuándo y que es gratis o cuánto sale.
- **Dos o tres anuncios por conjunto.** La pieza orgánica que mejor rindió, una versión con otro gancho en los primeros tres segundos y una imagen fija con la fecha. Meta concentra el gasto en los que mejor andan.

## Cómo se lee

- **Cada dos días, no antes.** Mirá el costo por registro de cada anuncio y de cada conjunto.
- **El que cuesta el doble que el resto, se pausa**, y su plata se reparte entre los otros.
- **La frecuencia avisa el cansancio.** Cuando un conjunto pasa de 3 y el CTR baja, el público ya vio demasiado el anuncio: cambiá el creativo o mové la plata a un público nuevo.
- **Avisale a quien vende cuando prendés o subís la pauta**, así está listo para contestar rápido cuando llega el pico de registros.

## El ejemplo: La Revolución del Ocio

Campaña de registro de Cáscara, del 9 al 15 de noviembre de 2026. Tres campañas con dos conjuntos cada una, todas optimizando al registro en la web, excluyendo a alumnos y clientes vigentes.

<table class="tabla-carta"><thead><tr><th>Campaña</th><th>Gasto</th><th>Registros</th><th>Costo por registro</th></tr></thead><tbody><tr><td>Similar (lookalike de 10.176 registrados a eventos)</td><td>USD 136</td><td>300</td><td>USD 0,45</td></tr><tr><td>Interacción 365 días</td><td>USD 182</td><td>398</td><td>USD 0,46</td></tr><tr><td>Video 50%, 30 días</td><td>USD 78</td><td>148</td><td>USD 0,53</td></tr><tr><td><b>Total</b></td><td><b>USD 396</b></td><td><b>846</b></td><td><b>USD 0,47</b></td></tr></tbody></table>

- **El mejor anuncio** trajo el 37% de los registros a USD 0,37, y USD 0,32 en el público similar. Era una pieza de preguntas frecuentes, sin producción: lo que decía, no cómo se veía.
- **El peor** costaba USD 1,22 por registro, más del doble del promedio: se pausó.
- **El retargeting se cansó en una semana.** La frecuencia pasó de 3 y el CTR cayó entre 14% y 54%, y el costo por registro empezó a subir. Por eso se suman creativos nuevos cada semana.
- **La pauta y el orgánico juntos.** En esa semana, lo que entró por anuncios fue más de la mitad de todos los registros. El resto vino de dos o tres piezas orgánicas por día con palabra clave en ManyChat, las historias de los founders y el grupo de WhatsApp.

## La versión chica, para tu primer lanzamiento

Con una audiencia más chica no vas a pagar USD 0,47 por registro: tomalo como referencia, no como meta. Una estructura que alcanza:

- **Una campaña de registro con tres conjuntos:** interacción 365 días, video 50% y un público nuevo (o similar, si tu base pasa de 100 personas). De 5 a 7 dólares por día cada uno.
- **El cuarto conjunto, desde el tercer día:** visitas sin registro.
- **Tres anuncios:** la pieza que mejor rindió, otra versión con otro gancho y una imagen con la fecha.
- **Una pieza orgánica por día con palabra clave**, que es lo que la pauta después amplifica.

## Checklist

- Pixel creado, código base en todas las páginas y CompleteRegistration en el gracias.
- Probado con Pixel Helper y en Probar eventos.
- Dominio verificado y evento prioritario elegido.
- Cada link con su origen y los parámetros de URL en cada anuncio.
- Campaña de registro con sus conjuntos, optimizando a Completar registro.
- Anuncios subidos de cero.
- Lectura cada dos días: pausar el que cuesta el doble y renovar cuando la frecuencia pasa de 3.
