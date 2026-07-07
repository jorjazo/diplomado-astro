#!/usr/bin/env python3
"""Generate galaxias m3 exam HTML files."""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
COURSE = "Astrofísica de Galaxias"

CSS = """<style>
:root{--bg:#070a12;--ink:#ece8df;--muted:#9aa6bb;--line:#26324a;--red:#e0382e;--red-soft:#f06a5e;--gold:#d9a74a;--cyan:#6fc7d6;--ok:#5fd07e;--bad:#f06a5e}
*{box-sizing:border-box}
body{margin:0;color:var(--ink);background:var(--bg);font-family:"Spectral",Georgia,serif;font-size:18px;line-height:1.7;
  background-image:radial-gradient(1.3px 1.3px at 20% 30%,rgba(255,255,255,.4),transparent),radial-gradient(1200px 700px at 80% -8%,#16203a 0%,transparent 60%),linear-gradient(180deg,#070a12,#0a0f1b);background-attachment:fixed}
.wrap{max-width:820px;margin:0 auto;padding:24px 22px 80px}
nav{font-size:.9rem;margin-bottom:18px}nav a{color:var(--muted);text-decoration:none}nav a:hover{color:var(--red-soft)}
.kick{font-family:"Fraunces",serif;font-size:.78rem;letter-spacing:.2em;text-transform:uppercase;color:var(--red-soft);font-weight:600}
h1{font-family:"Fraunces",serif;font-size:clamp(1.8rem,5vw,2.6rem);margin:.15em 0 .5em;font-weight:600}
.intro{color:var(--muted);font-size:.96rem;margin-bottom:24px}
fieldset{border:1px solid var(--line);border-radius:14px;margin:18px 0;padding:16px 20px;background:#0b112099}
legend{font-family:"Fraunces",serif;font-weight:600;color:#fff;padding:0 10px;font-size:1.04rem}
.qopen{border:1px dashed #36425c;border-radius:14px;margin:18px 0;padding:16px 20px;background:#0a0f1b80}
.qopen p.q{font-family:"Fraunces",serif;color:#fff;font-weight:600;margin:.1em 0 .4em}
label.opt{display:block;padding:8px 12px;border:1px solid transparent;border-radius:9px;margin:5px 0;cursor:pointer}
label.opt:hover{background:#10203a}
label.opt input{accent-color:var(--red);margin-right:10px}
.btn{background:var(--red);color:#fff;border:none;border-radius:10px;padding:11px 20px;font-family:"Fraunces",serif;font-weight:600;cursor:pointer;margin-top:8px}
.score{font-family:"Fraunces",serif;font-weight:600;margin-top:14px}
.fb{font-size:.86rem;margin-top:6px;color:var(--muted)}
fieldset.correct{border-color:var(--ok)}fieldset.wrong{border-color:var(--bad)}
details{margin-top:10px;border-top:1px solid var(--line);padding-top:10px}
summary{cursor:pointer;color:var(--gold);font-family:"Fraunces",serif;font-weight:600}
.answer{margin-top:10px;color:#d7e0ef;font-size:.96rem}
.tag{display:inline-block;font-size:.68rem;letter-spacing:.14em;text-transform:uppercase;color:var(--cyan);font-family:"Fraunces",serif;font-weight:600;border:1px solid var(--line);border-radius:999px;padding:2px 10px;margin-bottom:6px}
footer{margin-top:40px;border-top:1px solid var(--line);padding-top:18px;color:var(--muted);font-size:.85rem}
</style>"""

HEAD_LINKS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,600&family=Spectral:wght@400;500;600&display=swap" rel="stylesheet">'

SCRIPT = """<script>
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


def mc_block(n, legend, opts, fb):
    letters = "abcd"
    lines = [f'  <fieldset data-q="{n}"><legend>{n}. {legend}</legend>']
    for i, opt in enumerate(opts):
        lines.append(f'    <label class="opt"><input type="radio" name="q{n}" value="{letters[i]}">{opt}</label>')
    lines.append(f'    <p class="fb" hidden>{fb}</p>')
    lines.append('  </fieldset>')
    return "\n".join(lines)


def open_block(n, q, ans):
    return f"""<div class="qopen"><span class="tag">Respuesta escrita</span>
  <p class="q">{n}. {q}</p>
  <details><summary>Ver respuesta propuesta</summary>
    <div class="answer">{ans}</div>
  </details>
</div>"""


def render_exam(cx, nn, title, mod, cls, mc, opens, answers):
    ap = f"{cx}-apuntes.html"
    fn = f"{cx}-examen-{nn:02d}.html"
    mc_html = "\n".join(mc_block(i + 1, m[0], m[1], m[2]) for i, m in enumerate(mc))
    open_html = "\n".join(open_block(i + 4, o[0], o[1]) for i, o in enumerate(opens))
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Examen {nn:02d} — {cx} · {title}</title>
{HEAD_LINKS}
{CSS}
</head>
<body>
<main class="wrap">
<nav><a href="{ap}#examenes">← Apuntes (exámenes)</a> · <a href="index.html">Índice del módulo</a></nav>
<span class="kick">{COURSE} · Módulo {mod} · Clase {cls}</span>
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
{SCRIPT}
</body>
</html>
"""
    path = os.path.join(BASE, fn)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return fn


# fmt: title, answers, [(legend, opts, fb)x3], [(q, ans)x2]
M3C1 = [
    ("Relatividad especial", "b,c,a",
     [("En relatividad especial, el postulado clave de Einstein (además de las leyes de la física en todos los marcos inerciales) es:",
       ["La velocidad de la luz depende del movimiento del observador", "La velocidad de la luz en el vacío es la misma para todos los observadores inerciales", "El tiempo es absoluto e igual para todos", "La masa y la energía son independientes"],
       "El experimento de Michelson–Morley y otros mostraron c constante; de ahí salen dilatación temporal y contracción de longitudes."),
      ("En el experimento mental del reloj de luz en un tren en movimiento, el observador en reposo respecto al suelo mide:",
       ["Menor tiempo de ida y vuelta que el pasajero del tren", "Mayor tiempo de ida y vuelta que el pasajero del tren", "Exactamente el mismo tiempo", "Tiempo cero"],
       "La trayectoria de la luz es más larga para quien ve el tren moverse; con c fija, el intervalo temporal debe ser mayor → dilatación temporal."),
      ("La ecuación E = mc² implica que:",
       ["La masa no puede convertirse en energía", "Masa y energía son equivalentes y convertibles", "Solo aplica a partículas sin masa", "Contradice la conservación de energía"],
       "Explica el motor estelar: fusión nuclear convierte una fracción de masa en energía radiada.")],
     [("Distingue «velocidad relativa» cotidiana (ardilla, tren, perro) de lo que postula la relatividad especial sobre el tiempo. ¿Por qué no son lo mismo?",
       "La velocidad relativa clásica solo cambia quién mide qué componente de movimiento. La relatividad especial asume que <strong>c es finita e invariante</strong>: si dos observadores inerciales miden el mismo fenómeno lumínico, deben reconciliar distancias y tiempos de forma que el cociente distancia/tiempo sea siempre c. Eso fuerza a que el <strong>tiempo no sea absoluto</strong> (dilatación) y las longitudes paralelas al movimiento se contraigan. Es simétrico: cada uno ve al otro con reloj «lento»."),
      ("Resume en tres líneas por qué la relatividad especial fue revolucionaria para la física del siglo XX.",
       "1) Rompió la intuición de tiempo y espacio absolutos. 2) Unificó espacio y tiempo en espacio-tiempo con intervalo invariante. 3) Mostró que la energía y la masa son aspectos de una misma cantidad (E=mc²), abriendo la puerta a explicar estrellas y partículas con precisión experimental.")]),
    ("Principio de equivalencia", "a,b,c",
     [("El principio de equivalencia de Einstein establece que:",
       ["Un campo gravitacional uniforme es indistinguible de un marco acelerado", "La gravedad es más débil que el electromagnetismo", "Los astronautas no sienten gravedad porque están lejos de la Tierra", "La inercia y la gravedad son fuerzas distintas sin relación"],
       "Localmente, estar en reposo sobre la Tierra ≡ estar en una caja acelerada hacia arriba en el espacio libre de campos."),
      ("Los astronautas en órbita «flotan» porque:",
       ["No hay gravedad a esa altura", "Están en caída libre continua alrededor de la Tierra", "El motor de la nave cancela la gravedad", "La Estación Espacial no tiene masa"],
       "Siguen acelerándose hacia la Tierra, pero también se mueven lateralmente: caen sin dejar de «perderse» el suelo."),
      ("En relatividad general, la gravedad se interpreta como:",
       ["Una fuerza a distancia newtoniana sin más", "Curvatura del espacio-tiempo producida por masa-energía", "Solo un efecto del aire y la presión", "Una ilusión óptica"],
       "Los cuerpos siguen geodésicas en un espacio-tiempo curvo; eso se percibe como aceleración gravitacional.")],
     [("Explica la analogía «caída libre ≡ flotar en el espacio» y por qué contradice la intuición de que «en el espacio no hay gravedad».",
       "En órbita la gravedad terrestre sigue siendo ~90 % de la de la superficie. Lo que desaparece es la <strong>reacción de apoyo</strong>: no hay suelo que empuje hacia arriba. Caer libremente es seguir una geodésica sin fuerzas no gravitacionales; desde dentro de la cápsula todo parece ingravidez. La intuición falla porque confundimos «no sentir peso» con «no haber gravedad»."),
      ("¿Por qué la malla elástica bidimensional es solo una metáfora limitada del espacio-tiempo curvo?",
       "Muestra cómo la masa «hunde» una superficie y las trayectorias se curvan, pero el espacio-tiempo real tiene <strong>tres dimensiones espaciales más el tiempo</strong> (4D). Además, la malla es un embedding en un espacio externo con gravedad newtoniana; en GR la curvatura es intrínseca, no necesita un «plano de fondo». Sirve para intuición, no para cuantificar.")]),
    ("Efectos gravitacionales", "c,b,a",
     [("Cerca de un cuerpo masivo, según relatividad general, el tiempo:",
       ["Avanza más rápido que lejos del cuerpo", "Avanza igual en todas partes", "Avanza más lento que lejos del cuerpo", "Se detiene completamente"],
       "Efecto de «gravedad más fuerte» ⇒ relojes más lentos (como en Interestelar cerca del agujero negro)."),
      ("El redshift gravitacional hace que la luz que escapa de un pozo gravitacional:",
       ["Aumente su frecuencia (se vuelva más azul)", "No cambie", "Disminuya su frecuencia (se enrojezca)", "Viaje más rápido que c"],
       "Pierde energía al salir del campo; λ aumenta, ν disminuye."),
      ("El sistema GPS requiere correcciones relativistas porque:",
       ["Los satélites no tienen relojes atómicos", "Los relojes en órbita corren a distinta tasa que en la superficie (efectos especial + general)", "La Tierra no rota", "La luz no llega a los satélites"],
       "Sin corregir ~38–45 μs/día de desfase acumulado, la navegación erraría por kilómetros en poco tiempo.")],
     [("Describe cómo se combinan los efectos de relatividad especial y general en los relojes del GPS (cualitativo).",
       "Los satélites se mueven rápido → la RS hace que sus relojes vayan <strong>más lentos</strong> que en tierra. Están más lejos del centro de la Tierra → la RG hace que vayan <strong>más rápidos</strong> (menos campo). El efecto gravitacional domina ligeramente; el neto es adelanto de ~38 μs/día, que el sistema corrige."),
      ("¿Por qué el redshift gravitacional importa cerca de estrellas de neutrones o agujeros negros pero es despreciable para el Sol en la mayoría de observaciones?",
       "Depende de la <strong>curvatura</strong>: Δν/ν ~ GM/(rc²). Para el Sol es del orden de 10⁻⁶ en la superficie; para una estrella de neutrones o un BH estelar los campos son muchísimo más intensos a pocos radios esféricos, y hay que usar métricas relativistas completas para rayos de luz y espectros.")]),
    ("Evidencia histórica", "b,a,c",
     [("La precesión anómala del perihelio de Mercurio se explica con:",
       ["Solo la mecánica newtoniana y Júpiter", "Correcciones de relatividad general (curvatura extra cerca del Sol)", "El viento solar exclusivamente", "Materia oscura en el Sistema Solar"],
       "Mercurio, el planeta más interno, es donde el término relativista es medible."),
      ("La confirmación de 1919 durante un eclipse solar midió:",
       ["La masa del Sol con balanza", "La deflexión de la luz de estrellas lejanas al pasar cerca del Sol", "La velocidad de Mercurio", "Ondas gravitacionales"],
       "Eddington/Crommelin compararon posiciones estelares con y sin el Sol en el campo visual."),
      ("En el eclipse de 1919, las estrellas más cercanas al limbo solar se desplazaron:",
       ["Igual que las lejanas", "Menos que las lejanas", "Más que las lejanas", "No se desplazaron"],
       "La deflexión angular ∝ 1/b, donde b es el parámetro de impacto; más cerca del Sol ⇒ mayor desviación.")],
     [("Resume el argumento experimental del eclipse de 1919: qué se predijo, qué se midió y por qué hacía falta un eclipse.",
       "La RG predice que la luz de estrellas de fondo se <strong>deflecta</strong> al pasar cerca del Sol (~1,75″ para rayos que rozan el limbo). En día normal el cielo junto al Sol está saturado de luz solar; durante el eclipse la Luna tapa el disco y se fotografían estrellas cercanas al limbo. Comparando con placas de noche (sin Sol en el campo), las posiciones debían correrse hacia afuera, como predijo Einstein."),
      ("¿Por qué la precesión de Mercurio fue evidencia convincente antes del eclipse de 1919?",
       "Llevaba décadas sin explicación newtoniana completa (~43″/siglo extra). Einstein calculó ese exceso desde su teoría sin ajustar parámetros libres, mostrando que la curvatura del espacio-tiempo solar modifica la órbita. Fue la primera predicción cuantitativa exitosa de la RG en el Sistema Solar.")]),
    ("Lentes gravitacionales", "a,c,b",
     [("Una lente gravitacional fuerte ocurre cuando:",
       ["La luz de una galaxia de fondo pasa cerca de un cúmulo masivo", "Un telescopio tiene mala óptica", "Hay polvo en la Vía Láctea", "Dos estrellas chocan físicamente"],
       "La masa del cúmulo curva el espacio y puede producir arcos, anillos o múltiples imágenes."),
      ("En el cúmulo Abell 2218, los arcos azules/rojos suelen ser:",
       ["Estrellas del cúmulo", "Galaxias de fondo altamente magnificadas y distorsionadas", "Nebulosas planetarias", "Cometas"],
       "Son galaxias mucho más lejanas cuya luz fue fuertemente lenteada."),
      ("Si una supernova en una galaxia lejana es lenteada en cuatro imágenes, las explosiones pueden verse:",
       ["Todas al mismo tiempo", "En tiempos distintos según la longitud de cada camino de la luz", "Solo en rayos X", "Nunca en el visible"],
       "Diferentes trayectorias ⇒ diferentes tiempos de viaje (demoras de meses, como se observó).")],
     [("¿Por qué las lentes gravitacionales de cúmulos son herramientas para mapear materia oscura?",
       "La distorsión depende de la <strong>masa total</strong> que curva el espacio, no solo de la materia luminosa (galaxias amarillas). Modelando los arcos y las magnificaciones se reconstruye el potencial gravitacional del cúmulo, revelando que la mayor parte de la masa no emite luz."),
      ("Compara la deflexión estelar de 1919 (Sol) con una lente de cúmulo en términos de escala y geometría.",
       "El Sol es un solo cuerpo compacto: deflexiones de ~arcsec y patrón radial simple. Un cúmulo es una «maraña» de masa (principalmente halo de materia oscura): produce arcos, anillos (Einstein) y múltiples imágenes de la misma galaxia. La escala de masa y la complejidad del potencial son órdenes de magnitud mayores.")]),
    ("Ondas gravitacionales I", "b,a,c",
     [("Las ondas gravitacionales son:",
       ["Ondas de presión en el aire", "Perturbaciones del espacio-tiempo que se propagan a velocidad c", "Partículas con carga eléctrica", "Rayos cósmicos"],
       "Analogía ondulatoria con el EM, pero sourced por masas aceleradas, no cargas."),
      ("Einstein predijo ondas gravitacionales pero dudó de medirlas porque:",
       ["No creía en su teoría", "Las amplitudes típicas son minúsculas (≈ fracción del tamaño atómico en LIGO)", "No existen en el vacío", "Viajan más lento que la luz"],
       "Hace falta un evento cataclísmico y detectores de interferometría ultraestables."),
      ("Para generar ondas gravitacionales detectables se necesita, en esencia:",
       ["Masas en reposo", "Masas muy compactas acelerándose violentamente (p. ej. binarias de BH o estrellas de neutrones)", "Solo campos magnéticos", "Polvo interestelar"],
       "Cuanto mayor la aceleración y la masa involucrada, mayor la luminosidad gravitacional.")],
     [("Compara ondas gravitacionales, electromagnéticas y mecánicas (sonido) en fuente, medio y velocidad.",
       "GW: masas aceleradas, se propagan en el espacio-tiempo mismo, v = c. EM: cargas aceleradas, campos E y B en el vacío, v = c. Mecánicas: perturbación de un medio material (aire, agua), velocidad del sonido ≪ c. Las GW no necesitan «medio material»; estiran y comprimen el espacio transversalmente a su propagación."),
      ("¿Qué es el «ringdown» en la señal de una fusión de agujeros negros?",
       "Tras la coalescencia queda un agujero negro único, deformado (sin esfericidad). Oscila y emite GW a frecuencias características del modo cuasinormal mientras «suena» hacia el equilibrio. En la curva de LIGO es la fase final después del chirp y el pico de fusión.")]),
    ("Hulse–Taylor y LIGO", "c,b,a",
     [("Hulse y Taylor (PSR B1913+16) demostraron indirectamente ondas gravitacionales al medir:",
       ["La luz del Sol deflectada", "El decrecimiento del período orbital de un binario de pulsares por pérdida de energía", "Neutrinos de una supernova", "El redshift de un cuásar"],
       "La órbita espirala hacia adentro exactamente como predice la emisión de GW → Nobel 1993."),
      ("LIGO detecta ondas gravitacionales midiendo:",
       ["La temperatura de los brazos", "Cambios diminutos en la longitud óptica de brazos perpendiculares por interferometría láser", "Partículas en una cámara de burbujas", "Solo ondas de radio"],
       "Una GW altera ligeramente la diferencia de camino óptico entre brazos de ~4 km."),
      ("Para confirmar un evento, LIGO compara señales de:",
       ["Un solo detector", "Al menos dos detectores separados (p. ej. Hanford y Livingston)", "Solo telescopios ópticos", "Un satélite GPS"],
       "Coincidencia temporal entre sitios distintos descarta ruido local (sísmico, vehículos, etc.).")],
     [("Explica por qué el binario de pulsares de Hulse–Taylor está «en espiral» y cómo eso apoya la existencia de ondas gravitacionales.",
       "Emiten GW y pierden energía orbital. Sin esa pérdida, una órbita kepleriana sería estable. El período medido disminuye ~76 μs/año, coincidiendo con la predicción de pérdida de energía por GW. No detectaron la onda directamente, pero el sistema pierde energía como si la emitiera."),
      ("¿Qué información extrae LIGO de la forma de la señal (chirp) de una fusión de agujeros negros?",
       "La frecuencia y amplitud crecen con el acercamiento («chirp»), codificando las masas (y spins) de los progenitores y la masa del remanente. De la amplitud y la distancia luminosa se infiere la distancia al evento. Por eso se catalogan masas ~10–100 M☉ distintas de las conocidas solo por EM.")]),
    ("Poblaciones de fusiones", "a,c,b",
     [("En el diagrama masas de fusiones detectadas por GW (azul) vs. agujeros negros vistos por EM (rojo):",
       ["Hay una población de BH más masivos detectada por GW que la típica de rayos X", "Son idénticas sin sesgo", "No se ha detectado ninguna fusión", "Solo existen BH de 3 M☉"],
       "El método GW selecciona eventos más masivos y a mayor distancia cósmica."),
      ("Una kilonova corresponde a:",
       ["Fusión de dos agujeros negros sin luz", "Fusión de dos estrellas de neutrones con emisión electromagnética transitoria", "Explosión de una enana blanca sola", "Un cometa"],
       "GW170817: onda gravitacional + contrapartida EM observada en muchos telescopios."),
      ("Los pulsares son útiles como relojes porque:",
       ["Emiten luz constante sin variación", "Su período de rotación es extremadamente estable", "No tienen campo magnético", "Son agujeros negros"],
       "Permiten medir parámetros orbitales con precisión de microsegundos.")],
     [("¿Por qué no todos los pulsares son estrellas de neutrones jóvenes, pero sí todos los pulsares son estrellas de neutrones (con campo activo)?",
       "Al nacer tras una supernova, la estrella de neutrones tiene campo intenso y emite haces rotatorios. El campo decae y el «faró» se apaga tras ~10⁷–10⁸ años: queda una estrella de neutrones sin pulsaciones. Un púlsar requiere SN joven + campo + geometría favorable."),
      ("Resume el multimensajero GW170817: qué se detectó y por qué fue histórico.",
       "LIGO/Virgo detectaron GW de una fusión de estrellas de neutrones; la localización permitió apuntar telescopios que vieron la kilonova en NGC 4993. Fue la primera fusión de estrellas de neutrones con contrapartida EM y confirmó que estos eventos producen elementos pesados (r-proceso) y ondas gravitacionales.")]),
    ("Tipos de ondas y energía", "b,d,a",
     [("Las ondas gravitacionales viajan a:",
       ["El doble de la velocidad de la luz", "La velocidad de la luz", "La velocidad del sonido", "Velocidad que depende de la frecuencia"],
       "Como predice la RG; medido consistente con c en GW170817 + gamma-ray burst."),
      ("La amplitud de una onda gravitacional decae con la distancia porque:",
       ["Las ondas no transportan energía", "La energía se reparte sobre un frente que crece (área ∝ r²)", "Se detienen a 1 parsec", "Se convierten en masa"],
       "Mismo principio que intensidad de ondas en un lago: misma energía en círculo mayor ⇒ menor amplitud local."),
      ("¿Cuál NO es una predicción estándar de relatividad general bien contrastada?",
       ["Deflexión de la luz", "Ondas gravitacionales", "Agujeros de gusano estables transitables listos para usar", "Redshift gravitacional"],
       "Los puentes Einstein–Rosen son soluciones matemáticas sin evidencia observacional.")],
     [("¿Por qué la fusión de dos agujeros negros es uno de los pocos fenómenos que produce GW detectables hoy?",
       "Combina masas grandes, separaciones pequeñas y velocidades orbitales cercanas a c justo antes de fusionar ⇒ aceleración quadrupolar enorme y luminosidad gravitacional pico. Eventos más suaves (p. ej. binarias amplias) emiten GW pero con amplitud irrisoria para LIGO."),
      ("Conecta la detección de GW con la idea de «nuevo canal de observación» en astronomía.",
       "Durante siglos la astronomía fue casi solo electromagnética (más neutrinos y rayos cósmicos recientemente). GW abren una ventana a objetos oscuros y procesos sin luz (fusiones de BH, interior de supernovas). Es como pasar de solo «ver» a también «oír» vibraciones del espacio-tiempo, con sesgos distintos al EM.")]),
    ("Integrador clase 1", "c,a,b",
     [("El año «milagroso» de Einstein (1905) incluyó trabajos sobre:",
       ["Solo relatividad general", "Efecto fotoeléctrico, movimiento browniano, relatividad especial y E=mc²", "Solo cosmología", "Solo mecánica cuántica completa"],
       "La relatividad general llegó en 1915; 1905 fue relatividad especial y equivalencia masa-energía."),
      ("La contracción de longitudes en relatividad especial afecta principalmente a:",
       ["Dimensiones perpendiculares al movimiento relativo", "Dimensiones paralelas al movimiento relativo", "Solo el tiempo", "Solo la masa"],
       "Un objeto en movimiento se acorta en la dirección del movimiento vista por un observador en reposo."),
      ("Júpiter deforma el espacio-tiempo más que la Tierra principalmente porque:",
       ["Está más caliente", "Es mucho más masivo", "Rota más rápido", "Tiene más lunas"],
       "La curvatura escala con la masa (y la compactidad); Júpiter ~318 M⊕.")],
     [("Traza el hilo conceptual de la clase 1: de «c constante» hasta «ondas gravitacionales detectadas».",
       "c invariante → espacio-tiempo relativo (RS) → equivalencia gravedad/aceleración → curvatura (RG) → predicciones (Mercurio, eclipse, lentes, redshift, GW) → detección indirecta (Hulse–Taylor) y directa (LIGO 2015+). Cada eslabón es una consecuencia o prueba de la misma geometría."),
      ("Desde ingeniería: ¿qué paralelo hay entre el interferómetro de LIGO y un sistema de medición de alta precisión con rechazo de ruido?",
       "LIGO compara dos longitudes ópticas en cuadratura; una señal física global (GW) cambia la diferencia de camino de forma coherente en ambos brazos según orientación, mientras el ruido local (térmico, sísmico) no correlaciona entre sitios separados. Es interferometría heterodina con requisito de estabilidad λ/10²¹: similar a extraer una señal débil correlacionando múltiples sensores y descartando fallas locales.")]),
]

M3C2 = [
    ("Schwarzschild y horizonte", "b,c,a",
     [("La solución de agujero negro estático sin carga ni rotación se debe a:",
       ["Newton en 1687", "Karl Schwarzschild (1916)", "Hubble en 1929", "Schmidt en 1963"],
       "En la transcripción aparece mal como «Churchill»; es Schwarzschild."),
      ("El radio de Schwarzschild (horizonte de eventos) para un BH sin rotación es:",
       ["r_s = GM/c", "r_s = 2GM/c²", "r_s = c²/2GM", "r_s = GM²/c"],
       "Para M☉, r_s ≈ 3 km."),
      ("El horizonte de eventos es:",
       ["Una superficie física dura que destruye todo al tocarla", "La esfera a partir de la cual ninguna señal puede escapar al exterior", "El centro singular del agujero", "Solo una convención óptica"],
       "Es un lugar de «no retorno» causal, no una membrana material.")],
     [("Si comprimieras el Sol hasta su radio de Schwarzschild (~3 km), ¿qué pasaría con la Tierra en órbita actual?",
       "La órbita terrestre (~1 UA) quedaría muy fuera del horizonte (3 km ≪ 1 UA). La Tierra seguiría orbitando un objeto de 1 M☉, pero extremadamente compacto. A esa distancia el campo es el mismo que el newtoniano de 1 M☉; lo extremo es la compacidad, no un cambio instantáneo de la órbita a 1 UA."),
      ("¿Por qué decimos que el «tamaño» observacional de un agujero negro es el horizonte y no la singularidad?",
       "La singularidad está oculta detrás del horizonte; por definición no podemos recibir información del interior. Lo observable son efectos en el exterior: acreción, lentes, órbitas de estrellas, GW. El horizonte marca la escala donde c deja de ser suficiente para escapar.")]),
    ("Compacidad", "a,c,b",
     [("Tres objetos de 1 M☉ (Sol, enana blanca, agujero negro) producen la misma curvatura lejos, pero cerca:",
       ["El agujero negro permite «caer» mucho más profundo en el pozo gravitacional", "Son idénticos en todos los radios", "El Sol curva más cerca", "La enana blanca no curva el espacio"],
       "Misma masa ⇒ mismo potencial a gran distancia; distinta compacidad ⇒ distinto campo a radios pequeños."),
      ("Una estrella de neutrones de ~1,4 M☉ tiene un radio típico de unos pocos km, comparable a:",
       ["El radio del Sol", "El horizonte de un agujero negro de masa similar", "La órbita de la Tierra", "Un átomo"],
       "Por eso acreción y campos intensos se parecen, salvo que la estrella de neutrones tiene superficie."),
      ("La densidad ρ = M/V explica por qué un agujero negro es extremo:",
       ["Porque tiene poca masa", "Porque concentra toda la masa en un volumen mínimo (horizonte pequeño)", "Porque no tiene gravedad", "Porque es hueco"],
       "No es la masa total sino M concentrada en poco radio lo que dispara g y efectos de marea.")],
     [("Compara qué le ocurre a un cuerpo que cae hacia una estrella de neutrones vs. un agujero negro de la misma masa.",
       "En ambos casos atraviesa un campo gravitatorio intenso. En la estrella de neutrones <strong>choca con superficie sólida</strong> y puede liberar energía (p. ej. rayos X). En el agujero negro cruza el horizonte y no hay retorno; la información que emitía deja de llegarnos."),
      ("¿Por qué el Sol «convertido» en agujero negro de 1 M☉ seguiría manteniendo las órbitas planetarias a primera orden?",
       "A distancias ≫ r_s, el campo gravitacional de una masa esférica depende solo de M total (teorema de la cáscara/newtoniano). Cambia la compacidad interna, no la masa exterior medida desde lejos. Solo cerca del horizonte los efectos relativistas fuertes importan.")]),
    ("Espaguetificación y soluciones exóticas", "c,b,a",
     [("La «espaguetificación» ocurre por:",
       ["Presión atmosférica", "Gradiente de la gravedad (fuerzas de marea) entre extremos del cuerpo", "Rotación únicamente", "Campos magnéticos débiles"],
       "La parte cercana al BH siente atracción mucho mayor que la lejana."),
      ("Los agujeros de gusano (puentes Einstein–Rosen):",
       ["Han sido usados rutinariamente en misiones espaciales", "Son soluciones matemáticas sin evidencia observacional de estabilidad física", "Fueron descubiertos por LIGO", "Son lo mismo que un agujero negro estelar"],
       "Útiles en ciencia ficción; no hay candidatos observacionales."),
      ("El ISCO (Innermost Stable Circular Orbit) es importante porque:",
       ["Es donde las órbitas circulares se vuelven inestables y el material cae", "Es la superficie del Sol", "Es el borde de la galaxia", "No existe en relatividad general"],
       "Dentro del ISCO, el gas en disco de acreción pierde estabilidad y cae rápido.")],
     [("Explica mareas terrestres con la fórmula newtoniana F ∝ 1/r² y con la intuición de espacio curvo.",
       "Newton: la Luna tira más fuerte del lado cercano que del lejano de la Tierra → estiramiento diferencial. GR: la curvatura del espacio-tiempo no es uniforme sobre un cuerpo extendido; pies y cabeza siguen geodésicas ligeramente distintas. Mismo fenómeno, lenguajes distintos."),
      ("¿Por qué la docente advierte que entrar en un agujero de gusano (si existiera) no sería viaje turístico?",
       "Las mareas cerca de la garganta ultracurvada destrozarían cualquier estructura cohesiva; lo que «saliera» sería material desintegrado. Además, requerirían materia exótica con presión negativa para ser transitables, algo no observado.")]),
    ("Remanentes estelares", "b,a,c",
     [("Una estrella como el Sol deja al morir principalmente:",
       ["Un agujero negro", "Una enana blanca tras fase de gigante roja y nebulosa planetaria", "Una estrella de neutrones", "Nada"],
       "Umbral de masa: Sol → enana blanca; masivas → SN → estrella de neutrones o BH."),
      ("Las estrellas de más de ~8–10 M☉ típicamente terminan en:",
       ["Solo enfriamiento lento", "Supernova y remanente compacto (estrella de neutrones o agujero negro)", "Fusión eterna de hidrógeno", "Se convierten en planetas"],
       "Vida corta en MS, núcleo masivo, colapso gravitacional."),
      ("Un remanente «muerto» ya no es estrella en sentido estricto porque:",
       ["No rota", "No genera energía por fusión nuclear en su centro", "No tiene masa", "No tiene gravedad"],
       "Estrella = objeto en equilibrio con fusión en el núcleo; enanas blancas, estrellas de neutrones inertes y BH no cumplen eso.")],
     [("Resume el diagrama evolutivo de la clase: baja masa vs. alta masa hasta el remanente.",
       "Baja masa (≲8 M☉): MS larga → gigante roja → AGB → nebulosa planetaria → enana blanca. Alta masa: MS breve → supergigante → supernova tipo II (típica) → estrella de neutrones si ~8–25 M☉ progenitor, o agujero negro si más masivo (límites dependen de metales y pérdida de masa)."),
      ("¿Por qué las estrellas masivas «saben» consumir combustible más rápido sin ser conscientes?",
       "Formulación física: mayor masa ⇒ mayor presión gravitatoria ⇒ mayor temperatura central ⇒ mayor tasa de fusión (y luminosidad L ∝ M⁴ en MS). El equilibrio hidrostático exige más energía nuclear; el depósito de H se agota en mucho menos tiempo (~10⁶ años para O vs. ~10¹⁰ para M☉).")]),
    ("Supernova 1987A", "c,b,a",
     [("SN 1987A explotó en:",
       ["La Vía Láctea", "La Gran Nube de Magallanes (satélite de la Vía Láctea)", "Andrómeda", "El centro del Universo"],
       "Supernova más cercana observada con telescopios modernos; visible desde Chile."),
      ("El «evento de neutrinos» de SN 1987A detectó del orden de:",
       ["Millones de neutrinos en todos los detectores", "Unos ~24 neutrinos en detectores terrestres (p. ej. Kamiokande, IMB)", "Cero neutrinos", "Solo rayos gamma"],
       "La mayoría de la energía de la colapso va en neutrinos; apenas unos pocos interactúan."),
      ("Los neutrinos de SN 1987A llegaron antes/casi simultáneos con la luz porque:",
       ["Viajan más rápido que c", "Salen del núcleo sin interactuar y la luz tarda en atravesar material opaco", "La luz no se emitió", "Los detectores fallaron"],
       "Neutrinos escapan del núcleo inmediatamente; la onda de choque ilumina la envoltura después.")],
     [("¿Cómo permitieron los neutrinos fechar con precisión la explosión de SN 1987A?",
       "El pico de detecciones marca el arribo a la Tierra. Con la distancia a la LMC (~50 kpc) y v ≈ c, se acota el instante de emisión. Coincide con la primera luz visible, validando modelos de colapso."),
      ("Describe la geometría observada años después (anillos) de SN 1987A.",
       "Hay un anillo central brillante y anillos externos: estructura de «reloj de arena» vista con inclinación. El material de la supernova interactúa con capas eyectadas antes de la explosión, iluminando anillos a distintas distancias del progenitor Sanduleak -69 202.")]),
    ("Detectar agujeros negros estelares", "a,b,c",
     [("La forma más directa de «ver» un agujero negro estelar activo es:",
       ["Estudiar la radiación del disco de acreción (gas caliente), no el horizonte", "Fotografiar la singularidad", "Ver rayos cósmicos del horizonte", "Medir su masa con una balanza"],
       "El gas fricciona, se calienta y emite (a menudo rayos X)."),
      ("Una binaria de rayos X requiere típicamente:",
       ["Dos agujeros negros lejanísimos", "Un compacto (BH o estrella de neutrones) + compañera que le transfiere masa", "Solo una estrella sola", "Un cuásar"],
       "La compañera llena el lóbulo de Roche y alimenta el disco."),
      ("En la Vía Láctea hay del orden de ~10⁸ agujeros negros estelares, pero solo ~200 binarias de rayos X conocidas porque:",
       ["No existen los demás", "Hace falta proximidad orbital y transferencia de masa activa", "Todos están apagados para siempre", "LIGO los oculta"],
       "Solo una fracción pequeña está en configuración que alimente acreción detectable.")],
     [("Explica el mecanismo de disco de acreción y por qué la zona interna emite rayos X.",
       "El gas con momento angular pierde energía por fricción viscosa (o magnetorrotacional), spiralando hacia adentro. Al caer en un pozo profundo, se calienta hasta millones de K en la parte interna → emisión térmica en rayos X. La eficiencia de conversión de energía gravitacional a radiación puede ser ≫ fusión nuclear."),
      ("¿Cómo distinguir observacionalmente un BH de una estrella de neutrones en una binaria de rayos X?",
       "Masa del compacto por dinámica orbital (función de masa > ~3 M☉ favorece BH). Límite de Eddington y variabilidad. En estrellas de neutrones puede haber erupciones tipo rayos X, líneas de cyclotron, o reflexión de superficie; un BH no tiene superficie y permite discos que se adentran hasta el ISCO más profundo.")]),
    ("SS 433 y jets", "b,c,a",
     [("SS 433 es famoso por:",
       ["Ser un cuásar", "Sus jets de material con precesión que dibujan un patrón de «sacacorcho»", "No emitir en radio", "Ser una galaxia entera"],
       "Binaria con agujero negro y chorros precesionantes observados en radio."),
      ("Los jets de agujeros negros estelares:",
       ["Salen del interior de la singularidad", "Se lanzan desde las inmediaciones del disco/acreción a velocidades relativistas", "Son solo polvo estático", "No existen"],
       "Mecanismo no del todo resuelto; involucra campos magnéticos y disco."),
      ("Observar jets en radio a menudo da la imagen más «limpia» porque:",
       ["El radio atraviesa polvo y ofrece alta resolución con interferometría", "No hay emisión en radio de otros objetos", "Los jets solo existen en radio", "El visible siempre es más brillante"],
       "VLBI permite ver estructura parsec a distancia galáctica.")],
     [("¿Qué es la precesión del disco/jet en SS 433 y cómo se ve en el cielo?",
       "El eje del disco no es fijo; precesa (~162 días), así que los jets pintan lóbulos en espiral (sacacorcho) en emisión de radio. Es evidencia de geometría y torques en el sistema binario."),
      ("Compara el jet cercano (radio) con el choque lejano (rayos X) en SS 433.",
       "Cerca del BH se ve el jet activo en radio. A ~25 pc el jet choca con el medio denso; el choque calienta gas y brilla en rayos X. Son fenómenos distintos: propagación vs. interacción con el ISM.")]),
    ("TDE y mareas galácticas", "a,c,b",
     [("Un TDE (tidal disruption event) ocurre cuando:",
       ["Una estrella pasa demasiado cerca de un agujero negro y es despedazada por mareas", "Dos galaxias fusionan sin efectos", "Un planeta nace", "Un púlsar deja de pulsar"],
       "Destrucción parcial o total; acreción transitoria durante semanas–años."),
      ("El cometa Shoemaker–Levy 9 se desintegró antes de chocar con Júpiter por:",
       ["Explosión nuclear", "Fuerzas de marea al pasar dentro del radio de Roche de Júpiter", "Viento solar únicamente", "Colisión con una luna"],
       "Fragmentos en fila impactaron Júpiter en 1994."),
      ("Las «colas de marea» del HI entre las Nubes de Magallanes y la Vía Láctea son:",
       ["Artefactos del telescopio", "Gas estirado por la interacción gravitacional", "Estrellas nuevas", "Cuásares"],
       "Visibles en la línea de 21 cm del hidrógeno neutro.")],
     [("Contrasta un TDE con una binaria de rayos X en duración y alimentación del agujero negro.",
       "Binaria de rayos X: transferencia de masa estable durante millones de años. TDE: evento único cuando una estrella solitaria pasa en órbita hiperbólica/pertenurbada demasiado cerca; flare luminoso transitorio y luego silencio."),
      ("Explica mareas en la Tierra más allá del océano.",
       "El campo de marea estira la Tierra elásticamente (deformación de fracciones de cm en la corteza). Océanos responden más porque son fluidos; pero toda la Tierra experimenta fuerzas de marea de Sol y Luna.")]),
    ("Agujeros negros supermasivos", "c,b,a",
     [("Los agujeros negros supermasivos (SMBH) típicamente tienen masas:",
       ["Menores que 1 M☉", "Del orden de millones a miles de millones de M☉", "Iguales a la masa de la Tierra", "Solo 3 M☉"],
       "M87 ~6×10⁹ M☉; Sgr A* ~4×10⁶ M☉."),
      ("Hasta donde sabemos, los SMBH se encuentran:",
       ["Uniformemente en el halo sin relación con galaxias", "En los núcleos de galaxias", "Solo en cúmulos globulares", "Flotando en el vacío intergaláctico"],
       "Coevolución galaxia–SMBH es tema activo de investigación."),
      ("En la Vía Láctea se estiman ~10⁸ agujeros negros estelares pero el SMBH central (Sgr A*) tiene ~4×10⁶ M☉. Esto muestra que:",
       ["No hay agujeros negros estelares", "Los SMBH son categoría distinta: mucho más masivos y en el núcleo", "Todos los estelares se fusionaron ya", "Sgr A* es una estrella de neutrones"],
       "Estelares = remanentes de estrellas; supermasivos = otro canal de crecimiento/acreción.")],
     [("Resume las dos vías de estudio de agujeros negros estelares vistas en clase (acreción vs. dinámica).",
       "1) <strong>Acreción</strong>: gas caliente en disco (binarias de rayos X, TDE). 2) <strong>Dinámica</strong>: medir velocidades de estrellas o gas orbitando un pozo gravitacional invisible (p. ej. estrellas cerca de Sgr A*)."),
      ("¿Por qué la docente dice que no estudia «los chiquititos» sino AGN?",
       "Su investigación se centra en núcleos activos de galaxias (SMBH alimentados), fenomenología de discos, corona y jets a escala galáctica, distinta de la población de remanentes estelares dispersos en el disco.")]),
    ("Quásares, AGN e integrador", "b,a,c",
     [("Los cuásares fueron nombrados originalmente de «quasi-stellar radio source» porque:",
       ["Eran planetas del Sistema Solar", "Parecían estrellas puntuales pero con fuerte emisión de radio", "No tenían redshift", "Eran nebulosas planetarias"],
       "QSO = cuasi estelares; muchos también muy luminosos en óptico."),
      ("Maarten Schmidt (1963) identificó las líneas espectrales de 3C 273 como:",
       ["Líneas desconocidas de un elemento nuevo", "Hidrógeno con gran redshift (objeto extragaláctico muy lejano)", "Solo polvo", "Rayos X solares"],
       "El corrimiento al rojo gigante explicaba líneas «desplazadas»."),
      ("El argumento de variabilidad Δt × c limita:",
       ["La masa del Universo", "El tamaño máximo de la región emisora responsable del cambio de brillo", "La velocidad de la luz", "La edad del Sol"],
       "Si algo cambia en tiempo Δt, no puede ser mayor que ~c·Δt (cota superior).")],
     [("Integra clase 2: desde Schwarzschild hasta AGN. ¿Cuál es el hilo conductor?",
       "GR predice objetos compactos → estrellas masivas los producen (supernovas) → los detectamos por acreción (binarias X, TDE) o dinámica → en el núcleo galáctico hay SMBH → cuando se alimentan, AGN/cuásares con discos y a veces jets; variabilidad y espectros revelan regiones sub-galácticas ultraluminosas."),
      ("¿Por qué la acreción sobre un SMBH es el mecanismo más eficiente de luminosidad conocido?",
       "Convierte energía gravitacional en radiación con eficiencia η hasta ~0,1 (Ṁc²), mucho mayor que fusión nuclear (~0,007). Un pozo profundo + gas con fricción puede liberar luminosidades que superan el brillo de toda una galaxia en una región del tamaño del Sistema Solar o menor.")]),
]


def main():
    for i, pack in enumerate(M3C1, 1):
        title, ans, mc, opens = pack
        render_exam("m3c1", i, title, "III", "1", mc, opens, ans.split(","))
        print("m3c1-examen-%02d.html" % i)
    for i, pack in enumerate(M3C2, 1):
        title, ans, mc, opens = pack
        render_exam("m3c2", i, title, "III", "2", mc, opens, ans.split(","))
        print("m3c2-examen-%02d.html" % i)


if __name__ == "__main__":
    main()
