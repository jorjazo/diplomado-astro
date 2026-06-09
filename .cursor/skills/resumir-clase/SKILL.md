---
name: resumir-clase
description: Use when the user asks to resumir, sintetizar, or resumir-clase for a diplomado astronomy lecture; when generating HTML apuntes, interactive practice exams, or study notes from ff/ transcriptions and diapos/ slide PDFs for estrellas, planetas, galaxias, or observación.
---

# Resumir Clase

## Overview

Convierte transcripción (`ff/`) + diapositivas (`diapos/`) en un **sitio HTML navegable** en `{curso}/m{modulo}/html/`. Actúa como profesor de astronomía (audiencia: ingeniería informática). Sigue `AGENTS.md`.

## Paso 0 — Contexto Obligatorio

**No generar nada** sin confirmar explícitamente:

- **Curso:** `estrellas` | `planetas` | `galaxias` | `observación`
- **Módulo:** `1` | `2` | `3`
- **Clase:** `1`–`5`

Preguntar lo que falte. Registrar `CURSO_DIR`, `MX` (`m1`…`m3`), `CX` (`m2c1`…).

## Paso 1 — Fuentes

Base: `{CURSO_DIR}/{MX}/`

| Tipo | Ubicación | Notas |
|------|-----------|-------|
| Transcripción | `ff/` | Patrones: `estrellas-{CX}.md`, `galaxias-{CX}.md`, `planetas-{CX}.md`, `Observacion-{CX}.md`; variantes con hash o `-01`/`-02`. Leer todas las partes. |
| Diapositivas | `diapos/` | PDF; nombres irregulares — buscar por glob, no asumir patrón fijo. |
| Contexto | `compendio.md`, `AGENTS.md` | Opcional: OpenStax vía `material externo/openstax-astronomy-2e-indice.md` (marcar como externo). |

Contrastar transcripción con diapositivas; corregir errores de voz y anotarlos.

## Paso 2 — Imágenes

```bash
mkdir -p "{CURSO_DIR}/{MX}/html/{CX}/assets"
pdftoppm -jpeg -r 150 "$PDF" "{CURSO_DIR}/{MX}/html/{CX}/assets/slide"
```

Solo diapositivas relevantes. JPEG en `assets/`, no base64 masivo.

## Paso 3 — Archivos de Salida

En `{CURSO_DIR}/{MX}/html/`:

- `index.html` — índice del módulo
- `{CX}-apuntes.html` — apuntes principales
- `{CX}-examen-01.html` … `{CX}-examen-10.html`

**Navegación obligatoria (rutas relativas):**

- Apuntes `#examenes` → cada examen
- Cada examen → apuntes `#examenes` + `index.html`
- `index.html` → apuntes de cada clase

## Paso 4 — Apuntes (`{CX}-apuntes.html`)

Incluir: hero (curso/módulo/clase), resumen, índice con anclas, secciones temáticas (orden pedagógico, no cronológico), `<figure>` con slides comentadas, **≥2 widgets interactivos** (ecuaciones, Doppler, escalas log, etc.), tabla de conceptos clave, sección `#examenes` con enlaces a los 10 exámenes, footer con fuentes y disclaimer de transcripción.

Pedagogía: intuición → formalismo; conexiones informática (señales, log, pipelines); distinguir clase / inferencia / externo.

Fórmulas: KaTeX CDN. Widgets: HTML+CSS+JS inline, sin APIs externas.

## Paso 5 — Exámenes (`{CX}-examen-NN.html`)

**10 archivos**, cada uno con **5 preguntas exactas:**

| 1–3 | Selección múltiple (4 opciones) | Autocorregibles con JS al pulsar «Corregir» |
| 4–5 | Respuesta escrita | Respuesta propuesta en `<details><summary>Ver respuesta propuesta</summary>…</details>` colapsada |

Preguntas del contenido de la clase; sin repetir entre exámenes. Enlace «Volver a apuntes» en cada examen.

## Paso 6 — Cierre

1. Actualizar `INDICE.md` con las rutas nuevas.
2. Verificar grafo de enlaces index ↔ apuntes ↔ exámenes.
3. Informar al usuario los archivos creados.

## Errores Frecuentes

| Error | Corrección |
|-------|------------|
| Sin curso/módulo/clase | Preguntar primero |
| Salida en `apuntes/` u otra ruta | Solo `html/` |
| Un solo HTML | 12 archivos por clase |
| Exámenes en markdown | HTML interactivo separado |
| ≠5 preguntas o ≠3 MC | 5 total: 3 MC + 2 escritas |
| Respuesta escrita visible | `<details>` colapsado |
| Sin enlaces bidireccionales | Apuntes ↔ exámenes ↔ index |
| Omitir `INDICE.md` | Siempre actualizar |

## Plantillas

Estructura HTML completa, JS de corrección y widgets: [plantilla-estructura.md](plantilla-estructura.md). Referencia visual: `estrellas/m2/apuntes/m2c1.html`.
