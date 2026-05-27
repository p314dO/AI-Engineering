
### Intro
Esta sección ofrece una introducción sencilla a los conceptos de GenAI y FastAPI, incluyendo los pasos necesarios para configurar un proyecto FastAPI que impulsará tu servicio generativo. Integrarás diversos modelos generativos en tu aplicación FastAPI y expondrás puntos de acceso para interactuar con ellos.

---
# Objetivos del capítulo

En este capítulo aprenderás sobre:
- Inteligencia artificial generativa (GenAI) y sus casos de uso.
- Por qué los servicios de GenAI impulsarán las aplicaciones del futuro.
- Las barreras para una mayor adopción de los servicios de IA
- Cómo crear un servicio GenAI
- Por qué FastAPI es una buena opción para crear servicios de GenAI
- Descripción general del proyecto final
---

Al finalizar este capítulo, usted debería ser capaz de identificar el papel de la IA GenAI dentro de la hoja de ruta de sus propias aplicaciones y los desafíos asociados.

# ¿Qué es la IA generativa?
_La IA generativa_ es un subconjunto del aprendizaje automático que se centra en la creación de contenido nuevo utilizando un modelo entrenado con un conjunto de datos. El _modelo entrenado_ , que es un modelo matemático que representa patrones y distribuciones en los datos de entrenamiento, puede producir nuevos datos similares al conjunto de datos de entrenamiento.

Para ilustrar estos conceptos, imagina entrenar un modelo con un conjunto de datos que contiene imágenes de mariposas. El modelo aprende las complejas relaciones entre los píxeles de las imágenes. Una vez entrenado, puedes usar el modelo para crear nuevas imágenes de mariposas que no existían en el conjunto de datos original. Estas imágenes tendrán similitudes con las originales, pero serán diferentes.

---
###### Nota
El proceso de utilizar un modelo generativo entrenado para crear contenido nuevo basado en patrones aprendidos a partir de los datos de entrenamiento se conoce como inferencia.

---

[La figura 1-1](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch01.html#generative_ai) muestra el proceso completo.
![[Pasted image 20260527021418.png]]

Dado que no queremos generar los mismos resultados que el conjunto de datos de entrenamiento, añadimos ruido aleatorio durante el proceso de muestreo para crear variaciones en los resultados. Este componente aleatorio que afecta a las muestras generadas hace que el modelo generativo _sea probabilístico_ . Esto distingue a un modelo generativo de una función de cálculo fija que, por ejemplo, promedia los píxeles de varias imágenes para crear otras nuevas.

Al trabajar en soluciones GenAI, puede encontrarse con seis familias de modelos generativos, entre las que se incluyen: [1](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch01.html#id448)

**Variational autoencoders (VAEs)**
Los VAEs aprenden a codificar datos en un espacio matemático de baja dimensión (llamado _espacio latente_ —véase [la figura 1-2—](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch01.html#latent_space) ) para decodificarlos de nuevo al espacio original al generar nuevos datos.

**Generative adversarial networks (GANs)**
Las GAN son un par de redes neuronales (un discriminador y un generador) que compiten entre sí para aprender patrones en los datos durante el entrenamiento. Una vez entrenadas, se puede usar el generador para crear nuevos datos.

**Autoregressive models**
Estos modelos aprenden a predecir el siguiente valor en una secuencia basándose en los valores anteriores.

**Normalizing flow models**
Estos modelos transforman distribuciones de probabilidad simples (patrones en los datos) en otras más complejas para generar nuevos datos.

**Energy-based models (EBMs)**
Los modelos basados ​​en la evidencia (EBM, por sus siglas en inglés) se basan en la mecánica estadística. Definen una función de energía que asigna menor energía a los datos observados y mayor energía a otras configuraciones, y se entrenan para diferenciar entre estas configuraciones.

**Diffusion models**
Los difusores aprenden a añadir ruido a los datos de entrenamiento para crear una distribución ruidosa pura. Luego, aprenden a eliminar gradualmente el ruido de los puntos muestreados (de la distribución ruidosa pura) para generar nuevos datos.

**Transformers**
Los transformadores pueden modelar grandes conjuntos de datos secuenciales, como corpus de textos, con un paralelismo extremadamente eficiente. Estos modelos utilizan un mecanismo _de autoatención_ para capturar el contexto y las relaciones entre los elementos de una secuencia. A partir de una nueva secuencia, pueden usar los patrones aprendidos para generar nuevas secuencias de datos. Los transformadores se utilizan habitualmente como _modelos de lenguaje_ para procesar y generar datos textuales, ya que manejan mejor las relaciones de largo alcance en el texto. ChatGPT de OpenAI es un modelo de lenguaje conocido como _transformador generativo preentrenado_ (GPT).

---

Los VAE pueden incrustar información en _espacios latentes_ , que son versiones matemáticas comprimidas de los datos de entrada que contienen la información más importante necesaria para reconstruir la entrada original. Las capas de codificación del modelo comprimen/codifican datos de alta dimensión en un espacio de menor dimensión (es decir, espacio latente) para una manipulación, análisis y reconstrucción de datos más eficientes, como se muestra en [la Figura 1-2](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch01.html#latent_space) .
![[Pasted image 20260527023145.png]]

###### Figura 1-2. Vista del espacio latente de un modelo generativo en VAE.
Utilizando este espacio latente, puedes navegar por él (mediante datos de entrada como texto o imágenes) para generar contenido nuevo que nunca existió en los datos de entrenamiento del modelo. Internamente, el proceso de muestreo selecciona un punto de datos para reconstruir, interpolando conceptos en la información aprendida del espacio latente.

---

Cabe destacar que estos modelos generativos suelen procesar únicamente ciertos tipos de datos o _modalidades_ , como texto, imágenes, audio, vídeo, nubes de puntos o incluso mallas 3D. Algunos son incluso _multimodales,_ como el GPT-4o de OpenAI, que puede procesar de forma nativa múltiples modalidades como texto, audio e imágenes.

Para explicar estos conceptos de GenAI, usaré como ejemplo la generación de imágenes. Otros ejemplos incluyen modelos de lenguaje como chatbots o analizadores de documentos, modelos de audio para la generación de música o síntesis de voz, y generadores de video para crear avatares de IA y deepfakes. Probablemente ya hayas visto muchos otros ejemplos, y aún quedan cientos por descubrir.

Una cosa es segura: los servicios de GenAI impulsarán las aplicaciones del futuro. Veamos por qué.

# Por qué los servicios de IA generativa impulsarán las aplicaciones del futuro

Utilizamos ordenadores para automatizar soluciones a problemas cotidianos.

En el pasado, automatizar un proceso requería codificar manualmente las reglas de negocio, lo cual podía ser lento y tedioso, especialmente para problemas complejos como la detección de spam cuando se dependía de reglas escritas a mano. Hoy en día, se puede entrenar un modelo para comprender los matices del proceso de negocio. Una vez entrenado, este modelo puede superar el rendimiento de las reglas escritas a mano implementadas como código de aplicación, lo que permite reemplazar dichas reglas.

Este cambio hacia la automatización basada en modelos ha dado lugar a aplicaciones con inteligencia artificial en el mercado, que resuelven diversos problemas, como la optimización de precios, la recomendación de productos o la previsión meteorológica. Como parte de esta tendencia, surgieron modelos generativos que se diferencian de otros tipos de IA por su capacidad para producir contenido multimedia (texto, código, imágenes, audio, vídeo, etc.), mientras que la IA tradicional se centra más en la predicción y la clasificación.

Como ingeniero de software, creo que estos modelos poseen ciertas capacidades que influirán en la hoja de ruta de desarrollo de futuras aplicaciones. Pueden:

- Facilitar el proceso creativo
- Sugiera soluciones que sean relevantes para el contexto.
- Personalizar la experiencia del usuario
- Minimizar la demora en la resolución de consultas de los clientes.
- Actuar como interfaz para sistemas complejos
- Automatizar tareas administrativas manuales
- Ampliar y democratizar la generación de contenido

Analicemos cada capacidad con más detalle.

## Facilitando el proceso creativo
Dominar habilidades y adquirir conocimientos requiere un gran esfuerzo cognitivo. Puedes dedicar mucho tiempo a estudiar y practicar algo antes de poder generar ideas originales para producir contenido novedoso y creativo, como un ensayo o un diseño.

Durante el proceso creativo, es posible que experimentes bloqueo creativo: dificultades para imaginar y visualizar escenas, organizar ideas, crear narrativas, construir argumentos y comprender las relaciones entre conceptos. El proceso creativo requiere una comprensión profunda del propósito de tu creación y una clara identificación de las fuentes de inspiración e ideas que utilizarás. A menudo, al sentarte a escribir algo nuevo, como un ensayo original, puede resultarte difícil comenzar desde una pantalla o una hoja en blanco. Necesitarás haber investigado a fondo el tema para haber formado tus propias opiniones y la narrativa que deseas plasmar.

El proceso creativo también se aplica al diseño, no solo a la escritura. Por ejemplo, al diseñar una interfaz de usuario, es posible que necesites varias horas de investigación, consultando sitios web de diseño para obtener ideas sobre la paleta de colores, la maquetación y la composición antes de comenzar el diseño. Crear algo verdaderamente original partiendo de cero puede ser una tarea titánica. Necesitarás inspiración y deberás seguir un proceso creativo.

Producir contenido original requiere creatividad. Por lo tanto, para los humanos, generar ideas originales desde cero es una hazaña extraordinaria. Las nuevas ideas y creaciones suelen basarse en inspiraciones, la conexión de ideas y la adaptación de otras obras. La creatividad implica un pensamiento complejo y no lineal, así como inteligencia emocional, lo que dificulta su replicación o automatización mediante reglas y algoritmos. Sin embargo, ahora es posible imitar la creatividad con inteligencia artificial generativa.

Las herramientas de GenAI pueden ayudarte a optimizar el proceso conectando diversas ideas y conceptos de un extenso repositorio de conocimiento humano. Con estas herramientas, puedes descubrir ideas novedosas que requieren comprender un amplio conjunto de conocimientos interconectados y las interacciones entre varios conceptos. Además, estas herramientas pueden ayudarte a visualizar escenas o conceptos difíciles de imaginar. Para ilustrarlo, intenta imaginar la escena descrita en [el Ejemplo 1-1](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch01.html#image_prompt) .

##### Ejemplo 1-1. Descripción de una escena que es difícil de visualizar para los humanos.
```
Un bosque biomecánico interminable donde los árboles tienen raíces metálicas y hojas de neón brillantes, cada tronco con engranajes giratorios y pantallas digitales que muestran glifos alienígenas; el suelo es una mezcla de tierra cristalina y venas orgánicas pulsantes, mientras que un cielo surrealista oscila entre una matriz de fallos digitales y una 
aurora centelleante hecha de luz líquida.
```

Puede resultar bastante difícil de imaginar a menos que uno esté acostumbrado a visualizar este tipo de conceptos. Sin embargo, con la ayuda de un modelo generativo, cualquiera puede ahora visualizar y comunicar conceptos complejos a los demás.

Al proporcionar la descripción de la escena del [Ejemplo 1-1](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch01.html#image_prompt) a una herramienta de generación de imágenes como [DALL-E 3 (OpenAI),](https://oreil.ly/Z80Qm) se obtiene un resultado que se muestra en [la Figura 1-3](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch01.html#dalle_image) .

![[Pasted image 20260527023852.png]]

Gemini
![[Pasted image 20260527023909.jpg]]

Es fascinante ver cómo estas herramientas de GenAI pueden ayudarte a visualizar y comunicar conceptos complejos. Te permiten expandir tu imaginación e impulsar tu creatividad. Cuando te sientas bloqueado o tengas dificultades para comunicar o imaginar ideas novedosas, puedes recurrir a estas herramientas en busca de ayuda.

En el futuro, preveo aplicaciones que incluyan funciones similares para ayudar a los usuarios en su proceso creativo. Si tus aplicaciones ofrecen varias sugerencias para que el usuario las desarrolle, esto puede facilitar su incorporación y generar impulso.
