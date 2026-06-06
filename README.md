# Diplomado en Fundamentos de Astronomía

Este repositorio reúne material de estudio del **Diplomado en Fundamentos de Astronomía de la Universidad de Chile, versión 2026**.

El objetivo es conservar, ordenar y reutilizar el material de clases para estudiar con apoyo de agentes de IA, especialmente en sesiones donde el agente actúe como profesor de astronomía para una audiencia con formación en ingeniería en informática.

## Estructura del Diplomado

El diplomado está dividido en cuatro cursos:

- **Astrofísica de planetas**
- **Astrofísica de estrellas**
- **Astrofísica de galaxias**
- **Instrumentación y Métodos de Observación Astronómica**

Cada curso está dividido en módulos. Cada módulo contiene aproximadamente **5 clases**.

## Organización del Repositorio

La estructura esperada del repositorio sigue esta idea general:

```text
<curso>/
  m<numero-de-modulo>/
    ff/
      <transcripciones-de-audio>.md
    <audios-de-clases>
    <diapositivas>
    <material-complementario>
```

Actualmente el repositorio usa directorios por curso, por ejemplo:

- `planetas/`
- `estrellas/`
- `galaxias/`
- `observación/`

Dentro de cada curso, los módulos se nombran como `m1`, `m2`, etc. El directorio `ff/` contiene transcripciones generadas a partir de audios de clases cuando están disponibles.

El archivo `INDICE.md` mantiene el mapa por curso, módulo y clase, incluyendo fecha, tema, profesor/a, material disponible, objetivos de aprendizaje y recursos recomendados.

## Tipo de Material Guardado

En este repositorio se pueden guardar:

- Audios de clases, cuando estén disponibles.
- Transcripciones de esos audios, normalmente dentro de directorios `ff/`.
- Diapositivas usadas durante las clases.
- Material complementario recomendado por profesores o estudiantes.
- Índices de recursos externos transversales, guardados en `material externo/`.
- Apuntes personales, resúmenes, guías de estudio o preguntas para sesiones futuras.

## Uso con Agentes de IA

Este repositorio está pensado para iniciar sesiones de estudio asistidas por agentes. En esas sesiones, el agente debe actuar como **profesor de astronomía**, no solo como resumidor de documentos.

El agente debería:

- Explicar los contenidos con rigor conceptual, pero usando lenguaje claro.
- Considerar que la audiencia tiene estudios de ingeniería en informática.
- Relacionar ideas astronómicas con ejemplos computacionales, matemáticos, físicos o de sistemas cuando ayuden a entender mejor.
- Descomponer temas complejos en intuición, formalismo y ejemplos.
- Proponer ejercicios, preguntas de repaso y rutas de estudio.
- Complementar el material del repositorio con recursos externos confiables, como videos, textos, simuladores, sitios académicos o documentación técnica, en español o inglés.

Para instrucciones más detalladas para agentes, ver `AGENTS.md`.

## Sugerencias para Sacar Más Provecho

Para que el repositorio sea más útil en sesiones de estudio, convendría completar gradualmente:

- Una convención estable para nombrar archivos, por ejemplo `curso-m1c01-tema.ext`.
- Un archivo de apuntes por módulo con conceptos clave, dudas abiertas y preguntas de repaso.
- Referencias bibliográficas o enlaces recomendados por cada clase.
- Una lista de objetivos de aprendizaje por módulo.
- Indicación de qué material corresponde a clase, transcripción automática, resumen propio o recurso externo.
- Notas sobre el nivel de confianza de cada transcripción, especialmente si contiene errores de reconocimiento de voz.
- Enlaces desde compendios a recursos transversales como `material externo/openstax-astronomy-2e-indice.md`.

## Convención Recomendada para Futuras Sesiones

Al pedir ayuda a un agente, puede ser útil indicar:

1. Curso, módulo y clase que se quiere estudiar.
2. Archivos relevantes que debe revisar primero.
3. Nivel de profundidad deseado: resumen, explicación conceptual, derivación matemática, ejercicios o preparación para evaluación.
4. Si se quiere una explicación en español, inglés o bilingüe.
5. Qué tipo de apoyo externo se desea: videos, simuladores, textos, papers, sitios académicos o ejercicios.

