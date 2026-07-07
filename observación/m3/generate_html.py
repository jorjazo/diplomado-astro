#!/usr/bin/env python3
"""Generate all HTML study files for Observación Módulo 3, clases 1–3."""
from __future__ import annotations

import pathlib
import re

BASE = pathlib.Path(__file__).resolve().parent
OUT = BASE / "html"
REF_AP = BASE.parent / "m2" / "html" / "m2c1-apuntes.html"
COURSE = "Instrumentación y Observación"

# Correcciones documentadas de la transcripción automática
TRANSCRIPTION_CORRECTIONS = [
    '"difracción" en lentes refractores → refracción (la curvatura del vidrio desvía la luz, no la difracción)',
    '"zing", "SIG", "sync" → seeing (turbulencia atmosférica que desparrama la imagen)',
    '"Hull" / telescopio espacial Hull → Hubble',
    '"Verapoint", "ver a Rubí" → Vera Rubin (LSST)',
    '"Verarubin" → Vera Rubin',
    '"Churchill" y otros nombres mal reconocidos se contrastan con diapositivas cuando aparecen',
]

_ref = REF_AP.read_text(encoding="utf-8")
_css_m = re.search(r"<style>(.*?)</style>", _ref, re.S)
CSS_AP = _css_m.group(1) if _css_m else ""

CSS_EX = """<style>
:root{--bg:#070a12;--ink:#ece8df;--muted:#9aa6bb;--line:#26324a;--red:#e0382e;--red-soft:#f06a5e;--gold:#d9a74a;--cyan:#6fc7d6;--ok:#5fd07e;--bad:#f06a5e}
*{box-sizing:border-box}
body{margin:0;color:var(--ink);background:var(--bg);font-family:"Spectral",Georgia,serif;font-size:18px;line-height:1.7;
  background-image:radial-gradient(1.3px 1.3px at 20% 30%,rgba(255,255,255,.4),transparent),radial-gradient(1.1px 1.1px at 75% 18%,rgba(255,255,255,.3),transparent),radial-gradient(1200px 700px at 80% -8%,#16203a 0%,transparent 60%),linear-gradient(180deg,#070a12,#0a0f1b);background-attachment:fixed}
.wrap{max-width:820px;margin:0 auto;padding:24px 22px 80px}
nav{font-size:.9rem;margin-bottom:18px}nav a{color:var(--muted);text-decoration:none}nav a:hover{color:var(--red-soft)}
.kick{font-family:"Fraunces",serif;font-size:.78rem;letter-spacing:.2em;text-transform:uppercase;color:var(--red-soft);font-weight:600}
h1{font-family:"Fraunces",serif;font-size:clamp(1.8rem,5vw,2.6rem);margin:.15em 0 .5em;font-weight:600;letter-spacing:-.01em}
.intro{color:var(--muted);font-size:.96rem;margin-bottom:24px}
fieldset{border:1px solid var(--line);border-radius:14px;margin:18px 0;padding:16px 20px;background:#0b112099}
legend{font-family:"Fraunces",serif;font-weight:600;color:#fff;padding:0 10px;font-size:1.04rem}
.qopen{border:1px dashed #36425c;border-radius:14px;margin:18px 0;padding:16px 20px;background:#0a0f1b80}
.qopen p.q{font-family:"Fraunces",serif;color:#fff;font-weight:600;margin:.1em 0 .4em}
label.opt{display:block;padding:8px 12px;border:1px solid transparent;border-radius:9px;margin:5px 0;cursor:pointer;transition:.12s}
label.opt:hover{background:#10203a}
label.opt input{accent-color:var(--red);margin-right:10px}
.btn{background:var(--red);color:#fff;border:none;border-radius:10px;padding:11px 20px;font-family:"Fraunces",serif;font-weight:600;font-size:.96rem;cursor:pointer;margin-top:8px}
.btn:hover{background:var(--red-soft)}
.score{font-family:"Fraunces",serif;font-weight:600;margin-top:14px;font-size:1.05rem}
.fb{font-size:.86rem;margin-top:6px;color:var(--muted)}
fieldset.correct{border-color:var(--ok)}fieldset.wrong{border-color:var(--bad)}
details{margin-top:10px;border-top:1px solid var(--line);padding-top:10px}
summary{cursor:pointer;color:var(--gold);font-family:"Fraunces",serif;font-weight:600}
.answer{margin-top:10px;color:#d7e0ef;font-size:.96rem}
.tag{display:inline-block;font-size:.68rem;letter-spacing:.14em;text-transform:uppercase;color:var(--cyan);font-family:"Fraunces",serif;font-weight:600;border:1px solid var(--line);border-radius:999px;padding:2px 10px;margin-bottom:6px}
footer{margin-top:40px;border-top:1px solid var(--line);padding-top:18px;color:var(--muted);font-size:.85rem}
</style>"""

HEAD_LINKS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,600'
    '&family=Spectral:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">'
)

GRADE_JS = """<script>
function gradeQuiz(){
  var form=document.getElementById('quiz');
  var ans=form.dataset.answers.split(',');var ok=0;
  ans.forEach(function(a,i){
    var fs=form.querySelector('fieldset[data-q="'+(i+1)+'"]');
    var sel=form.querySelector('input[name="q'+(i+1)+'"]:checked');
    fs.classList.remove('correct','wrong');
    var fb=fs.querySelector('.fb');if(fb)fb.hidden=false;
    if(sel&&sel.value===a){ok++;fs.classList.add('correct');}else{fs.classList.add('wrong');}
  });
  var el=document.getElementById('score');el.hidden=false;
  el.textContent='Alternativas correctas: '+ok+' / '+ans.length;
  el.style.color = ok===ans.length ? 'var(--ok)' : 'var(--gold)';
}
</script>"""


def head_ap(title: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
{HEAD_LINKS}
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<style>{CSS_AP}</style>
</head>
<body>
"""


TAIL_AP = """
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
<script>
document.addEventListener("DOMContentLoaded",function(){
  if(window.renderMathInElement) renderMathInElement(document.body,{delimiters:[{left:"$$",right:"$$",display:true},{left:"\\\\[",right:"\\\\]",display:true},{left:"\\\\(",right:"\\\\)",display:false}],throwOnError:false});
  document.querySelectorAll(".katex-block").forEach(function(el){katex.render(el.dataset.tex,el,{displayMode:true,throwOnError:false});});
  document.querySelectorAll(".katex-inline").forEach(function(el){katex.render(el.dataset.tex,el,{displayMode:false,throwOnError:false});});
%s
});
</script>
</body>
</html>
"""


def fig(cx: str, n: int, cap: str, alt: str = "") -> str:
    return f"""<figure>
<img src="{cx}/assets/slide-{n:02d}.jpg" alt="{alt or cap}">
<figcaption><span class="cap">Diapositiva {n}</span>{cap}</figcaption>
</figure>"""


def exams_section(cx: str, items: list[tuple[int, str]]) -> str:
    lis = "\n".join(
        f'    <li><a href="{cx}-examen-{i:02d}.html">Examen {i:02d}<small>{sub}</small></a></li>'
        for i, sub in items
    )
    return f"""<section id="examenes">
<div class="shead"><span class="num">✓</span><div>
<h2>Exámenes de práctica</h2>
<p>10 exámenes de 5 preguntas (3 alternativas autocorregibles + 2 escritas).</p>
</div></div>
<ol class="examlist">
{lis}
</ol>
</section>"""


def disc_footer() -> str:
    items = "".join(f"<li>{c}</li>" for c in TRANSCRIPTION_CORRECTIONS)
    return f"""<p class="disc"><strong>Nota sobre transcripción:</strong> el audio fue transcrito automáticamente. Correcciones aplicadas en estos apuntes:
<ul>{items}</ul></p>"""


def mc_block(n: int, legend: str, opts: list[str], fb: str) -> str:
    letters = "abcd"
    lines = [f'  <fieldset data-q="{n}"><legend>{n}. {legend}</legend>']
    for i, opt in enumerate(opts):
        lines.append(f'    <label class="opt"><input type="radio" name="q{n}" value="{letters[i]}">{opt}</label>')
    lines.append(f'    <p class="fb" hidden>{fb}</p>')
    lines.append("  </fieldset>")
    return "\n".join(lines)


def open_block(n: int, q: str, ans: str) -> str:
    return f"""<div class="qopen"><span class="tag">Respuesta escrita</span>
  <p class="q">{n}. {q}</p>
  <details><summary>Ver respuesta propuesta</summary>
    <div class="answer">{ans}</div>
  </details>
</div>"""


def render_exam(cx: str, nn: int, title: str, cls: int, mc, opens, answers: list[str]) -> str:
    ap = f"{cx}-apuntes.html"
    mc_html = "\n".join(mc_block(i + 1, m[0], m[1], m[2]) for i, m in enumerate(mc))
    open_html = "\n".join(open_block(i + 4, o[0], o[1]) for i, o in enumerate(opens))
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Examen {nn:02d} — {cx} · {title}</title>
{HEAD_LINKS}
{CSS_EX}
</head>
<body>
<main class="wrap">
<nav><a href="{ap}#examenes">← Apuntes (exámenes)</a> · <a href="index.html">Índice del módulo</a></nav>
<span class="kick">{COURSE} · Módulo III · Clase {cls}</span>
<h1>Examen {nn:02d} — {title}</h1>
<p class="intro">3 preguntas de alternativas (autocorregibles) + 2 de respuesta escrita.</p>

<form id="quiz" data-answers="{','.join(answers)}">
{mc_html}
  <button type="button" class="btn" onclick="gradeQuiz()">Corregir alternativas</button>
  <p class="score" id="score" hidden></p>
</form>

{open_html}

<footer>Examen de práctica · <a href="{ap}#examenes" style="color:var(--red-soft)">Volver a apuntes</a></footer>
</main>
{GRADE_JS}
</body>
</html>
"""


WIDGETS_C1 = r"""
  function airyCalc(){
    var lam=+document.getElementById('airy-lam').value*1e-9;
    var D=+document.getElementById('airy-d').value;
    var theta=1.22*lam/D;
    document.getElementById('airy-out').innerHTML='θ ≈ <b>'+(theta*206265).toFixed(3)+'</b> arcsec';
  }
  var al=document.getElementById('airy-lam'),ad=document.getElementById('airy-d');
  if(al){al.oninput=airyCalc;ad.oninput=airyCalc;airyCalc();}
  function fluxCalc(){
    var d=+document.getElementById('flux-d').value;
    document.getElementById('flux-out').innerHTML='F ∝ 1/d² → al doble de distancia: <b>'+(1/4).toFixed(3)+'</b>× el flujo';
  }
  var fd=document.getElementById('flux-d'); if(fd){fd.oninput=fluxCalc;fluxCalc();}
"""

WIDGETS_C2 = r"""
  function photonCalc(){
    var lam=+document.getElementById('ph-lam').value*1e-9;
    var h=6.626e-34,c=299792458;
    var E=h*c/lam, ev=1.602e-19;
    document.getElementById('ph-out').innerHTML='E ≈ <b>'+(E/ev).toFixed(3)+'</b> eV · λ = <b>'+(lam*1e9).toFixed(0)+'</b> nm';
  }
  var pl=document.getElementById('ph-lam'); if(pl){pl.oninput=photonCalc;photonCalc();}
  function bitsCalc(){
    var b=+document.getElementById('bits-n').value;
    document.getElementById('bits-out').innerHTML='Máximo ADU: <b>'+(Math.pow(2,b)-1)+'</b> niveles ('+b+' bits)';
  }
  var bn=document.getElementById('bits-n'); if(bn){bn.oninput=bitsCalc;bitsCalc();}
"""

WIDGETS_C3 = r"""
  function radioRes(){
    var lam=+document.getElementById('rad-lam').value;
    var D=+document.getElementById('rad-d').value;
    var theta=1.22*lam/D;
    document.getElementById('rad-out').innerHTML='θ ≈ <b>'+(theta*206265).toFixed(2)+'</b> arcsec (λ='+lam+' m, D='+D+' m)';
  }
  var rl=document.getElementById('rad-lam'),rd=document.getElementById('rad-d');
  if(rl){rl.oninput=radioRes;rd.oninput=radioRes;radioRes();}
  function nuCalc(){
    var f=+document.getElementById('nu-f').value*1e6;
    var c=299792458;
    document.getElementById('nu-out').innerHTML='λ = c/ν ≈ <b>'+(c/f).toFixed(3)+'</b> m ('+(c/f*100).toFixed(1)+' cm)';
  }
  var nf=document.getElementById('nu-f'); if(nf){nf.oninput=nuCalc;nuCalc();}
"""


def build_m3c1_apuntes() -> str:
    e = exams_section("m3c1", [
        (1, "Refractores y reflectores"), (2, "Área colectora"), (3, "Óptica activa"),
        (4, "Espejos segmentados"), (5, "Vera Rubin"), (6, "Límite de difracción"),
        (7, "Seeing atmosférico"), (8, "Óptica adaptativa"), (9, "Monturas y espejos"),
        (10, "Integrador clase 1"),
    ])
    body = f"""
<main class="wrap">
<nav class="top"><a href="index.html">← Módulo III — índice</a></nav>
<div class="hero">
<span class="kick">{COURSE} · Módulo III · Clase 1</span>
<h1>El <em>telescopio</em> como recolector de luz</h1>
<p class="sub">Del refractor de Galileo a espejos segmentados de 10 m, óptica activa y adaptativa: el aparato que concentra la luz antes del detector.</p>
<div class="meta">
<span><b>Docente:</b> César Fuentes</span>
<span><b>Tema:</b> Telescopios ópticos e infrarrojos</span>
</div>
</div>
<p class="lead"><span class="drop">E</span>sta clase se centra en el <span class="hl">instrumento que dobla y concentra la luz</span>, no en los detectores (clase 2). El Módulo III recorre técnicas de observación y las tecnologías que las hicieron posibles — escalas de décadas, como Hubble o James Webb.</p>
<nav class="idx"><span class="tag">Contenido</span><ol>
<li><a href="#s1">Refractores: lentes y límites</a></li>
<li><a href="#s2">¿Por qué telescopios grandes?</a></li>
<li><a href="#s3">Reflectores newtonianos y Cassegrain</a></li>
<li><a href="#s4">Escala histórica: Herschel a Palomar</a></li>
<li><a href="#s5">Revestimiento y espejos modernos</a></li>
<li><a href="#s6">Óptica activa (8 m)</a></li>
<li><a href="#s7">Espejos segmentados (Keck, GMT)</a></li>
<li><a href="#s8">Vera Rubin y campo amplio</a></li>
<li><a href="#s9">Difracción, seeing y óptica adaptativa</a></li>
<li><a href="#interactivo">Widgets</a></li>
<li><a href="#conceptos">Conceptos clave</a></li>
<li><a href="#examenes">Exámenes</a></li>
</ol></nav>

<section id="s1"><div class="shead"><span class="num">1</span><div><h2>Refractores: lentes y límites</h2>
<p>Galileo usó un <strong>refractor</strong>: lente objetivo concentra la luz; ocular la paraleliza para el ojo.</p></div></div>
<div class="box prof"><span class="tag">Corrección transcripción</span><p>En audio: «difracción de la luz en lentes». Físicamente es <strong>refracción</strong> (cambio de índice al entrar/salir del vidrio). La dispersión cromática produce arcoíris en los bordes del campo.</p></div>
<p>Limitaciones: solo se sujeta por los bordes → flexión y vibración; vidrio grueso y pesado; aberración cromática. Gaia debe corregir movimientos propios espurios por este efecto óptico.</p>
{fig("m3c1", 3, "Esquema de telescopio refractor.")}
{fig("m3c1", 5, "Dispersión cromática en lente: arcoíris en los bordes.")}
</section>

<section id="s2"><div class="shead"><span class="num">2</span><div><h2>¿Por qué telescopios grandes?</h2>
<p>Ley del inverso del cuadrado: flujo ∝ 1/d². Objeto al doble de distancia → un cuarto de luminosidad. Área colectora grande = más fotones por segundo.</p></div></div>
<div class="formula"><span class="katex-block" data-tex="F = \\frac{L}{4\\pi d^2}"></span>
<small>Analogía biológica: ojos de animales nocturnos con pupilas enormes.</small></div>
{fig("m3c1", 8, "Área colectora vs. distancia al objeto.")}
</section>

<section id="s3"><div class="shead"><span class="num">3</span><div><h2>Reflectores: Newton y Cassegrain</h2>
<p>Newton: espejo primario + secundario que desvía la luz al lateral. Cassegrain: orificio central en el primario. Ventajas: soporte por detrás, espejos más grandes, corrección activa de forma.</p></div></div>
{fig("m3c1", 12, "Monturas newtoniana y Cassegrain.")}
<p>James Webb: capa de <strong>oro</strong> para reflejar bien en infrarrojo (no por costo del oro, sino por λ).</p>
</section>

<section id="s4"><div class="shead"><span class="num">4</span><div><h2>Escala histórica: Herschel a Palomar</h2>
<p>Herschel (~1785): lente ~1,2 m, tubo ~12 m. Yerkes (1890): 1 m, 18 m de largo; piso móvil para el observador. Lick: piso que sube/baja; el mecenas enterrado bajo la cúpula.</p></div></div>
{fig("m3c1", 14, "Telescopio de Herschel.")}{fig("m3c1", 16, "Yerkes: refractor clásico.")}
<p>Palomar 5 m (~1948): límite de espejo monolítico rígido. Dupont/Las Campanas 2,5 m: comparable al Hubble espacial en diámetro.</p>
{fig("m3c1", 22, "Espejo de 2,5 m en Las Campanas.")}
</section>

<section id="s5"><div class="shead"><span class="num">5</span><div><h2>Revestimiento y fabricación</h2>
<p>Evaporación en cámara de vacío: filamentos de Al o Ag se evaporan en capas de 2–3 átomos. Mirror Lab (Arizona): vidrio fundido en centrífuga de 8 m, meses de enfriamiento controlado.</p></div></div>
{fig("m3c1", 26, "Fabricación de espejo en centrífuga.")}
</section>

<section id="s6"><div class="shead"><span class="num">6</span><div><h2>Óptica activa (~8 m)</h2>
<p>Gemini 8 m: espejo más delgado + ~120 pistones que corrigen deformación al apuntar. Estrella guía: si se alarga → reenfocar (~1 min). Distinto de óptica adaptativa (atmósfera, ms).</p></div></div>
{fig("m3c1", 28, "Gemini vs. Palomar: estructura más compacta.")}{fig("m3c1", 30, "Magallanes 6,5 m en Las Campanas.")}
</section>

<section id="s7"><div class="shead"><span class="num">7</span><div><h2>Espejos segmentados</h2>
<p>Keck (Hawái): 36 hexágonos de ~2 m, 7,5 cm grosor, 3 pistones cada uno. Problema computacional de los 80: alinear todos los segmentos. ELT: 40 m + láseres para OA.</p></div></div>
{fig("m3c1", 33, "Espejo segmentado Keck (proyección).")}{fig("m3c1", 35, "GMT: siete espejos de 8 m.")}
</section>

<section id="s8"><div class="shead"><span class="num">8</span><div><h2>Vera Rubin (LSST)</h2>
<p>8,4 m con curvaturas primaria+terciaria; campo 3,5° (~40 lunas). Cámara 3,2 Gpx; ~cada 5 min una imagen; terabytes/noche.</p></div></div>
<div class="box prof"><span class="tag">Corrección transcripción</span><p>«Verapoint» / «ver a Rubí» → <strong>Vera Rubin Observatory</strong> (antes LSST).</p></div>
{fig("m3c1", 37, "Camino óptico Vera Rubin.")}
</section>

<section id="s9"><div class="shead"><span class="num">9</span><div><h2>Difracción, seeing y óptica adaptativa</h2>
<p>Límite de difracción del telescopio: patrón de Airy. Atmósfera → <strong>seeing</strong> (imagen que titila y se desparrama).</p></div></div>
<div class="box prof"><span class="tag">Corrección transcripción</span><p>Audio: «zinc», «SIG», «sync» → <strong>seeing</strong>. Chile ~0,6″ es excelente; Brasil puede ser 10–100× peor.</p></div>
<div class="formula"><span class="katex-block" data-tex="\\theta \\approx 1.22\\,\\frac{\\lambda}{D}"></span>
<small>θ = tamaño del disco de Airy; D = diámetro del telescopio.</small></div>
<p>Óptica adaptativa: láser en capa de sodio → estrella artificial; espejo deformable corrige frente de ondas en ms. Keck: órbitas estelares en Sgr A* (Nobel Ghez/Genzel). Comparación Galileo vs. Hubble en Saturno.</p>
<div class="box prof"><span class="tag">Corrección transcripción</span><p>«Telescopio espacial Hull» → <strong>Hubble</strong>.</p></div>
{fig("m3c1", 36, "Simulación: sin atmósfera vs. con seeing vs. con OA.")}{fig("m3c1", 38, "Centro galáctico con y sin óptica adaptativa.")}
</section>

<section id="interactivo">
<div class="widget" id="w-airy"><h4>Límite de difracción θ ≈ 1,22 λ/D</h4>
<div class="wgrid"><label>λ (nm)<input type="number" id="airy-lam" value="500"></label>
<label>D (m)<input type="number" id="airy-d" value="8" step="any"></label></div>
<output class="wout" id="airy-out"></output></div>
<div class="widget" id="w-flux"><h4>Ley del inverso del cuadrado</h4>
<label>Factor de distancia d<input type="range" id="flux-d" min="1" max="5" step="0.5" value="2">
<output class="wout" id="flux-out"></output></div>
</section>

<section id="conceptos"><div class="tbl"><table>
<thead><tr><th>Concepto</th><th>Resumen</th></tr></thead>
<tbody>
<tr><td><b>Refractor</b></td><td>Lentes; limitado por peso y cromatismo</td></tr>
<tr><td><b>Reflector</b></td><td>Espejos; escala a metros</td></tr>
<tr><td><b>Óptica activa</b></td><td>Pistones corrigen forma del espejo (~min)</td></tr>
<tr><td><b>Segmentado</b></td><td>Keck, ELT; muchos grados de libertad</td></tr>
<tr><td><b>Seeing</b></td><td>Turbulencia atmosférica; &gt; difracción en tierra</td></tr>
<tr><td><b>Óptica adaptativa</b></td><td>Corrige atmósfera en ms (láser + deformable)</td></tr>
</tbody></table></div></section>
{e}
<footer><p><b>Fuentes:</b> <code>observación/m3/ff/observacion-m3c1.md</code>, diapositivas Módulo III Clase 1.</p>
{disc_footer()}</footer>
</main>
"""
    return head_ap("Telescopios — Módulo III · Clase 1") + body + (TAIL_AP % WIDGETS_C1)
