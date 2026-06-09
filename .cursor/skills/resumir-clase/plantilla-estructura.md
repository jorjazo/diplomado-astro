# Plantillas HTML — Apuntes de Clase

Referencia para el skill `resumir-clase`. Copiar y adaptar por clase.

## index.html (módulo)

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Astrofísica de Estrellas — Módulo II — Apuntes HTML</title>
  <link rel="stylesheet" href="m2/shared.css"><!-- opcional -->
</head>
<body>
  <main>
    <h1>Módulo II — Apuntes HTML</h1>
    <p>Material de estudio generado a partir de transcripciones y diapositivas.</p>
    <ul>
      <li><a href="m2c1-apuntes.html">Clase 1 — El medio interestelar</a>
        (<a href="m2c1-apuntes.html#examenes">exámenes</a>)</li>
      <!-- repetir por cada clase con material -->
    </ul>
  </main>
</body>
</html>
```

## Esqueleto apuntes (`{CX}-apuntes.html`)

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{Título} — {TITULO_CURSO}, Módulo {N} · Clase {M}</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
  <style>/* tema oscuro, ver estrellas/m2/apuntes/m2c1.html */</style>
</head>
<body>
<main class="wrap">
  <nav class="top"><a href="index.html">← Módulo</a></nav>

  <header class="hero">
    <span class="kick">{TITULO_CURSO} · Módulo {N} · Clase {M}</span>
    <h1>{Título temático}</h1>
    <p class="sub">…</p>
  </header>

  <p class="lead">…</p>

  <nav class="idx"><ol><!-- anclas #s1, #s2 … --></ol></nav>

  <section id="s1">…</section>
  <!-- figuras con assets/slide-NN.jpg -->

  <section id="interactivo">
    <h2>Explorar conceptos</h2>
    <!-- widget 1, widget 2 -->
  </section>

  <section id="conceptos">…tabla…</section>

  <section id="examenes">
    <h2>Exámenes de práctica</h2>
    <p>10 exámenes de 5 preguntas (3 de alternativas autocorregibles, 2 de respuesta escrita).</p>
    <ol>
      <li><a href="m2c1-examen-01.html">Examen 1</a></li>
      <!-- … 02 … 10 -->
    </ol>
  </section>

  <footer>…fuentes y disclaimer transcripción…</footer>
</main>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script>/* render fórmulas, widgets */</script>
</body>
</html>
```

## Widget ejemplo — relación λ·ν = c

```html
<div class="widget" id="w-lambda-nu">
  <label>Longitud de onda λ (m): <input type="number" id="lambda" step="any" value="0.21"></label>
  <button type="button" id="calc-nu">Calcular ν y E</button>
  <output id="out-nu"></output>
</div>
<script>
const c = 299792458, h = 6.62607015e-34;
document.getElementById('calc-nu').onclick = () => {
  const lam = +document.getElementById('lambda').value;
  const nu = c / lam, E = h * nu;
  document.getElementById('out-nu').textContent =
    `ν = ${nu.toExponential(3)} Hz · E = ${E.toExponential(3)} J`;
};
</script>
```

## Esqueleto examen (`{CX}-examen-NN.html`)

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Examen {NN} — {CX}</title>
  <style>/* mismo tema que apuntes */</style>
</head>
<body>
<main>
  <nav>
    <a href="m2c1-apuntes.html#examenes">← Apuntes (exámenes)</a> ·
    <a href="index.html">Índice del módulo</a>
  </nav>
  <h1>Examen {NN} — {Título breve}</h1>

  <form class="quiz" id="quiz-01" data-answers="b,c,a">
    <fieldset data-q="1">
      <legend>1. (alternativas) …</legend>
      <label><input type="radio" name="q1" value="a"> A</label>
      <label><input type="radio" name="q1" value="b"> B</label>
      <label><input type="radio" name="q1" value="c"> C</label>
      <label><input type="radio" name="q1" value="d"> D</label>
    </fieldset>
    <!-- q2, q3 igual -->
    <button type="button" onclick="gradeQuiz('quiz-01')">Corregir alternativas</button>
    <p class="score" id="score-01" hidden></p>
  </form>

  <div class="q-open">
    <p><strong>4.</strong> (escrita) …</p>
    <details>
      <summary>Ver respuesta propuesta</summary>
      <div class="answer"><p>…</p></div>
    </details>
  </div>

  <div class="q-open">
    <p><strong>5.</strong> (escrita) …</p>
    <details>
      <summary>Ver respuesta propuesta</summary>
      <div class="answer"><p>…</p></div>
    </details>
  </div>
</main>
<script>
function gradeQuiz(id) {
  const form = document.getElementById(id);
  const ans = form.dataset.answers.split(',');
  let ok = 0;
  ans.forEach((a, i) => {
    const sel = form.querySelector(`input[name="q${i+1}"]:checked`);
    if (sel && sel.value === a) ok++;
  });
  const el = form.querySelector('.score');
  el.hidden = false;
  el.textContent = `Alternativas: ${ok} / ${ans.length}`;
}
</script>
</body>
</html>
```

## Convención de nombres

| Elemento | Patrón |
|----------|--------|
| Apuntes | `{CX}-apuntes.html` |
| Examen n | `{CX}-examen-{NN}.html` (NN = 01…10) |
| Assets | `{CX}/assets/slide-{NN}.jpg` |
| Enlaces internos | rutas relativas desde `html/` |

## Títulos de curso

| Directorio | Título |
|------------|--------|
| estrellas | Astrofísica de Estrellas |
| planetas | Astrofísica de Planetas |
| galaxias | Astrofísica de Galaxias |
| observación | Instrumentación y Métodos de Observación Astronómica |
