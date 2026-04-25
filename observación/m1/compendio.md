# Compendio de Estudio: Instrumentación y Métodos de Observación Astronómica, Módulo 1

Este compendio integra las diapositivas del módulo 1 de **Instrumentación y Métodos de Observación Astronómica** con las transcripciones disponibles. El foco es entender la luz como portadora de información, cómo se mide, qué distorsiona la atmósfera y cómo ubicamos objetos en el cielo.

## Fuentes y Cobertura

| Clase | Diapositivas | Transcripción | Cobertura |
| --- | --- | --- | --- |
| Clase 1 | `observación/m1/diapos/Modulo_I_Clase_1_La_luz.pdf` | No disponible | Parcial: solo diapositivas |
| Clase 2 | `observación/m1/diapos/Modulo_I_Clase_2_Espectro_Electromagn_tico.pdf` | No disponible | Parcial: solo diapositivas |
| Clase 3 | `observación/m1/diapos/Modulo_I_Clase_3_Atmosferas_y_lineas_espectrales.pdf` | No disponible | Parcial: solo diapositivas |
| Clase 4 | `observación/m1/diapos/Modulo_I_Clase_4_Sistemas_de_Coordenadas.pdf` | `observación/m1/ff/Observaci-n-m1c4-ccfdb902-799b.md` | Alta |
| Clase 5 | `observación/m1/diapos/Modulo_I_Clase_5_Sol_y_Luna.pdf` | `observación/m1/ff/Observaci-n-m1c5-7357ae05-3dd0.md` | Alta |

También existen en `observación/m1/ff/` dos transcripciones compartidas con planetas (`Planetas-y-Observaci-n-m1c31...` y `Planetas-y-observaci-n-m1c32...`). Se usan solo como apoyo para coordenadas, mareas y contexto de observación, no como núcleo de este compendio.

> Nota: las transcripciones son automáticas y pueden contener errores. Los procedimientos observacionales deben verificarse con apuntes, diapositivas y documentación técnica cuando se apliquen en práctica.

## Guía de Lectura

El módulo se puede leer como una cadena de medición:

1. La astronomía recibe información principalmente como luz.
2. La luz tiene naturaleza ondulatoria y corpuscular.
3. Los fotones se organizan en espectro, flujo, luminosidad y magnitudes.
4. La materia deja huellas por absorción, emisión, reflexión y refracción.
5. La atmósfera terrestre modifica lo que llega al detector.
6. Para observar, hay que saber dónde apuntar y cómo seguir el movimiento aparente del cielo.

## 1. Luz: Onda, Partícula e Información

La astronomía estudia el Universo principalmente a través de la luz. La historia de la luz muestra una tensión productiva entre modelos de onda y partícula. Newton defendía una interpretación corpuscular; Huygens, una ondulatoria. El experimento de Young en 1801 mostró interferencia, apoyando el carácter ondulatorio. Maxwell integró luz y electromagnetismo. Michelson-Morley y la relatividad especial mostraron que no se necesitaba un éter clásico.

El efecto fotoeléctrico devolvió el carácter corpuscular: la luz llega en cuantos de energía, fotones. La conclusión moderna no es elegir onda o partícula, sino aceptar que la descripción depende del fenómeno. Interferencia y difracción requieren lenguaje ondulatorio; energía discreta y detección individual requieren fotones.

Para ingeniería, se parece a usar dos modelos de una misma señal: una representación de onda para propagación e interferencia, y una representación discreta para eventos de detección y conteo.

## 2. Fotones, Frecuencia, Longitud de Onda y Energía

Un fotón se caracteriza por longitud de onda, frecuencia y energía. La velocidad de la luz conecta longitud de onda y frecuencia:

`c = lambda * nu`

La energía del fotón viene dada por:

`E = h * nu = h * c / lambda`

Por eso fotones de menor longitud de onda, como UV o rayos X, tienen mayor energía que fotones infrarrojos o de radio. Esta relación conecta espectro electromagnético, física atómica y observación astronómica.

Cuando hay muchos fotones hablamos de cantidades macroscópicas:

- **Luminosidad:** energía emitida por una fuente por unidad de tiempo.
- **Flujo:** energía que atraviesa un área por unidad de tiempo, por frecuencia o longitud de onda.
- **Espectro:** distribución de energía según longitud de onda o frecuencia.

El flujo decrece con el cuadrado de la distancia a una fuente, un principio central para interpretar brillo aparente.

## 3. Cuerpo Negro y Espectro Electromagnético

El cuerpo negro es un modelo ideal de radiación en equilibrio. Absorbe toda la radiación incidente y emite con una forma espectral que depende solo de temperatura. En la realidad no existen cuerpos negros perfectos, pero estrellas y planetas pueden aproximarse en ciertos rangos.

Tres ideas son especialmente importantes:

- La forma del espectro depende de la temperatura.
- El máximo de emisión se desplaza a longitudes de onda más cortas al aumentar temperatura.
- El flujo total emitido crece fuertemente con temperatura, asociado a `sigma T^4`.

El espectro electromagnético ordena desde rayos gamma y X hasta UV, visible, infrarrojo, microondas y radio. Cada banda responde a fenómenos distintos: altas energías para procesos violentos, visible para estrellas, infrarrojo para polvo y objetos fríos, radio para gas y campos magnéticos.

## 4. Magnitudes y Rango Dinámico

La escala de magnitudes viene de la antigüedad, pero fue formalizada como escala logarítmica. Cinco magnitudes corresponden a un factor 100 en flujo; una magnitud equivale aproximadamente a un factor 2,5.

La escala es inversa: una magnitud menor indica un objeto más brillante. El Sol tiene magnitud aparente muy negativa, las estrellas más débiles visibles a simple vista están cerca de magnitud 6, y observaciones profundas llegan a magnitudes alrededor de 30.

Esto es natural para datos con rangos dinámicos enormes. Para ingeniería informática, es similar a usar decibeles, escalas logarítmicas o normalizaciones para representar señales que varían por muchos órdenes de magnitud.

## 5. Líneas Espectrales

Los átomos tienen niveles de energía cuantizados. Cuando un electrón cambia de nivel, absorbe o emite un fotón con energía específica. Como los niveles dependen del átomo o ion, las líneas espectrales funcionan como huellas digitales químicas y físicas.

Las líneas pueden ser:

- **De emisión:** un gas caliente y tenue emite fotones en longitudes de onda particulares.
- **De absorción:** un gas más frío frente a una fuente continua absorbe longitudes de onda específicas.

Las leyes espectrales de Kirchhoff resumen estas situaciones. Además, las moléculas producen transiciones rotovibracionales, especialmente importantes en infrarrojo.

Una línea no solo identifica elementos. Su intensidad, anchura y desplazamiento pueden indicar temperatura, presión, densidad, turbulencia, rotación o velocidad radial por Doppler.

## 6. La Atmósfera Como Filtro y Perturbación

La atmósfera terrestre no es transparente ni estática. Absorbe fotones por moléculas como agua, ozono y otros componentes; emite radiación propia; y desvía la luz por turbulencia.

Esto introduce tres problemas observacionales:

- **Absorción atmosférica:** reduce o altera la señal. Requiere corrección telúrica, modelos atmosféricos y considerar masa de aire.
- **Emisión de cielo:** añade fondo. Puede restarse con técnicas de observación y calibración, especialmente en infrarrojo.
- **Seeing:** la turbulencia ensancha la imagen, típicamente en escalas de fracciones a pocos segundos de arco.

Incluso sin atmósfera, la resolución no sería infinita. La difracción impone un límite angular aproximado `1.22 lambda / D`, donde `D` es el diámetro de la apertura. En términos de procesamiento de señales, la atmósfera y el telescopio definen una función de dispersión de punto: la imagen registrada es una versión convolucionada del objeto real.

## 7. Coordenadas Celestes y Monturas

Para observar hay que ubicar objetos en la esfera celeste. El sistema ecuatorial usa:

- **Ascensión recta:** análoga a longitud, medida de 0 a 24 horas.
- **Declinación:** análoga a latitud, medida de -90 a +90 grados.

El cero de declinación es el ecuador celeste. La ascensión recta se referencia al nodo ascendente asociado al cruce entre ecuador y eclíptica. La eclíptica es el plano Tierra-Sol proyectado en el cielo y está inclinada cerca de 24 grados respecto al ecuador celeste.

El sistema horizontal depende del observador: altura y azimut cambian con lugar y tiempo. Por eso los sistemas de coordenadas se relacionan mediante rotaciones y se eligen según el objetivo: ecuatorial para catálogos y seguimiento, altazimutal para telescopios locales, eclíptico para dinámica del Sistema Solar, galáctico para estructura de la Vía Láctea.

Las monturas también reflejan esta geometría. Una montura ecuatorial alinea un eje con el eje de rotación terrestre, facilitando seguimiento con un solo movimiento. Una montura altazimutal es mecánicamente conveniente, pero requiere controlar ambos ejes y corregir rotación de campo.

## 8. Tiempo, Luna, Eclipses y Movimiento No Sideral

Observar requiere tiempo astronómico. El tiempo solar, civil, universal y sideral responden a referencias distintas. El tiempo sideral está asociado a qué ascensión recta cruza el meridiano local en un momento dado.

La Luna es un gran iluminador del cielo nocturno: aumenta el fondo, reduce contraste y condiciona qué observaciones conviene hacer. También produce eclipses lunares y solares. Los eclipses permiten ciencia: observación de corona solar, respuesta atmosférica terrestre y estudios de atmósferas o emisiones en cuerpos como Io.

No todo objeto se mueve como estrella fija. Planetas, asteroides, cometas y satélites tienen movimiento no sideral. Para observarlos se requieren efemérides y soluciones de mecánica celeste, por ejemplo con JPL Horizons.

La oblicuidad, la eclíptica, la precesión y los sistemas de coordenadas conectan la geometría del cielo con estaciones, zodiaco, movimiento solar aparente y planificación observacional.

## Conceptos Clave

- **Cuerpo negro:** radiador ideal cuyo espectro depende solo de temperatura.
- **Difracción:** límite físico de resolución angular por apertura finita.
- **Flujo:** energía recibida por unidad de área y tiempo.
- **Fotón:** cuanto de luz con energía `E = h nu`.
- **Magnitud:** escala logarítmica inversa de brillo.
- **Seeing:** degradación angular por turbulencia atmosférica.
- **Sistema ecuatorial:** coordenadas de ascensión recta y declinación.
- **Tiempo sideral:** referencia temporal asociada a la rotación de la esfera celeste.
- **Transición espectral:** salto cuantizado que produce línea de emisión o absorción.

## Preguntas de Repaso

1. ¿Por qué la luz necesita una descripción ondulatoria y corpuscular?
2. ¿Qué cambia físicamente entre un fotón de radio y uno de rayos X?
3. ¿Cuál es la diferencia entre luminosidad y flujo?
4. ¿Por qué la escala de magnitudes es logarítmica e inversa?
5. ¿Qué condiciones producen líneas de absorción versus emisión?
6. ¿Qué corrige una corrección telúrica?
7. ¿Por qué el seeing limita la resolución de una imagen?
8. ¿Qué ventaja tiene una montura ecuatorial para seguimiento?
9. ¿Por qué la Luna puede ser un problema o una oportunidad científica?

## Ejercicios Sugeridos

- Explicar `E = h nu` y `c = lambda nu` usando tres bandas: radio, visible y rayos X.
- Dibujar una cadena de observación: objeto, emisión, atmósfera, telescopio, detector, calibración.
- Comparar seeing atmosférico y difracción como dos límites distintos de resolución.
- Elegir un objeto y buscar sus coordenadas ecuatoriales; luego describir qué debe hacer un telescopio altazimutal para seguirlo.
- Diseñar una estrategia simple para observar un objeto débil evitando Luna brillante y alta masa de aire.

## Recursos Externos Recomendados

- JPL Horizons: efemérides y movimiento no sideral.
- SIMBAD y Aladin: búsqueda de objetos astronómicos y visualización de campos.
- PhET Blackbody Spectrum: simulador de cuerpo negro.
- ESO Observing Basics: introducción a seeing, masa de aire y planificación.
- Stellarium: simulador de cielo para practicar coordenadas, tiempo sideral y movimiento aparente.

## Notas de Incertidumbre

- No hay transcripciones locales para las clases 1, 2 y 3; esas secciones se basan principalmente en diapositivas.
- Las clases 4 y 5 tienen transcripción, pero algunas partes remiten a cálculos o procedimientos que se desarrollarán en módulos posteriores.
- Las transcripciones compartidas con planetas contienen material útil de coordenadas y mareas, pero no todo corresponde estrictamente al curso de observación.

