# -*- coding: utf-8 -*-
import json,os
B=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # la raíz del repo
J=open(B+'/contenido/app-data.json',encoding='utf-8').read()

CSS = r'''
/* ============================================================
   CÁSCARA FOUNDERS · app
   La piel es de F3: tinta, papel cálido, etiqueta encajonada, radio 0.
   La respiración es de Cáscara: escala grande, aire, columnas anchas.
   Monocromo. El rojo de F3 está racionado: solo lo frenado y lo vencido.
   ============================================================ */
:root{
  --tinta:#171717; --tinta-deep:#0A0A0C; --tinta-warm:#1A1815;
  --papel:#ECEAE4; --papel2:#FBFAF8; --gris:#6A6A66; --gris2:#8E8B85;
  --tiza:#DBD7D2; --rojo:#FE1414;
  --disp:"Helvetica Now Display","Helvetica Neue",Helvetica,Arial,sans-serif;
  --edit:"Redaction 10","Redaction","Exposure","Times New Roman",Times,serif;
  --rail:252px; --gut:56px; --col:1080px;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --tinta:#ECEAE4; --tinta-deep:#F7F5F1; --tinta-warm:#E4E1DA;
  --papel:#121211; --papel2:#1A1A18; --gris:#93908A; --gris2:#6E6B66;
  --tiza:#2C2C2A; --rojo:#FF4D4D;
}}
:root[data-theme="dark"]{
  --tinta:#ECEAE4; --tinta-deep:#F7F5F1; --tinta-warm:#E4E1DA;
  --papel:#121211; --papel2:#1A1A18; --gris:#93908A; --gris2:#6E6B66;
  --tiza:#2C2C2A; --rojo:#FF4D4D;
}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{height:100%}
body{margin:0;background:var(--papel);color:var(--tinta);font-family:var(--disp);
  font-size:20px;line-height:1.5;-webkit-font-smoothing:antialiased;
  font-feature-settings:"kern" 1}
/* grano finísimo de papel, como en los informes */
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:1;opacity:.026;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='120' height='120'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3'/></filter><rect width='120' height='120' filter='url(%23n)'/></svg>")}
button{font:inherit;color:inherit;background:none;border:0;padding:0;cursor:pointer;text-align:left}
a{color:inherit;text-decoration:none}
:focus-visible{outline:1px solid var(--tinta);outline-offset:3px}
.num{font-weight:800;letter-spacing:-.05em;font-variant-numeric:tabular-nums}
.it{font-family:var(--edit);font-style:italic}

/* etiqueta encajonada — el motivo de F3, uno por vista */
.caja{display:inline-block;border:1px solid var(--gris2);padding:6px 13px;
  font-size:10.5px;letter-spacing:.24em;text-transform:uppercase;color:var(--gris)}
.et{font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--gris)}

/* ---------- riel de navegación (escritorio) ---------- */
.riel{position:fixed;left:0;top:0;bottom:0;width:var(--rail);background:#0A0A0C;
  color:#FBFAF8;display:flex;flex-direction:column;padding:26px 0 26px;z-index:30;
  transition:width .18s ease}
.riel *{color:inherit}
.riel .marca{padding:0 22px 28px;border-bottom:1px solid rgba(236,234,228,.14);
  display:flex;align-items:center;gap:14px}
/* el sello: la caja de radio 0 con la F de Founders, el mismo motivo que la etiqueta de los documentos */
.riel .marca .sello-f{flex:0 0 auto;width:34px;height:34px;border:1.5px solid var(--papel2);
  display:flex;align-items:center;justify-content:center;font-size:19px;font-weight:800;
  letter-spacing:-.04em;line-height:1;padding-bottom:1px}
.riel .marca .txt{min-width:0}
.riel .marca b{display:block;font-size:17px;font-weight:800;letter-spacing:-.03em;line-height:1.1;
  white-space:nowrap}
.riel .marca .txt span{display:block;font-size:9px;letter-spacing:.24em;text-transform:uppercase;
  color:rgba(236,234,228,.42);margin-top:6px;white-space:nowrap}
.riel nav{display:flex;flex-direction:column;padding-top:8px}
.riel nav button{display:grid;grid-template-columns:30px 1fr;gap:12px;align-items:baseline;
  padding:15px 26px;color:rgba(236,234,228,.5);transition:color .12s}
.riel nav button .n{font-size:10.5px;letter-spacing:.14em;font-variant-numeric:tabular-nums}
.riel nav button .t{font-size:16px;letter-spacing:-.015em}
.riel nav button:hover{color:#FBFAF8}
.riel nav button[aria-selected="true"]{color:#FBFAF8}
.riel nav button[aria-selected="true"] .t{font-weight:700}
.riel nav button[aria-selected="true"]::before{content:"";position:absolute;left:0;width:3px;
  height:22px;background:#FBFAF8;margin-top:2px}
.riel nav button{position:relative}
.riel .pie{margin-top:auto;padding:22px 26px 0;border-top:1px solid rgba(236,234,228,.14)}
.riel .pie .f{font-size:10.5px;letter-spacing:.2em;color:rgba(236,234,228,.42)}
.riel .pie .s{font-family:var(--edit);font-style:italic;font-size:14px;
  color:rgba(236,234,228,.42);margin-top:8px;line-height:1.4}

/* plegar el riel */
.plegar{position:absolute;top:24px;right:-13px;width:26px;height:26px;background:#0A0A0C;
  border:1px solid #2A2A30;display:flex;align-items:center;justify-content:center;z-index:2}
.plegar i{width:7px;height:7px;border-left:1.5px solid #FBFAF8;border-bottom:1.5px solid #FBFAF8;
  transform:rotate(45deg);margin-left:3px;transition:transform .18s}
.plegar:hover{background:#17171A}
body.plegado .riel{width:58px}
body.plegado .riel .marca .txt,body.plegado .riel .pie,body.plegado .riel nav button .t{display:none}
body.plegado .riel .marca{padding:0 0 22px;justify-content:center;gap:0}
/* plegado, el botón baja para dejar respirar el sello */
body.plegado .plegar{top:auto;bottom:22px;right:-13px}
body.plegado .riel nav button{grid-template-columns:1fr;justify-items:center;padding:16px 0}
body.plegado .plegar i{transform:rotate(-135deg);margin-left:0;margin-right:3px}
/* al esconder la barra, el contenido queda centrado en la pantalla entera:
   el riel flota encima y el lienzo lleva el mismo aire de los dos lados */
body.plegado main{margin-left:0;padding:0 58px}
body.plegado .hoja{max-width:calc(var(--col) + 80px)}
@media (max-width:720px){.plegar{display:none} body.plegado .riel{width:auto}
  body.plegado .riel nav button .t{display:block} body.plegado main{margin-left:0;padding:0}}

/* ---------- lienzo ---------- */
main{margin-left:var(--rail);min-height:100%;position:relative;z-index:2;transition:margin-left .18s ease}
.hoja{max-width:var(--col);margin:0 auto;padding:0 var(--gut) 96px}
.encab{padding:56px 0 0;display:flex;justify-content:space-between;align-items:flex-start;gap:30px}
.sello{font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--gris2);
  text-align:right;line-height:1.7;white-space:nowrap}
h1.tit{font-size:clamp(40px,4.4vw,64px);font-weight:800;letter-spacing:-.038em;line-height:1;
  margin:26px 0 0;text-wrap:balance;max-width:22ch}
.entrada{font-size:22px;line-height:1.5;color:var(--gris);max-width:52ch;margin:20px 0 0}

/* banda de cifras: hairlines, sin cajas */
.banda{display:grid;grid-template-columns:repeat(4,1fr);margin-top:46px;
  border-top:1px solid var(--tinta);border-bottom:1px solid var(--tiza)}
.banda > *{padding:22px 26px 20px;border-left:1px solid var(--tiza);text-align:left}
.banda > *:first-child{border-left:0;padding-left:0}
.banda b{display:block;font-size:46px;line-height:.92;font-weight:800;letter-spacing:-.055em;
  font-variant-numeric:tabular-nums}
.banda span{display:block;font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--gris);margin-top:12px}
.banda button:hover b{color:var(--gris)}
.banda b.alerta{color:var(--rojo)}

h2.bl{font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--gris);
  font-weight:400;margin:64px 0 0;padding-bottom:14px;border-bottom:1px solid var(--tinta);
  display:flex;justify-content:space-between;align-items:baseline;gap:16px}
h2.bl em{font-style:italic;font-family:var(--edit);text-transform:none;letter-spacing:0;
  font-size:15px;color:var(--gris2)}

/* ---------- filas de cliente ---------- */
.fila{display:grid;grid-template-columns:34px minmax(0,1fr) 130px 88px 150px 18px;
  gap:24px;align-items:center;width:100%;padding:20px 0;border-bottom:1px solid var(--tiza)}
.fila:hover{background:var(--papel2)}
.fila .idx{font-size:11px;color:var(--gris2);font-variant-numeric:tabular-nums}
.fila .nm{display:block;font-size:23px;font-weight:700;letter-spacing:-.026em;line-height:1.15}
.fila .sub{display:block;font-size:16.5px;color:var(--gris);margin-top:5px;line-height:1.4;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.fila .dia{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--gris)}
.fila .dia b{font-size:19px;letter-spacing:-.04em;display:block;color:var(--tinta);
  font-variant-numeric:tabular-nums;margin-bottom:3px}
.fila .dia.vencido b{color:var(--rojo)}
.fila .hc{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--gris);text-align:right}
.fila .hc b{display:block;font-size:30px;letter-spacing:-.04em;color:var(--tinta);
  font-variant-numeric:tabular-nums;font-weight:800;margin-bottom:3px}
.fila .fl{width:9px;height:9px;border-right:1px solid var(--gris2);
  border-top:1px solid var(--gris2);transform:rotate(45deg)}

/* ritmo: tinta, no semáforo. Lleno / hueco / rojo racionado */
.ritmo{display:inline-flex;align-items:center;gap:9px;font-size:10.5px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--gris);white-space:nowrap}
.ritmo i{width:10px;height:10px;flex:0 0 auto;border:1px solid var(--tinta)}
.ritmo.verde i{background:var(--tinta)}
.ritmo.amarillo i{background:transparent}
.ritmo.rojo{color:var(--rojo)}
.ritmo.rojo i{background:var(--rojo);border-color:var(--rojo)}

/* navegación del detalle: volver, anterior y siguiente */
.dtnav{display:flex;align-items:center;justify-content:space-between;gap:20px;
  padding:22px 0 0;margin-bottom:6px}
.dtnav button{display:inline-flex;align-items:center;gap:11px;font-size:10.5px;
  letter-spacing:.18em;text-transform:uppercase;color:var(--gris);padding:9px 0}
.dtnav button:hover{color:var(--tinta)}
.dtnav button[disabled]{opacity:.3;cursor:default}
.dtnav .lados{display:flex;align-items:center;gap:26px;min-width:0}
.dtnav .nom{font-size:13px;letter-spacing:-.01em;text-transform:none;color:var(--tinta);
  max-width:22ch;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.dtnav .pos{font-size:10.5px;letter-spacing:.16em;color:var(--gris2);font-variant-numeric:tabular-nums}
.pf{width:9px;height:9px;flex:0 0 auto;border-right:1.5px solid currentColor;
  border-top:1.5px solid currentColor;transform:rotate(45deg)}
.pf.izq{transform:rotate(-135deg)}
@media (max-width:720px){
  .dtnav{padding-top:14px;flex-wrap:wrap;gap:10px}
  .dtnav .nom{display:none}
  .dtnav .lados{gap:16px}
}

/* ---------- detalle ---------- */
.dt{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:0 64px;align-items:start}
.dt-l{min-width:0}
.dt h1{font-size:clamp(38px,4.2vw,58px);font-weight:800;letter-spacing:-.04em;line-height:1;
  margin:24px 0 0;text-wrap:balance}
.dt .py{font-size:21px;color:var(--gris);margin:16px 0 0;max-width:46ch}
.dt .sellos{display:flex;gap:10px;margin-top:26px;flex-wrap:wrap}
.bloque{padding:28px 0;border-bottom:1px solid var(--tiza)}
.bloque p{margin:12px 0 0;font-size:22px;line-height:1.52;max-width:54ch}
.bloque .grande{font-size:clamp(24px,2.4vw,32px);font-weight:700;letter-spacing:-.028em;
  line-height:1.22;max-width:26ch;margin-top:14px}

/* lateral del detalle: el handicap y los días */
.aside{position:sticky;top:0;padding-top:120px}
.hcard{border-top:1px solid var(--tinta);padding-top:22px}
.hcard .t{display:flex;align-items:baseline;gap:12px}
.hcard .t b{font-size:66px;line-height:.85}
.hcard .t span{font-size:17px;color:var(--gris)}
.hcard .tr{font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--gris);margin-top:12px}
.ejes{margin-top:26px}
.ej{display:grid;grid-template-columns:1fr auto;gap:10px 14px;align-items:center;
  padding:11px 0;border-top:1px solid var(--tiza)}
.ej .n{font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--gris)}
.ej.f .n{color:var(--tinta);font-weight:700}
.ej .v{font-size:17px;color:var(--tinta);font-variant-numeric:tabular-nums;font-weight:700}
.ej .b{grid-column:1/-1;height:7px;background:var(--tiza);position:relative}
.ej .b i{display:block;height:100%;background:var(--tinta)}
.ej.f .b i{background:var(--rojo)}
.ej.e .n{color:var(--tinta)}
.hcard .sube{font-family:var(--edit);font-style:italic;font-size:16px;line-height:1.5;
  color:var(--gris);margin-top:20px;border-top:1px solid var(--tiza);padding-top:16px}

/* promedio de la camada por eje, en la vista del programa */
.ejeprom{display:grid;grid-template-columns:210px 64px minmax(0,1fr);gap:16px;align-items:baseline;
  border-top:1px solid var(--tiza);padding:18px 0}
.ejeprom .n{font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--tinta);font-weight:700}
.ejeprom .v{font-size:22px;color:var(--tinta);font-weight:700;font-variant-numeric:tabular-nums}
.ejeprom .bb{grid-column:1/-1;height:7px;background:var(--tiza);margin-top:4px}
.ejeprom .bb i{display:block;height:100%;background:var(--tinta)}
.ejeprom .q{font-size:18.5px;color:var(--gris);line-height:1.48}
@media (max-width:720px){
  .ejeprom{grid-template-columns:1fr auto;gap:6px 14px}
  .ejeprom .q{grid-column:1/-1}
}

/* la regla de los 90 días */
.dias{border-top:1px solid var(--tinta);padding-top:22px;margin-top:34px}
.dias .g{display:flex;align-items:baseline;gap:10px}
.dias .g b{font-size:52px;line-height:.9}
.dias .g span{font-size:15px;color:var(--gris)}
.dias .g b.vencido{color:var(--rojo)}
.dias .regla{height:6px;background:var(--tiza);margin-top:16px;position:relative;overflow:hidden}
.dias .regla i{display:block;height:100%;background:var(--tinta)}
.dias .regla i.vencido{background:var(--rojo)}
.dias .marcas{display:flex;justify-content:space-between;margin-top:8px;
  font-size:9.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--gris2)}
.dias .nota{font-family:var(--edit);font-style:italic;font-size:16px;color:var(--gris);margin-top:14px}

.check{margin:14px 0 0;padding:0;list-style:none}
.check li{display:grid;grid-template-columns:16px 1fr;gap:14px;padding:14px 0;
  border-top:1px solid var(--tiza);font-size:20px;line-height:1.45}
.check li::before{content:"";width:11px;height:11px;border:1px solid var(--gris2);margin-top:7px}
.check li b{display:block;font-size:10px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--gris2);font-weight:400;margin-bottom:3px}

.boton{display:inline-flex;align-items:center;gap:14px;border:1px solid var(--tinta);
  padding:15px 22px;font-size:11px;letter-spacing:.18em;text-transform:uppercase;margin-top:30px}
.boton:hover{background:var(--tinta);color:var(--papel)}
.boton.tinta{background:var(--tinta);color:var(--papel)}
.boton.tinta:hover{background:transparent;color:var(--tinta)}
.boton .fl{width:8px;height:8px;border-right:1px solid currentColor;border-top:1px solid currentColor;
  transform:rotate(45deg)}

/* ---------- filtros y buscador ---------- */
.barra{display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin-top:34px}
.busca{display:flex;align-items:center;gap:12px;border-bottom:1px solid var(--tinta);
  flex:1;min-width:240px}
.busca input{flex:1;font:inherit;font-size:20px;border:0;background:none;color:inherit;
  padding:11px 0;min-width:0}
.busca input::placeholder{color:var(--gris2)}
.filtros{display:flex;gap:0;flex-wrap:wrap;border:1px solid var(--tiza)}
.filtros button{font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;padding:11px 15px;
  color:var(--gris);border-right:1px solid var(--tiza)}
.filtros button:last-child{border-right:0}
.filtros button[aria-pressed="true"]{background:var(--tinta);color:var(--papel)}

/* ---------- acordeón ---------- */
.ac{border-bottom:1px solid var(--tiza)}
.ac summary{list-style:none;display:grid;grid-template-columns:44px minmax(0,1fr) auto 20px;
  gap:20px;align-items:baseline;padding:24px 0;cursor:pointer}
.ac summary::-webkit-details-marker{display:none}
.ac summary:hover{background:var(--papel2)}
.ac .an{font-size:11px;color:var(--gris2);font-variant-numeric:tabular-nums}
.ac .at small{display:block;font-size:10px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--gris2);margin-bottom:7px}
.ac .at b{display:block;font-size:24px;font-weight:700;letter-spacing:-.026em;line-height:1.2}
.ac .c{font-size:20px;color:var(--gris);font-variant-numeric:tabular-nums;font-weight:800;letter-spacing:-.04em}
.ac .mas{width:14px;height:14px;position:relative;justify-self:end;margin-top:8px}
.ac .mas::before,.ac .mas::after{content:"";position:absolute;background:var(--gris2)}
.ac .mas::before{left:0;right:0;top:6px;height:1px}
.ac .mas::after{top:0;bottom:0;left:6px;width:1px;transition:transform .16s}
.ac[open] .mas::after{transform:scaleY(0)}
.ac .cuerpo{padding:0 0 30px 64px;max-width:62ch}
.ac .cuerpo p{margin:0 0 15px;font-size:21px;line-height:1.55;color:var(--gris)}
.ac .cuerpo p b{color:var(--tinta)}
.ac .cuerpo ul{margin:12px 0 0;padding-left:20px;color:var(--gris)}
.ac .cuerpo li{margin-bottom:9px;font-size:20px}
.ac .cuerpo .pieza{padding:16px 0;border-top:1px solid var(--tiza)}
.ac .cuerpo .pieza .ph{display:flex;justify-content:space-between;gap:16px;align-items:baseline}
.ac .cuerpo .pieza b{font-size:19px;color:var(--tinta);letter-spacing:-.02em}
.ac .cuerpo .pieza p{margin:7px 0 0;font-size:19px}

.pieza .pq{font-family:var(--edit);font-style:italic;color:var(--gris2);margin-top:8px}
.capas{margin-top:14px}
.capas summary{list-style:none;cursor:pointer;font-size:10.5px;letter-spacing:.18em;
  text-transform:uppercase;color:var(--gris);padding:10px 0;border-top:1px solid var(--tiza);
  white-space:nowrap;display:block}
.capas summary::-webkit-details-marker{display:none}
.capas summary:hover{color:var(--tinta)}
.capa{margin-top:14px}
.capa .ct{display:block;font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--gris2);margin-bottom:8px}
.capa ol{margin:0;padding-left:22px}
.capa li{font-size:18.5px;line-height:1.5;color:var(--gris);margin-bottom:8px}
.est{font-size:9.5px;letter-spacing:.16em;text-transform:uppercase;padding:4px 9px;
  border:1px solid currentColor;white-space:nowrap;color:var(--gris)}
.est.falta{color:var(--rojo)}

.duenos{display:grid;grid-template-columns:repeat(3,1fr);gap:0 40px;margin-top:10px}
.duen{border-top:1px solid var(--tinta);padding:20px 0 26px}
.duen .dh{display:flex;justify-content:space-between;align-items:baseline;gap:12px}
.duen .dh b{font-size:22px;font-weight:700;letter-spacing:-.024em}
.duen .dh span{font-size:24px;color:var(--gris);font-weight:800;letter-spacing:-.04em;
  font-variant-numeric:tabular-nums}
.duen ul{margin:16px 0 0;padding:0;list-style:none}
.duen li{font-size:18px;line-height:1.42;margin-bottom:14px;color:var(--gris)}
.duen li b{display:block;font-size:9.5px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--gris2);font-weight:400;margin-bottom:3px}
.duen .mas{font-family:var(--edit);font-style:italic;font-size:14.5px;color:var(--gris2)}

.vacio{padding:60px 0;font-family:var(--edit);font-style:italic;font-size:19px;color:var(--gris2)}
.vista{display:none}.vista.on{display:block}
.topmov{display:none}

/* ================= TABLET ================= */
@media (max-width:1080px){
  :root{--rail:196px;--gut:38px}
  .fila{grid-template-columns:28px minmax(0,1fr) 110px 74px 130px 16px;gap:16px}
  .fila .nm{font-size:21px}
  .dt{grid-template-columns:1fr;gap:0}
  .aside{position:static;padding-top:38px}
  .duenos{grid-template-columns:repeat(2,1fr);gap:0 30px}
}
/* ================= CELULAR ================= */
@media (max-width:720px){
  :root{--gut:20px;--tabh:58px}
  body{font-size:17px}
  .riel{left:0;right:0;top:auto;bottom:0;width:auto;height:calc(var(--tabh) + env(safe-area-inset-bottom,0px));
    padding:0 0 env(safe-area-inset-bottom,0px);flex-direction:row}
  .riel .marca,.riel .pie{display:none}
  .riel nav{flex-direction:row;flex:1;padding:0}
  .riel nav button{flex:1;grid-template-columns:1fr;gap:0;justify-items:center;
    align-content:center;padding:0;height:var(--tabh)}
  .riel nav button .n{display:none}
  .riel nav button .t{font-size:11px;letter-spacing:.14em;text-transform:uppercase}
  .riel nav button[aria-selected="true"]::before{left:50%;transform:translateX(-50%);top:0;
    width:26px;height:2px;margin:0}
  main{margin-left:0;padding-bottom:calc(var(--tabh) + env(safe-area-inset-bottom,0px))}
  .topmov{display:flex;position:sticky;top:0;z-index:15;background:var(--papel);
    border-bottom:1px solid var(--tiza);align-items:center;gap:12px;
    padding:13px var(--gut);min-height:52px}
  .topmov b{font-size:15px;font-weight:800;letter-spacing:-.025em;flex:1;
    white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .topmov .f{font-size:9.5px;letter-spacing:.18em;color:var(--gris2)}
  .topmov .atras{width:34px;height:34px;margin-left:-8px;display:none;align-items:center;
    justify-content:center}
  .topmov .atras i{width:9px;height:9px;border-left:1.5px solid var(--tinta);
    border-bottom:1.5px solid var(--tinta);transform:rotate(45deg);display:block}
  body.detalle .topmov .atras{display:flex}
  .encab{padding-top:30px;flex-direction:column;gap:14px}
  .sello{display:none}
  h1.tit{font-size:clamp(30px,8vw,40px);margin-top:16px}
  .entrada{font-size:17px;margin-top:14px}
  .banda{grid-template-columns:1fr 1fr;margin-top:30px;border-bottom:0}
  .banda > *{padding:18px 0 16px;border-left:0;border-bottom:1px solid var(--tiza)}
  .banda > *:nth-child(even){padding-left:20px;border-left:1px solid var(--tiza)}
  .banda b{font-size:34px}
  h2.bl{margin-top:44px;flex-direction:column;gap:6px;align-items:flex-start}
  .fila{grid-template-columns:minmax(0,1fr) auto;gap:6px 14px;padding:16px 0}
  .fila .idx{display:none}
  .fila .nm{font-size:19px}
  .fila .hc{grid-row:1;grid-column:2;justify-self:end;font-size:9.5px}
  .fila .hc b{display:inline;font-size:22px;margin:0}
  .fila .sub{grid-column:1/-1}
  .fila .dia{grid-column:1;font-size:9.5px}
  .fila .dia b{display:inline;font-size:14px;margin:0}
  .fila .ritmo{grid-column:2;justify-self:end;font-size:9.5px}
  .fila .fl{display:none}
  .duenos{grid-template-columns:1fr;gap:0}
  .ac summary{grid-template-columns:36px minmax(0,1fr) auto 18px;gap:14px;padding:18px 0}
  .ac .at b{font-size:19px}
  .ac .cuerpo{padding-left:0}
  .ac .cuerpo p,.ac .cuerpo li{font-size:16.5px}
  .bloque p{font-size:17.5px}
  .bloque .grande{font-size:22px}
  .hcard .t b{font-size:52px}
  .dias .g b{font-size:40px}
  .check li{font-size:16.5px}
  .boton{width:100%;justify-content:space-between}
}
@media print{.riel,.topmov,.boton{display:none}main{margin:0}body::before{display:none}}
'''

JS = r'''
var D=__DATA__;
var $=function(s){return document.querySelector(s)};
var esc=function(s){var d=document.createElement('div');d.textContent=s==null?'':s;return d.innerHTML};
var SEC=[['hoy','Hoy'],['clientes','Clientes'],['programa','Programa'],['material','Material']];
var TIT={hoy:'Hoy',clientes:'Los clientes',programa:'El programa',material:'El material'};
var C=D.clientes, con=C.filter(function(c){return c.h});
var prom=Math.round(con.reduce(function(a,c){return a+c.h.g},0)/con.length);
var frenados=con.filter(function(c){return c.h.ri==='rojo'});
var cierre=C.filter(function(c){return c.modo==='cierre'});
var vencidos=C.filter(function(c){return c.dia&&c.dia>90});
var promDias=Math.round(C.filter(function(c){return c.dia}).reduce(function(a,c){return a+c.dia},0)/C.filter(function(c){return c.dia}).length);
var filtro=null,busca='',tab='hoy';
var ORD=[];   // el orden que se está viendo, para moverse con las flechas

function ritmo(h){return '<span class="ritmo '+h.ri+'"><i></i>'+esc(h.rt)+'</span>'}
function encab(et,tit,entrada,sello){
  return '<div class="encab"><div><span class="caja">'+esc(et)+'</span></div>'+
    (sello?'<div class="sello">'+sello+'</div>':'')+'</div>'+
    '<h1 class="tit">'+esc(tit)+'</h1>'+(entrada?'<p class="entrada">'+esc(entrada)+'</p>':'');
}
function fila(c,i){
  var h=c.h, venc=c.dia&&c.dia>90;
  return '<button class="fila" onclick="abrir(\''+c.slug+'\')">'+
   '<span class="idx num">'+('0'+(i+1)).slice(-2)+'</span>'+
   '<span><span class="nm">'+esc(c.nombre)+'</span><span class="sub">'+esc(c.cuello)+'</span></span>'+
   '<span class="dia'+(venc?' vencido':'')+'">'+(c.dia?'<b>'+c.dia+'</b> de 90 días':'<b>—</b>sin fecha')+'</span>'+
   '<span class="hc"><b class="num">'+(h?h.g:'—')+'</b>handicap</span>'+
   (h?ritmo(h):'<span class="ritmo"><i style="border-style:dotted"></i>sin dato</span>')+
   '<span class="fl"></span></button>';
}

/* ---------------- HOY ---------------- */
function vHoy(){
  var at=con.slice().sort(function(a,b){return a.h.g-b.h.g}).slice(0,6);
  var h='<div class="hoja">'+encab('Cáscara Founders · '+D.fecha,
    'La camada, de menor a mayor handicap',
    'Arriba está quien más atención necesita. El día de cada uno dice dónde está parado en los noventa.',
    'Torre de control<br>'+C.length+' clientes<br>'+D.fecha);
  h+='<div class="banda">'+
    '<button onclick="ir(\'clientes\')"><b class="num">'+C.length+'</b><span>Clientes</span></button>'+
    '<div><b class="num">'+prom+'</b><span>Handicap promedio</span></div>'+
    '<button onclick="ir(\'clientes\',\'vencido\')"><b class="num'+(vencidos.length?' alerta':'')+'">'+vencidos.length+'</b><span>Pasaron los 90 días</span></button>'+
    '<button onclick="ir(\'clientes\',\'rojo\')"><b class="num'+(frenados.length?' alerta':'')+'">'+frenados.length+'</b><span>Frenados</span></button>'+
  '</div>';
  h+='<h2 class="bl">Necesita atención <em>los seis handicaps más bajos</em></h2><div>';
  at.forEach(function(c,i){h+=fila(c,i)});
  h+='</div><a class="boton" onclick="ir(\'clientes\')">Ver los '+C.length+'<span class="fl"></span></a>';
  h+='<h2 class="bl">Le toca a <em>los accionables de septiembre de nuestro lado</em></h2><div class="duenos">';
  D.tareas.forEach(function(t){
    h+='<div class="duen"><div class="dh"><b>'+esc(t.d)+'</b><span class="num">'+t.items.length+'</span></div><ul>';
    t.items.slice(0,3).forEach(function(i){h+='<li><b>'+esc(i.c)+'</b>'+esc(i.t)+'</li>'});
    h+='</ul>'+(t.items.length>3?'<span class="mas">y '+(t.items.length-3)+' más</span>':'')+
      '<div><button class="boton" style="margin-top:16px;padding:10px 15px;font-size:10px" onclick="verDueno(\''+esc(t.d)+'\')">Ver todos<span class="fl"></span></button></div></div>';});
  h+='</div></div>';
  $('#v-hoy').innerHTML=h;
}
function verDueno(d){
  var t=null; D.tareas.forEach(function(x){if(x.d===d)t=x}); if(!t)return;
  var h='<div class="hoja">'+encab('Accionables de Cáscara · septiembre',d,
    t.items.length+' accionables de su lado, sacados de las fichas de los clientes.','');
  h+='<ul class="check" style="margin-top:40px">';
  t.items.forEach(function(i){h+='<li><span><b>'+esc(i.c)+'</b>'+esc(i.t)+'</span></li>'});
  h+='</ul></div>';
  $('#v-detalle').innerHTML=h; verDetalle(d);
}

/* ---------------- CLIENTES ---------------- */
var F=[['todos','Todos'],['Conseguir','Conseguir'],['Sostener','Sostener'],['Entregar','Entregar'],
       ['cierre','En cierre'],['vencido','Pasaron 90'],['rojo','Frenados']];
function vClientes(){
  var h='<div class="hoja">'+encab('La camada','Los '+C.length+' clientes','',
    'Ordenados por handicap<br>día promedio: '+promDias);
  h+='<div class="barra"><span class="busca"><input id="q" type="search" placeholder="Buscar cliente o proyecto" value="'+esc(busca)+'" aria-label="Buscar"></span><span class="filtros">';
  F.forEach(function(f){h+='<button data-f="'+f[0]+'" aria-pressed="'+((filtro||'todos')===f[0])+'">'+f[1]+'</button>'});
  h+='</span></div><div id="lista" style="margin-top:30px;border-top:1px solid var(--tinta)"></div>'+
     '<p class="vacio" id="vacio" hidden>Nada con ese filtro.</p></div>';
  $('#v-clientes').innerHTML=h;
  $('#q').addEventListener('input',function(){busca=this.value;pinta()});
  $('#v-clientes').querySelectorAll('.filtros button').forEach(function(b){
    b.addEventListener('click',function(){
      filtro=b.dataset.f==='todos'?null:b.dataset.f;
      $('#v-clientes').querySelectorAll('.filtros button').forEach(function(o){o.setAttribute('aria-pressed',String(o===b))});
      pinta();});});
  pinta();
}
function pinta(){
  var t=busca.trim().toLowerCase();
  var l=C.filter(function(c){
    if(filtro==='cierre'&&c.modo!=='cierre')return false;
    if(filtro==='rojo'&&(!c.h||c.h.ri!=='rojo'))return false;
    if(filtro==='vencido'&&!(c.dia&&c.dia>90))return false;
    if(filtro&&['Conseguir','Sostener','Entregar'].indexOf(filtro)>-1&&c.ori!==filtro)return false;
    if(t&&(c.nombre+' '+c.proyecto).toLowerCase().indexOf(t)<0)return false;
    return true;});
  l.sort(function(a,b){return (a.h?a.h.g:999)-(b.h?b.h.g:999)});
  ORD=l.map(function(c){return c.slug});
  $('#lista').innerHTML=l.map(fila).join('');
  $('#vacio').hidden=l.length>0;
}

/* ---------------- DETALLE ---------------- */
function nombreDe(sl){var n=null;C.forEach(function(x){if(x.slug===sl)n=x.nombre});return n}
function saltar(d){
  var a=location.hash.indexOf('#c/')===0?location.hash.slice(3):null;
  var i=ORD.indexOf(a);
  if(i<0)return; var j=i+d; if(j<0||j>=ORD.length)return; abrir(ORD[j]);
}
function abrir(slug){
  var c=null; C.forEach(function(x){if(x.slug===slug)c=x}); if(!c)return;
  var venc=c.dia&&c.dia>90, pct=c.dia?Math.min(100,Math.round(c.dia/90*100)):0;
  if(ORD.indexOf(slug)<0) ORD=C.slice().sort(function(a,b){return (a.h?a.h.g:999)-(b.h?b.h.g:999)}).map(function(x){return x.slug});
  var pos=ORD.indexOf(slug);
  var ant=pos>0?nombreDe(ORD[pos-1]):null, sig=pos>-1&&pos<ORD.length-1?nombreDe(ORD[pos+1]):null;
  var h='<div class="hoja">'+
    '<div class="dtnav">'+
      '<button onclick="ir(\'clientes\')"><span class="pf izq"></span>Volver a clientes</button>'+
      '<div class="lados">'+
        '<button '+(ant?'onclick="saltar(-1)"':'disabled')+'><span class="pf izq"></span>'+
          '<span class="nom">'+(ant?esc(ant):'')+'</span></button>'+
        '<span class="pos">'+(pos+1)+' / '+ORD.length+'</span>'+
        '<button '+(sig?'onclick="saltar(1)"':'disabled')+'><span class="nom">'+(sig?esc(sig):'')+'</span>'+
          '<span class="pf"></span></button>'+
      '</div>'+
    '</div>'+
    '<div class="dt"><div class="dt-l">'+
    '<div class="encab"><div><span class="caja">'+(c.modo==='cierre'?'Informe de cierre':'Radiografía y roadmap')+'</span></div>'+
    '<div class="sello">'+esc(c.ori)+'<br>'+(c.h?esc(c.h.tr):'')+'</div></div>'+
    '<h1>'+esc(c.nombre)+'</h1><p class="py">'+esc(c.proyecto)+'</p>';
  h+='<div class="bloque"><span class="et">El cuello de botella</span><p class="grande">'+esc(c.cuello)+'</p></div>';
  if(c.etapa) h+='<div class="bloque"><span class="et">En qué etapa está</span><p>'+esc(c.etapa)+'</p></div>';
  if(c.h) h+='<div class="bloque"><span class="et">Por dónde se trabaja</span><p>'+esc(c.h.nota)+'</p></div>';
  if(c.metrica) h+='<div class="bloque"><span class="et">La métrica que importa</span><p>'+esc(c.metrica)+'</p></div>';
  if(c.ct&&c.ct.length) h+='<div class="bloque"><span class="et">Septiembre · lo hace él o ella</span><ul class="check">'+
    c.ct.map(function(x){return '<li><span>'+esc(x)+'</span></li>'}).join('')+'</ul></div>';
  if(c.cas&&c.cas.length) h+='<div class="bloque"><span class="et">Septiembre · lo hace Cáscara</span><ul class="check">'+
    c.cas.map(function(x){return '<li><span>'+esc(x)+'</span></li>'}).join('')+'</ul></div>';
  if(c.abierto) h+='<div class="bloque"><span class="et">Sin definir</span><p>'+esc(c.abierto)+'</p></div>';
  if(c.doc) h+='<a class="boton tinta" href="clientes/'+esc(c.doc)+'">Abrir el documento completo<span class="fl"></span></a>';
  h+='<p class="vacio" style="padding:26px 0 0;font-size:15px">Última llamada tomada: '+esc(c.ultima)+'</p>';
  h+='</div><aside class="aside">';
  if(c.h){
    h+='<div class="hcard"><span class="et">Handicap general</span><div class="t"><b class="num">'+c.h.g+'</b><span>de 100</span></div>'+
      '<div class="tr">'+esc(c.h.tr)+' · '+esc(c.h.rt)+'</div><div class="ejes">';
    for(var i=0;i<5;i++){
      h+='<div class="ej'+(i===c.h.flo[0]?' f':(c.h.flo.indexOf(i)>-1?' e':''))+'"><span class="n">'+esc(D.ejes[i])+'</span>'+
         '<span class="v num">'+c.h.e1[i]+'</span>'+
         '<span class="b"><i style="width:'+c.h.e1[i]+'%"></i></span></div>';}
    h+='</div>'+(c.h.sube?'<p class="sube">La más baja es '+esc(D.ejes[c.h.flo[0]]).toLowerCase()+'. '+esc(c.h.sube)+'</p>':'')+'</div>';
  }
  h+='<div class="dias"><span class="et">Con nosotros</span><div class="g"><b class="num'+(venc?' vencido':'')+'">'+
     (c.dia||'—')+'</b><span>'+(c.dia?'días':'sin fecha cargada')+'</span></div>'+
     '<div class="regla"><i class="'+(venc?'vencido':'')+'" style="width:'+pct+'%"></i></div>'+
     '<div class="marcas"><span>día 1</span><span>día 90</span></div>'+
     '<p class="nota">'+(c.dia?(venc?'Pasó los noventa días: por eso el tramo es de cierre.':'Está en el día '+c.dia+' de los noventa.'):'Falta cargar el START en Cuentas.')+
     (c.fuente==='llamada'?' Contado desde la primera llamada registrada, porque el START no está cargado.':'')+'</p></div>';
  h+='</aside></div></div>';
  $('#v-detalle').innerHTML=h; verDetalle(c.nombre); location.hash='#c/'+slug;
}
function verDetalle(t){
  document.querySelectorAll('.vista').forEach(function(v){v.classList.remove('on')});
  $('#v-detalle').classList.add('on'); $('#tmov').textContent=t;
  document.body.classList.add('detalle'); window.scrollTo(0,0);
}

/* ---------------- PROGRAMA ---------------- */
function ac(n,pre,tit,cuenta,cuerpo){
  return '<details class="ac"><summary><span class="an num">'+(n||'')+'</span>'+
    '<span class="at">'+(pre?'<small>'+esc(pre)+'</small>':'')+'<b>'+esc(tit)+'</b></span>'+
    '<span class="c">'+(cuenta!=null?cuenta:'')+'</span><span class="mas"></span></summary>'+
    '<div class="cuerpo">'+cuerpo+'</div></details>';
}
function capas(i){
  function lista(t,xs){ return (xs&&xs.length)?'<div class="capa"><span class="ct">'+t+'</span><ol>'+
    xs.map(function(x){return '<li>'+esc(x)+'</li>'}).join('')+'</ol></div>':''; }
  var h=lista('Pasos',i.p)+lista('Qué completar',i.cc)+lista('Qué herramientas',i.hh);
  return h?'<details class="capas"><summary>Ver el módulo completo</summary>'+h+'</details>':'';
}
function vPrograma(){
  var h='<div class="hoja">'+encab('El programa','Noventa días, diez uno a uno y trece semanas de grupales','',
    'Cáscara diseña<br>el founder ejecuta');
  h+='<h2 class="bl">El recorrido <em>'+D.proceso.length+' etapas, en el orden real</em></h2><div>';
  D.proceso.forEach(function(p){h+=ac(p.n,p.c,p.t,null,'<p>'+esc(p.x)+'</p>')});
  h+='</div><h2 class="bl">Las orientaciones <em>terminado el mes uno se elige una sola</em></h2><div>';
  D.orientaciones.forEach(function(o){
    var n=C.filter(function(c){return c.ori===o.n}).length;
    h+=ac('','lo lidera '+o.l,o.n,n,'<p>'+esc(o.x)+'</p><ul>'+o.m.map(function(m){return '<li>'+esc(m)+'</li>'}).join('')+'</ul>');});
  h+='</div><h2 class="bl">El handicap <em>cinco habilidades del 1 al 100; el general es el promedio</em></h2><div>';
  D.ejes_def.forEach(function(x,i){
    var p=Math.round(con.reduce(function(a,c){return a+c.h.e1[i]},0)/con.length);
    h+='<div class="ejeprom"><span class="n">'+esc(x.n)+'</span>'+
      '<span class="v num">'+p+'</span>'+
      '<span class="q">'+esc(x.q)+'</span>'+
      '<span class="bb"><i style="width:'+p+'%"></i></span></div>';});
  h+='</div><h2 class="bl">Las grupales</h2><div>';
  D.grupales.forEach(function(g){h+=ac('',g.c,g.n,null,'<p>'+esc(g.x)+'</p>')});
  h+='</div><h2 class="bl">Los mentores <em>qué traerle y qué no</em></h2><div>';
  D.mentores.forEach(function(m){h+=ac('',m.r,m.n,null,'<p><b>Sí:</b> '+esc(m.si)+'</p><p><b>No:</b> '+esc(m.no)+'</p>')});
  h+='</div><a class="boton" href="programa.html">Versión larga, para compartir<span class="fl"></span></a></div>';
  $('#v-programa').innerHTML=h;
}

/* ---------------- MATERIAL ---------------- */
function vMaterial(){
  var tot=D.modulos.reduce(function(a,m){return a+m.items.length},0);
  var h='<div class="hoja">'+encab('La biblioteca','Todo lo que está escrito','',
    'La oferta, los documentos<br>los contratos y los procesos');
  h+='<h2 class="bl">Las familias</h2><div>';
  D.bloques.forEach(function(b){
    var cu=''; b.piezas.forEach(function(p){
      cu+='<div class="pieza"><div class="ph"><b>'+esc(p.t)+'</b>'+
        (p.e?'<span class="est'+(p.e==='falta escribir'?' falta':'')+'">'+esc(p.e)+'</span>':'')+'</div>'+
        '<p>'+esc(p.q)+'</p>'+(p.u?'<a class="boton" style="margin-top:14px;padding:10px 15px;font-size:10px" href="'+esc(p.u)+'">Abrir<span class="fl"></span></a>':'')+'</div>';});
    h+=ac('','',b.n,b.piezas.length,cu);});
  var nmod=D.modulos.reduce(function(a,m){return a+m.items.length},0);
  h+='</div><h2 class="bl">Los módulos <em>'+nmod+', cada uno con sus pasos, qué completar y qué herramientas</em></h2><div>';
  D.modulos.forEach(function(m){
    var cu = m.porque?'<p>'+esc(m.porque)+'</p>':'';
    m.items.forEach(function(i){
      cu+='<div class="pieza"><div class="ph"><b>'+esc(i.t)+'</b>'+
        (i.e?'<span class="est'+(i.e==='falta'?' falta':'')+'">'+esc(i.e)+'</span>':'')+'</div><p>'+esc(i.x)+'</p>'+
        (i.q?'<p class="pq">'+esc(i.q)+'</p>':'')+capas(i)+'</div>';});
    h+=ac('',m.c,m.c,m.items.length,cu);});
  h+='</div><h2 class="bl">Decisiones tomadas <em>'+D.decisiones.length+'</em></h2><div>';
  D.decisiones.forEach(function(d,i){h+=ac(('0'+(i+1)).slice(-2),'',d.t,null,'<p>'+esc(d.x)+'</p>')});
  h+='</div><h2 class="bl">Lo que falta decidir o escribir <em>'+D.falta.length+'</em></h2><ul class="check">';
  D.falta.forEach(function(f){h+='<li><span>'+esc(f)+'</span></li>'});
  h+='</ul><a class="boton" href="materiales.html">Versión larga<span class="fl"></span></a></div>';
  $('#v-material').innerHTML=h;
}

/* ---------------- router ---------------- */
function ir(t,f){
  tab=t;
  if(t==='clientes'){filtro=(f&&f!=='todos')?f:null;vClientes();}
  document.querySelectorAll('.vista').forEach(function(v){v.classList.remove('on')});
  $('#v-'+t).classList.add('on');
  document.querySelectorAll('.riel nav button').forEach(function(b){b.setAttribute('aria-selected',String(b.dataset.t===t))});
  $('#tmov').textContent=TIT[t]; document.body.classList.remove('detalle');
  window.scrollTo(0,0);
  if(location.hash.indexOf('#c/')===0) history.replaceState(null,'','#'+t); else location.hash='#'+t;
}
document.querySelectorAll('.riel nav button').forEach(function(b){
  b.addEventListener('click',function(){ir(b.dataset.t)})});
$('#atras').addEventListener('click',function(){ir(tab)});
(function(){
  var b=$('#plegar');
  try{ if(localStorage.getItem('cf-riel')==='1') document.body.classList.add('plegado'); }catch(e){}
  b.addEventListener('click',function(){
    var p=document.body.classList.toggle('plegado');
    b.setAttribute('aria-label', p?'Mostrar el menú':'Esconder el menú');
    b.setAttribute('title', p?'Mostrar el menú':'Esconder el menú');
    try{ localStorage.setItem('cf-riel', p?'1':'0'); }catch(e){}
  });
})();
window.addEventListener('hashchange',function(){
  var hs=location.hash.slice(1);
  if(hs.indexOf('c/')===0){ if('#'+hs!==location.hash) return; abrir(hs.slice(2)); return; }
  if(document.body.classList.contains('detalle')) ir(TIT[hs]?hs:tab);});
/* teclado: flechas para moverse entre clientes, escape para volver */
document.addEventListener('keydown',function(e){
  if(!document.body.classList.contains('detalle')) return;
  var t=e.target.tagName; if(t==='INPUT'||t==='TEXTAREA') return;
  if(e.key==='ArrowRight'){e.preventDefault();saltar(1)}
  else if(e.key==='ArrowLeft'){e.preventDefault();saltar(-1)}
  else if(e.key==='Escape'){e.preventDefault();ir(tab)}});
$('#fmov').textContent=D.fecha;
vHoy();vClientes();vPrograma();vMaterial();
if(location.hash.indexOf('#c/')===0) abrir(location.hash.slice(3));
else if(location.hash&&TIT[location.hash.slice(1)]) ir(location.hash.slice(1));
'''

NAV="".join(
 '<button role="tab" data-t="%s" aria-selected="%s"><span class="n num">%s</span><span class="t">%s</span></button>'
 % (k, "true" if i==0 else "false", "0%d"%(i+1), n)
 for i,(k,n) in enumerate([('hoy','Hoy'),('clientes','Clientes'),('programa','Programa'),('material','Material')]))

BODY = f'''<aside class="riel">
  <div class="marca"><span class="sello-f" aria-hidden="true">F</span><span class="txt"><b>Cáscara Founders</b><span>Torre de control</span></span></div>
  <nav role="tablist" aria-label="Secciones">{NAV}</nav>
  <button class="plegar" id="plegar" aria-label="Esconder el menú" title="Esconder el menú"><i></i></button>
  <div class="pie"><div class="f">{ "12 SEP 2026" }</div>
    <div class="s">Se actualiza solo todas las mañanas con lo que salió de las llamadas del día anterior.</div></div>
</aside>

<main>
  <div class="topmov">
    <button class="atras" id="atras" aria-label="Volver"><i></i></button>
    <b id="tmov">Hoy</b><span class="f" id="fmov"></span>
  </div>
  <div class="vista on" id="v-hoy"></div>
  <div class="vista" id="v-clientes"></div>
  <div class="vista" id="v-programa"></div>
  <div class="vista" id="v-material"></div>
  <div class="vista" id="v-detalle"></div>
</main>'''

HTML = ('<!doctype html>\n<html lang="es"><head>\n<meta charset="utf-8">\n'
 '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
 '<title>Cáscara Founders</title>\n'
 '<meta name="description" content="Torre de control de Cáscara Founders: la camada, el programa y la biblioteca.">\n'
 '<meta name="theme-color" content="#0A0A0C">\n'
 '<meta name="apple-mobile-web-app-capable" content="yes">\n'
 '<meta name="apple-mobile-web-app-title" content="Founders">\n'
 '<style>' + CSS + '</style>\n</head><body>\n' + BODY +
 '\n<script>\n' + JS.replace('__DATA__', J) + '\n</script>\n</body></html>')
open(B+'/index.html','w',encoding='utf-8').write(HTML)
print("app:",len(HTML))
