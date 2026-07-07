#!/usr/bin/env python3
"""Generate m3c1 and m3c2 apuntes HTML."""
import re
import pathlib

BASE = pathlib.Path(__file__).resolve().parent
REF = BASE.parent.parent / "m2" / "html" / "m2c1-apuntes.html"
ref = REF.read_text(encoding="utf-8")
css_m = re.search(r"<style>(.*?)</style>", ref, re.S)
css = css_m.group(1) if css_m else ""


def head(title: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,600&family=Spectral:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<style>{css}</style>
</head>
<body>
"""


TAIL = """
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


def fig(cx, n, cap, alt=""):
    return f"""<figure>
<img src="{cx}/assets/slide-{n:02d}.jpg" alt="{alt}">
<figcaption><span class="cap">Diapositiva {n}</span>{cap}</figcaption>
</figure>"""


def exams(cx, items):
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


WIDGETS_C1 = r'''
  var G=6.67430e-11, c=299792458, Msun=1.98847e30;
  function rsCalc(){
    var M=+document.getElementById('rs-m').value*Msun;
    var rs=2*G*M/(c*c);
    document.getElementById('rs-out').innerHTML='r<sub>s</sub> ≈ <b>'+(rs/1000).toFixed(3)+'</b> km';
  }
  var rsm=document.getElementById('rs-m');
  if(rsm){rsm.oninput=rsCalc;document.querySelectorAll('#w-rs button').forEach(function(b){b.onclick=function(){rsm.value=b.dataset.m;rsCalc();};});rsCalc();}
  function gpsCalc(){
    var h=+document.getElementById('gps-h').value*1000, Re=6371000, M=5.972e24;
    document.getElementById('gps-hv').textContent=(h/1000).toLocaleString('es');
    var r=Re+h, v=Math.sqrt(6.67430e-11*M/r);
    var dtGR=(6.67430e-11*M/(c*c*Re)-6.67430e-11*M/(c*c*r))*86400*1e6;
    var dtSR=-0.5*(v*v/(c*c))*86400*1e6;
    document.getElementById('gps-out').innerHTML='Neto ≈ <b>'+(dtGR+dtSR).toFixed(1)+'</b> μs/día (estimación GPS)';
  }
  var gpsh=document.getElementById('gps-h'); if(gpsh){gpsh.oninput=gpsCalc;gpsCalc();}
  function gCalc(){
    var v=+document.getElementById('g-v').value;
    document.getElementById('gv').textContent=v.toFixed(3);
    var g=1/Math.sqrt(1-v*v);
    document.getElementById('g-out').innerHTML='γ = <b>'+g.toFixed(4)+'</b>';
  }
  var gv=document.getElementById('g-v'); if(gv){gv.oninput=gCalc;gCalc();}
'''

WIDGETS_C2 = r'''
  var c=299792458, ly=9.4607e15, AU=1.496e11, Msun=1.98847e30, yr=365.25*86400;
  function varCalc(){
    var dt=+document.getElementById('var-dt').value*+document.getElementById('var-unit').value;
    var R=c*dt;
    document.getElementById('var-out').innerHTML='R ≲ <b>'+(R/AU).toExponential(2)+'</b> UA · <b>'+(R/ly).toFixed(3)+'</b> ly';
  }
  document.getElementById('var-dt').oninput=varCalc;
  document.getElementById('var-unit').oninput=varCalc; varCalc();
  function accCalc(){
    var mdot=+document.getElementById('acc-mdot').value*Msun/yr;
    var eta=+document.getElementById('acc-eta').value;
    document.getElementById('acc-etav').textContent=eta.toFixed(3);
    var L=eta*mdot*c*c, Lsun=3.828e26;
    document.getElementById('acc-out').innerHTML='L ≈ <b>'+(L/Lsun).toExponential(2)+'</b> L<sub>☉</sub>';
  }
  document.getElementById('acc-mdot').oninput=accCalc;
  document.getElementById('acc-eta').oninput=accCalc; accCalc();
'''


def build_m3c1():
    e = exams("m3c1", [
        (1, "Relatividad especial"), (2, "Principio equivalencia"), (3, "Efectos gravitacionales"),
        (4, "Evidencia histórica"), (5, "Lentes gravitacionales"), (6, "Ondas gravitacionales I"),
        (7, "Hulse–Taylor y LIGO"), (8, "Poblaciones de fusiones"), (9, "Tipos de ondas"),
        (10, "Integrador clase 1"),
    ])
    body = f"""
<main class="wrap">
<nav class="top"><a href="index.html">← Módulo III — índice</a></nav>
<div class="hero">
<span class="kick">Astrofísica de Galaxias · Módulo III · Clase 1</span>
<h1>Del espacio-tiempo plano a las <em>ondas gravitacionales</em></h1>
<p class="sub">Einstein, relatividad especial y general, lentes gravitacionales y detección de ondas gravitacionales.</p>
</div>
<p class="lead"><span class="drop">E</span>l Módulo III entra en régimen relativista: agujeros negros, núcleos activos y ondas gravitacionales. Esta clase es el andamiaje físico — postulados, predicciones e instrumentos de verificación.</p>
<nav class="idx"><span class="tag">Contenido</span><ol>
<li><a href="#s1">Einstein y 1905</a></li><li><a href="#s2">Velocidad relativa vs. SR</a></li>
<li><a href="#s3">c constante y dilatación temporal</a></li><li><a href="#s4">Equivalencia y E=mc²</a></li>
<li><a href="#s5">Relatividad general</a></li><li><a href="#s6">GPS y redshift gravitacional</a></li>
<li><a href="#s7">Mercurio y eclipse 1919</a></li><li><a href="#s8">Lentes gravitacionales</a></li>
<li><a href="#s9">Ondas gravitacionales y LIGO</a></li><li><a href="#interactivo">Widgets</a></li>
<li><a href="#conceptos">Conceptos</a></li><li><a href="#examenes">Exámenes</a></li>
</ol></nav>

<section id="s1"><div class="shead"><span class="num">1</span><div><h2>Einstein y el año 1905</h2></div></div>
<p><strong>1905:</strong> fotoeléctrico, browniano, relatividad especial, <span class="katex-inline" data-tex="E=mc^2"></span>. <strong>1915:</strong> relatividad general (RG). La equivalencia masa–energía explicó el brillo estelar (fusión nuclear).</p>
{fig("m3c1", 1, "Apertura del módulo III.")}
</section>

<section id="s2"><div class="shead"><span class="num">2</span><div><h2>Velocidad relativa cotidiana</h2></div></div>
<p>Perro en tren, metro que parte: la velocidad depende del observador. A escala galáctica sumamos órbitas anidadas. Esto es cinemática clásica, <em>no</em> relatividad especial.</p>
</section>

<section id="s3"><div class="shead"><span class="num">3</span><div><h2>Relatividad especial</h2></div></div>
<p>Postulado central: <strong>c es constante</strong> en el vacío para todos los observadores inerciales (compatible con Michelson–Morley y con mediciones astronómicas en distintas épocas del año).</p>
<p>Experimento del <strong>reloj de luz</strong>: en el vagón, ida y vuelta vertical (distancia 2L). Para quien ve el tren moverse, la luz recorre hipotenusa → trayectoria más larga. Con la misma c, el tiempo medido en tierra debe ser mayor: <span class="hl">dilatación temporal</span>. También aparece <strong>contracción de longitudes</strong> en la dirección del movimiento.</p>
<div class="box cs"><span class="tag">Ingeniería</span><p>Piensa en sincronizar dos relojes en redes distribuidas: si asumes simultaneidad absoluta pero las señales viajan a c finita, cometes errores sistemáticos. La SR formaliza ese error en marcos que se mueven uno respecto al otro.</p></div>
<div class="formula"><span class="katex-block" data-tex="\\Delta t' = \\gamma \\Delta t,\\quad \\gamma = 1/\\sqrt{{1-v^2/c^2}}"></span></div>
{fig("m3c1", 8, "Reloj de luz en vagón en movimiento.")}
</section>

<section id="s4"><div class="shead"><span class="num">4</span><div><h2>Principio de equivalencia</h2></div></div>
<p>Campo gravitatorio uniforme ≡ aceleración. Caída libre ≡ ingravidez (astronautas en órbita). Distinto del principio de inercia (Galileo/Newton).</p>
</section>

<section id="s5"><div class="shead"><span class="num">5</span><div><h2>Relatividad general</h2></div></div>
<p>Materia y energía curvan el espacio-tiempo (4D). Los cuerpos siguen geodésicas. Metáfora de la malla 2D es limitada.</p>
{fig("m3c1", 15, "Curvatura por Sol, Tierra y Júpiter.")}
<div class="box physics"><span class="tag">Tiempo y luz</span><p>Cerca de masa: relojes más lentos; luz que escapa se enrojece (redshift gravitacional).</p></div>
</section>

<section id="s6"><div class="shead"><span class="num">6</span><div><h2>GPS y efectos medibles</h2></div></div>
<p>Interestelar: cerca del agujero negro el tiempo es mucho más lento. GPS requiere corrección relativista.</p>
<div class="box dato"><span class="tag">Orden de magnitud</span><p>Corrección neta ~<strong>38–45 microsegundos/día</strong> (no milisegundos; posible lapsus en transcripción).</p></div>
</section>

<section id="s7"><div class="shead"><span class="num">7</span><div><h2>Mercurio y eclipse 1919</h2></div></div>
<p>Perihelio de Mercurio: +43″/siglo por RG. Eclipse 1919: deflexión de luz estelar; mayor desplazamiento más cerca del Sol. Sobral y Príncipe; Crommelin y Eddington.</p>
{fig("m3c1", 22, "Esquema del eclipse.")}{fig("m3c1", 24, "Placa fotográfica 1919.")}
</section>

<section id="s8"><div class="shead"><span class="num">8</span><div><h2>Lentes gravitacionales</h2></div></div>
<p>Cúmulos masivos (p. ej. Abell 2218) distorsionan luz de fondo → arcos, anillos de Einstein. Materia oscura domina el potencial. Supernovas lenteadas con retardos temporales entre imágenes.</p>
{fig("m3c1", 27, "Lente fuerte en cúmulo.")}
</section>

<section id="s9"><div class="shead"><span class="num">9</span><div><h2>Ondas gravitacionales y LIGO</h2></div></div>
<p>Las <strong>ondas gravitacionales (GW)</strong> son perturbaciones del espacio-tiempo que se propagan a c. Se generan cuando distribuciones de masa <em>aceleran</em> de forma no simétrica (radiación cuadrupolar). La amplitud típica en LIGO es ~10<sup>−21</sup> (cambio relativo de longitud del orden del tamaño atómico en brazos de 4 km).</p>
<ul>
<li><strong>Analogía EM:</strong> cargas aceleradas → ondas electromagnéticas; masas aceleradas → GW. La gravedad es muchísimo más débil → señales minúsculas.</li>
<li><strong>Hulse–Taylor (PSR B1913+16):</strong> el período orbital de un binario de pulsares decrece ~76 μs/año, consistente con pérdida de energía por GW → Nobel 1993 (detección indirecta).</li>
<li><strong>LIGO (14 sep 2015):</strong> GW150914, fusión de dos BH ~30 M<sub>☉</sub> a ~1,3 Gpc. Virgo y KAGRA se sumaron después.</li>
</ul>
<p>El detector es un <strong>interferómetro Michelson</strong> con brazos perpendiculares: la GW modula ligeramente la diferencia de camino óptico. Se exige coincidencia entre observatorios separados (Hanford WA, Livingston LA) para descartar ruido local. La forma de la señal: <em>chirp</em> (frecuencia creciente al acercarse), pico de fusión, <em>ringdown</em> (modos cuasinormales del BH final).</p>
<p>Implicancia astrofísica: apareció una población de BH estelares más masiva que la conocida solo por rayos X. Las <strong>kilonovas</strong> (fusión de estrellas de neutrones, GW170817) unen GW y luz, confirmando producción de elementos pesados por r-proceso.</p>
{fig("m3c1", 33, "Primera señal LIGO.")}{fig("m3c1", 35, "Masas GW vs. EM.")}
<div class="box next"><span class="tag">Siguiente</span><p>Clase 2: Schwarzschild, horizonte y agujeros negros observables.</p></div>
</section>

<section id="interactivo">
<div class="widget" id="w-rs"><h4>Radio de Schwarzschild</h4>
<label>M (M<sub>☉</sub>)</label><input type="number" id="rs-m" value="1" step="any">
<div class="presets"><button data-m="1">1 M<sub>☉</sub></button><button data-m="10">10 M<sub>☉</sub></button><button data-m="4e6">Sgr A*</button></div>
<output class="wout" id="rs-out"></output></div>
<div class="widget" id="w-gps"><h4>Corrección GPS (μs/día)</h4>
<label>Altitud km</label><input type="range" id="gps-h" min="200" max="40000" value="20200">
<p><span id="gps-hv">20200</span> km</p><output class="wout" id="gps-out"></output></div>
<div class="widget"><h4>Factor γ(v)</h4>
<input type="range" id="g-v" min="0" max="0.999" step="0.001" value="0.5"> v/c=<span id="gv">0.5</span>
<output class="wout" id="g-out"></output></div>
</section>

<section id="conceptos"><div class="tbl"><table>
<thead><tr><th>Concepto</th><th>Resumen</th></tr></thead>
<tbody>
<tr><td><b>SR</b></td><td>c invariante; tiempo y longitud relativos</td></tr>
<tr><td><b>RG</b></td><td>Curvatura por masa-energía</td></tr>
<tr><td><b>Redshift grav.</b></td><td>Luz pierde energía al escapar</td></tr>
<tr><td><b>Lente grav.</b></td><td>Masa magnifica fondo</td></tr>
<tr><td><b>GW / LIGO</b></td><td>Astronomía de ondas a c; fusiones compactas</td></tr>
</tbody></table></div></section>
{e}
<footer><p><b>Fuentes:</b> <code>galaxias/m3/ff/galaxias-m3c1.md</code>, diapositivas Módulo III Clase 1.</p>
<p class="disc">Transcripción automática; contrastada con diapositivas y física estándar.</p></footer>
</main>
"""
    return head("Relatividad y ondas gravitacionales — Módulo III · Clase 1") + body + (TAIL % WIDGETS_C1)


def build_m3c2():
    e = exams("m3c2", [
        (1, "Schwarzschild"), (2, "Compacidad"), (3, "Espaguetificación"),
        (4, "Remanentes"), (5, "SN 1987A"), (6, "Detectar BH"),
        (7, "SS 433"), (8, "TDE"), (9, "SMBH"), (10, "Quásares y AGN"),
    ])
    body = f"""
<main class="wrap">
<nav class="top"><a href="index.html">← Módulo III</a> · <a href="m3c1-apuntes.html">Clase 1</a></nav>
<div class="hero">
<span class="kick">Astrofísica de Galaxias · Módulo III · Clase 2</span>
<h1>Agujeros negros: de <em>Schwarzschild</em> a los AGN</h1>
<p class="sub">Horizonte, remanentes estelares, detección por acreción y dinámica, camino hacia cuásares.</p>
</div>
<p class="lead"><span class="drop">L</span>o decisivo no es solo la masa sino la <strong>compacidad</strong>. La clase une predicción relativista, supernovas, binarias de rayos X y agujeros negros supermasivos activos.</p>
<nav class="idx"><span class="tag">Contenido</span><ol>
<li><a href="#s1">Schwarzschild</a></li><li><a href="#s2">Horizonte y compacidad</a></li>
<li><a href="#s3">Espaguetificación</a></li><li><a href="#s4">Supernovas y remanentes</a></li>
<li><a href="#s5">Detectar BH estelares</a></li><li><a href="#s6">Jets y TDE</a></li>
<li><a href="#s7">SMBH y AGN</a></li><li><a href="#s8">Cuásares y variabilidad</a></li>
<li><a href="#interactivo">Widgets</a></li><li><a href="#conceptos">Conceptos</a></li>
<li><a href="#examenes">Exámenes</a></li>
</ol></nav>

<section id="s1"><div class="shead"><span class="num">1</span><div><h2>Schwarzschild (1916)</h2></div></div>
<div class="box prof"><span class="tag">Transcripción</span><p>«Churchill» en audio = <strong>Karl Schwarzschild</strong>.</p></div>
<div class="formula"><span class="katex-block" data-tex="r_s = 2GM/c^2"></span>
<small>1 M<sub>☉</sub> → ~3 km; Tierra → ~9 mm.</small></div>
{fig("m3c2", 4, "Horizonte y escalas.")}
</section>

<section id="s2"><div class="shead"><span class="num">2</span><div><h2>Horizonte y compacidad</h2></div></div>
<p>Horizonte = límite causal, no superficie material. Misma masa: Sol vs. enana blanca vs. BH → mismo campo lejos, pozo distinto cerca. Estrella de neutrones ~10 km vs. horizonte de BH similar: la EN tiene superficie.</p>
{fig("m3c2", 8, "Pozos gravitacionales comparados.")}
</section>

<section id="s3"><div class="shead"><span class="num">3</span><div><h2>Espaguetificación y gusanos</h2></div></div>
<p>Mareas intensas cerca del BH. Puentes Einstein–Rosen: matemática sin evidencia observacional. ISCO: órbitas inestables interior.</p>
{fig("m3c2", 11, "Caída hacia agujero negro.")}
</section>

<section id="s4"><div class="shead"><span class="num">4</span><div><h2>Remanentes y supernovas</h2></div></div>
<p>~10<sup>11</sup> estrellas en galaxia tipo Vía Láctea; ~10<sup>8</sup> BH estelares. Baja masa → enana blanca; alta masa → SN → EN o BH.</p>
<p><strong>SN 1987A</strong> (LMC): ~24 neutrinos; <strong>Cangrejo</strong> (1054); <strong>Eta Carinae</strong> candidata.</p>
{fig("m3c2", 16, "SN 1987A.")}{fig("m3c2", 18, "Diagrama evolutivo.")}
</section>

<section id="s5"><div class="shead"><span class="num">5</span><div><h2>Detectar agujeros negros</h2></div></div>
<p><strong>Acreción:</strong> disco caliente, rayos X (~200 binarias X en la Vía Láctea). <strong>Dinámica:</strong> órbitas estelares (Sgr A*).</p>
{fig("m3c2", 21, "Binaria de rayos X.")}
</section>

<section id="s6"><div class="shead"><span class="num">6</span><div><h2>Jets, mareas, TDE</h2></div></div>
<p>SS 433: jets precesionando (sacacorcho). Colas de marea HI (Magallanes). TDE: estrella despedazada por BH.</p>
{fig("m3c2", 23, "SS 433.")}
</section>

<section id="s7"><div class="shead"><span class="num">7</span><div><h2>SMBH y AGN</h2></div></div>
<p>SMBH: 10<sup>6</sup>–10<sup>10</sup> M<sub>☉</sub> en núcleos. Sgr A* ~4×10<sup>6</sup> M<sub>☉</sub>. Alimentados → AGN.</p>
</section>

<section id="s8"><div class="shead"><span class="num">8</span><div><h2>Cuásares y variabilidad</h2></div></div>
<p>En los años 50–60 aparecieron fuentes <strong>cuasi estelares</strong> de radio (QSO). Parecían estrellas puntuales pero con luminosidad y espectros anómalos.</p>
<p><strong>Maarten Schmidt (1963):</strong> en 3C 273 las líneas «desconocidas» eran Hα, Hβ, Hγ… con <strong>gran redshift</strong> (z ≈ 0,16). Objeto extragaláctico ultraluminoso: L ~ 10× la de la Vía Láctea. El núcleo brilla tanto que opaca la galaxia anfitriona.</p>
<p><strong>Argumento de variabilidad:</strong> si el brillo cambia en tiempo Δt, la región emisora no puede ser mucho mayor que R ≲ c·Δt (cota superior; la señal no puede coordinar un cambio instantáneo en toda una galaxia). Variaciones en ~1 año → tamaño ≲ 1 año-luz; variaciones en días → escala del Sistema Solar, pero con luminosidad de muchas galaxias → requiere <strong>acreción sobre agujero negro supermasivo</strong>.</p>
<p>La acreción convierte energía gravitacional en radiación con eficiencia η hasta ~10% (Ṁc²), muy por encima de la fusión nuclear estelar (~0,7%). Es el motor de los AGN. Solo ~10% de AGN muestran jets de radio prominentes; el resto son «radio-quiet» pero igualmente luminosos en otras bandas.</p>
{fig("m3c2", 27, "Curva de luz de cuásar con variabilidad fuerte.")}{fig("m3c2", 28, "Modelo esquemático AGN: disco, corona, jet.")}
</section>

<section id="interactivo">
<div class="widget"><h4>c·Δt</h4>
<input type="number" id="var-dt" value="1" step="any">
<select id="var-unit"><option value="3600">horas</option><option value="86400">días</option><option value="31557600" selected>años</option></select>
<output class="wout" id="var-out"></output></div>
<div class="widget"><h4>Luminosidad de acreción L≈ηṀc²</h4>
<input type="number" id="acc-mdot" value="1" step="any"> M<sub>☉</sub>/año
<input type="range" id="acc-eta" min="0.01" max="0.4" step="0.01" value="0.1"> η=<span id="acc-etav">0.10</span>
<output class="wout" id="acc-out"></output></div>
</section>

<section id="conceptos"><div class="tbl"><table>
<thead><tr><th>Concepto</th><th>Nota</th></tr></thead>
<tbody>
<tr><td><b>r_s</b></td><td>Horizonte BH estático</td></tr>
<tr><td><b>Binaria X</b></td><td>~200 en Vía Láctea</td></tr>
<tr><td><b>TDE</b></td><td>Flare por estrella rota</td></tr>
<tr><td><b>AGN</b></td><td>SMBH alimentado; cuásar si muy luminoso</td></tr>
</tbody></table></div></section>
{e}
<footer><p><b>Fuentes:</b> <code>galaxias-m3c2.md</code>, diapositivas Clase 2. Ver <a href="m3c1-apuntes.html">clase 1</a>.</p></footer>
</main>
"""
    return head("Agujeros negros y AGN — Módulo III · Clase 2") + body + (TAIL % WIDGETS_C2)


def main():
    (BASE / "m3c1-apuntes.html").write_text(build_m3c1(), encoding="utf-8")
    (BASE / "m3c2-apuntes.html").write_text(build_m3c2(), encoding="utf-8")
    print("Generated apuntes OK")


if __name__ == "__main__":
    main()
