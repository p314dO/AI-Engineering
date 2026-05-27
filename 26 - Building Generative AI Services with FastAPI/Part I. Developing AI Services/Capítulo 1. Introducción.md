
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


## Sugerir soluciones contextualmente relevantes
Con frecuencia, te encontrarás con problemas específicos que no tienen una solución previamente establecida. Las soluciones a estos problemas no son obvias y requieren mucha investigación, ensayo y error, consulta con otros expertos y lectura. Los desarrolladores están familiarizados con esta situación, ya que encontrar soluciones relevantes a los problemas de programación puede ser complicado y no sencillo.

Esto se debe a que los desarrolladores deben resolver problemas teniendo en cuenta un contexto determinado. Un problema no puede definirse sin una descripción exhaustiva de las "circunstancias", y la "situación" surge en el _contexto_ .

En esencia, _el contexto_ reduce el número de posibles soluciones a un problema.

---

**# The Role of Context-Rich Prompts in Generative Models**
Cuando le indicas a un modelo que solo use unas pocas palabras clave, obtendrás una respuesta que puede o no satisfacer tu _intención_ . Para explicar por qué, veamos un motor de búsqueda y cómo funciona.

Google ha invertido mucho capital en desarrollar un motor de búsqueda capaz de inferir tu intención a partir de las pocas palabras clave que introduces en la barra de búsqueda. Los resultados te muestran páginas que se ajustan a tu intención.

Cuantas menos palabras clave proporciones, más difícil le resultará al motor de búsqueda inferir lo que buscas y mostrarte resultados relevantes. Por ejemplo, si buscas "corbatas", el motor de búsqueda debe hacer suposiciones e inferir que tu intención era comprar corbatas (prendas de vestir) en lugar de aprender sobre ellas. Si, en cambio, buscas "corbata Trinity" o "tipos de corbata", tu consulta tiene una intención educativa y Google puede mostrarte los resultados adecuados.

Esto también se aplica a los modelos generativos. Cuando se proporciona poco o ningún contexto como indicación al modelo, este debe inferir la intención y producir algo que probablemente esté correlacionado con ella. Una respuesta genérica sería la más adecuada para este tipo de consulta. Por eso, a menudo se obtiene una respuesta genérica al usar una palabra clave corta genérica, que consiste en una pequeña secuencia de palabras.

Cuanto más detalladas y contextualizadas sean tus consultas, mejores y más relevantes serán las respuestas de tu modelo. Por eso, las preguntas con contexto son cruciales para obtener resultados relevantes, específicos y de alta calidad al trabajar con modelos generativos.

---

Con los motores de búsqueda, se buscan fuentes de información con algunas palabras clave que pueden o no contener una solución relevante. Cuando los desarrolladores buscan soluciones, pegan registros de errores en Google y son redirigidos a sitios web de preguntas y respuestas sobre programación como [Stack Overflow](https://stackoverflow.com/) . Los desarrolladores deben entonces esperar encontrar a alguien que haya tenido el mismo problema en el mismo contexto y que haya proporcionado una solución. Este método para encontrar soluciones a problemas de programación no es muy eficiente. Es posible que como desarrollador no siempre encuentres la solución que buscas en estos sitios web.

Los desarrolladores recurren ahora a la IA generativa para resolver problemas de programación. Al proporcionar una descripción del contexto del problema, la IA puede generar posibles soluciones. Además, la integración con editores de código facilita enormemente la incorporación de este contexto a los modelos de lenguaje, algo imposible con búsquedas en Google o Stack Overflow. Estos modelos de IA generan soluciones contextualmente relevantes, basadas en un conocimiento adquirido a través de foros en línea y sitios web de preguntas y respuestas. Con las soluciones propuestas, se puede decidir cuál es la más adecuada.

Por este motivo, usar las herramientas de codificación de GenAI suele ser más rápido que buscar soluciones en foros y sitios web. Incluso [Stack Overflow, el sitio de preguntas y respuestas sobre programación](https://oreil.ly/nOX_K) , ha atribuido una disminución del tráfico superior a la media (aproximadamente un 14 %) a los desarrolladores que probaron el modelo de lenguaje y el generador de código GPT-4 tras su lanzamiento. Esta cifra podría ser mayor, ya que varios usuarios avanzados del sitio han comentado en la publicación del blog de la empresa que perciben una drástica reducción de la actividad de los usuarios. De hecho, se ha [registrado una disminución de aproximadamente el 60 % en las preguntas formuladas y en la actividad de votos positivos en el sitio](https://oreil.ly/P6Kur) , en comparación con 2018.

En cualquier caso, Stack Overflow sigue esperando que el tráfico fluctúe en el futuro con la introducción de herramientas de codificación GenAI que democratizan la codificación, expanden la comunidad de desarrolladores y crean nuevos desafíos de programación. El poder de los sitios de preguntas y respuestas reside no solo en encontrar la respuesta, sino también en comprender las discusiones circundantes y la importancia de citar las fuentes. [2](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch01.html#id470) Como resultado, estos sitios seguirán siendo un recurso invaluable para los desarrolladores debido a sus comunidades de expertos y contenido curado por humanos que mantiene la confianza en la corrección y calidad de las respuestas osoluciones. [3](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch01.html#id472)

## Personalización de la experiencia del usuario
Los clientes y usuarios de software moderno esperan cierto nivel de personalización e interactividad al utilizar aplicaciones modernas.

Al integrar modelos generativos, como un modelo de lenguaje, en las aplicaciones existentes, puedes innovar la forma en que los usuarios interactúan con el sistema. En lugar de la interacción tradicional de la interfaz de usuario, donde tienes que hacer clic en varias pantallas, puedes conversar en texto natural con un chatbot para solicitar la información que buscas o que se realice una acción en tu nombre. Por ejemplo, al navegar por un sitio web de planificación de viajes, puedes describir tus vacaciones ideales y pedirle al chatbot que prepare un itinerario basado en el acceso de la plataforma a aerolíneas, proveedores de alojamiento y la base de datos de ofertas de paquetes vacacionales. O, si ya has reservado unas vacaciones, puedes solicitar recomendaciones de lugares turísticos basadas en los detalles del itinerario de tu cuenta. El chatbot puede entonces describirte los resultados y pedirte tu opinión.

Estos modelos de lenguaje pueden funcionar como un asistente personal, formulando preguntas relevantes hasta que relacionan tus preferencias y necesidades específicas con un catálogo de productos para generar recomendaciones personalizadas. Estos asistentes virtuales comprenden tu intención y te sugieren opciones adecuadas a tu situación. Si no te convencen las sugerencias, puedes proporcionar comentarios para que podamos ajustarlas a tus preferencias.

En el ámbito educativo, estos modelos GenAI pueden utilizarse para describir o visualizar conceptos complejos adaptados a las preferencias y capacidades de aprendizaje de cada estudiante.

En los videojuegos y la realidad virtual (RV), la IA genómica se puede utilizar para construir entornos y mundos dinámicos basados ​​en las interacciones del usuario con la aplicación. Por ejemplo, en los juegos de rol (RPG), se pueden generar narrativas e historias de personajes sobre la marcha, a partir de las decisiones y opciones de diálogo del usuario en tiempo real, utilizando un modelo de lenguaje integrado. Este proceso crea una experiencia única para el jugador y los usuarios de estas aplicaciones.

## Minimizar la demora en la resolución de consultas de los clientes.
Además de los asistentes de usuario personalizados, las empresas suelen necesitar apoyo para gestionar un gran volumen de consultas de atención al cliente. Debido a este volumen, los clientes a menudo tienen que esperar largas colas o varios días hábiles antes de recibir respuesta. Asimismo, a medida que las empresas aumentan su complejidad operativa y su número de clientes, resolver las consultas de manera oportuna puede resultar más costoso y requerir una amplia capacitación del personal.

GenAI puede optimizar los procesos de atención al cliente tanto para los clientes como para las empresas. Ahora, los clientes pueden chatear o llamar a un modelo lingüístico capaz de acceder a bases de datos y fuentes relevantes para resolver consultas en cuestión de minutos, no de días. A medida que los clientes describen sus problemas, el modelo puede responder a estas consultas de acuerdo con las políticas de la empresa y dirigirlos a los recursos pertinentes cuando sea necesario.

Mientras que los chatbots tradicionales a menudo se basaban en un conjunto de reglas elaboradas manualmente y guiones predefinidos, los chatbots impulsados ​​por GenAI pueden ser mejores:

- Comprender el contexto de la conversación
- Considerar las preferencias del usuario
- Generar respuestas dinámicas y personalizadas
- Aceptar y adaptarse a los comentarios de los usuarios.
- Gestionar consultas inesperadas, en particular sobre conversaciones históricas o extensas.

Estos factores permiten que los chatbots de GenAI interactúen de forma más natural y variada con el cliente. Estos bots serán el primer punto de contacto para los clientes que deseen obtener respuestas rápidas a sus consultas antes de que sus casos sean derivados a un agente humano. Como cliente, también puede preferir hablar primero con uno de estos chatbots de GenAI si esto significa evitar largas colas y obtener una solución rápida.

Estos ejemplos apenas rozan la superficie de todas las funcionalidades que pueden integrarse en las aplicaciones existentes. Esta flexibilidad y agilidad de los modelos generativos abre un sinfín de posibilidades para nuevas aplicaciones en el futuro.

## Actuar como interfaz para sistemas complejos
Hoy en día, muchas personas aún enfrentan dificultades al interactuar con sistemas complejos como bases de datos o herramientas de desarrollo. Quienes no son desarrolladores pueden necesitar acceder a información o realizar tareas sin contar con las habilidades necesarias para ejecutar comandos en estos sistemas complejos. Los modelos LLM y GenAI pueden actuar como interfaz entre estos sistemas y sus usuarios.

Los usuarios pueden proporcionar instrucciones en lenguaje natural, y los modelos GenAI pueden escribir y ejecutar consultas en sistemas complejos. Por ejemplo, un gestor de inversiones puede solicitar a un bot GenAI que agregue el rendimiento de la cartera en la base de datos de la empresa sin necesidad de solicitar informes a especialistas. Otro ejemplo es la nueva herramienta de relleno generativo de Photoshop, que crea capas de imagen y realiza ediciones contextuales para usuarios que no dominan las diversas herramientas de Photoshop.

Varias startups de IA ya han desarrollado aplicaciones GenAI en las que los usuarios interactúan con un modelo de lenguaje en lenguaje natural para realizar acciones con las herramientas. Mediante el uso de modelos de lenguaje, estas startups están reemplazando flujos de trabajo complejos y la necesidad de navegar por múltiples pantallas de interfaz de usuario.

Si bien los modelos GenAI pueden funcionar como interfaz para sistemas complejos como bases de datos o API, los desarrolladores deberán implementar medidas de seguridad y protección, como se explica en [el Capítulo 9](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch09.html#ch09) sobre seguridad en IA. Estas integraciones deberán gestionarse cuidadosamente para evitar consultas maliciosas y vectores de ataque mediante modelos generativos en estos sistemas.

## Automatización de tareas administrativas manuales
En muchas empresas grandes y con larga trayectoria, suele haber varios equipos que realizan tareas administrativas manuales que son menos visibles para los equipos de atención al cliente y sus clientes.

Una tarea administrativa típica implica el procesamiento manual de documentos con diseños complejos, como facturas, órdenes de compra y comprobantes de pago. Hasta hace poco, estas tareas se realizaban mayoritariamente de forma manual, ya que el diseño y la organización de la información de cada documento pueden ser visualmente únicos, lo que requiere validación o aprobación humana. Además, cualquier software desarrollado para automatizar estos procesos podría ser frágil y exigir un alto nivel de precisión y exactitud, incluso en casos excepcionales.

Ahora, el lenguaje y otros modelos generativos permiten automatizar y mejorar aún más algunas partes de estos procesos manuales para lograr una mayor precisión. Si las automatizaciones existentes fallan debido a casos excepcionales o cambios en el proceso, los modelos de lenguaje pueden intervenir para verificar los resultados según ciertos criterios y subsanar las deficiencias o señalar elementos que requieran revisión manual.

## Ampliación y democratización de la generación de contenido
A la gente le encanta el contenido nuevo y siempre está buscando ideas para explorar. Ahora, los escritores pueden investigar y generar ideas al escribir una entrada de blog con la ayuda de las herramientas de GenAI. Al conversar con un modelo, pueden intercambiar ideas y generar esquemas.

El aumento de productividad en la generación de contenido es enorme. Ya no es necesario realizar tareas cognitivas tediosas como resumir investigaciones o reformular oraciones. El tiempo necesario para producir una entrada de blog de calidad se reduce drásticamente, de días a horas. En lugar de empezar desde cero, puedes centrarte en el esquema, la fluidez y la estructura del contenido antes de usar GenAI para completar los detalles. Cuando tienes dificultades para encontrar la secuencia de palabras adecuada para lograr claridad y brevedad, las herramientas de GenAI pueden ser de gran ayuda. Sin embargo, lo que hace que un texto sea interesante a menudo no es el contenido en sí, sino el estilo y la fluidez de la escritura.

Muchas empresas ya han comenzado a utilizar estas herramientas para explorar ideas y redactar documentos, propuestas, publicaciones en redes sociales y entradas de blog.

En resumen, estas son varias razones por las que creo que más desarrolladores integrarán las funciones de GenAI en sus aplicaciones en el futuro. La tecnología aún está en sus inicios y todavía hay muchos desafíos que superar antes de que GenAI pueda adoptarse de forma generalizada.

# Cómo crear un servicio de IA generativa
Los modelos generativos necesitan acceso a información contextual detallada para proporcionar respuestas más precisas y relevantes. En algunos casos, también pueden necesitar acceso a herramientas para realizar acciones en nombre del usuario; por ejemplo, para realizar un pedido mediante la ejecución de una función personalizada. Por lo tanto, es posible que deba crear API en torno a los modelos generativos (como adaptadores) para gestionar las integraciones con fuentes de datos externas (bases de datos, API, etc.) y controlar el acceso del usuario al modelo.

Para crear estos envoltorios de API, puede colocar modelos generativos detrás de un servidor web HTTP e implementar las integraciones, controles y enrutadores necesarios como se muestra en [la Figura 1-4](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch01.html#web_server) .

![[Pasted image 20260527120133.png]]

El servidor web controla el acceso a las fuentes de datos y al modelo. Internamente, el servidor puede consultar la base de datos y los servicios externos para enriquecer las solicitudes al usuario con información relevante y generar resultados más pertinentes. Una vez generados los resultados, la capa de control realiza una verificación mientras los enrutadores envían las respuestas finales al usuario.

---
###### Consejo
Incluso puedes ir un paso más allá configurando un modelo de lenguaje para construir una instrucción para otro sistema y pasársela a otro componente para ejecutar esos comandos, como interactuar con una base de datos o realizar una llamada a una API.

---

En resumen, el servidor web actúa como un intermediario crucial que gestiona el acceso a los datos, enriquece las indicaciones para el usuario y controla la calidad de los resultados generados antes de enviarlos a los usuarios. Además de proporcionar modelos generativos a los usuarios, este enfoque por capas mejora la relevancia y la fiabilidad de las respuestas de dichos modelos.

# ¿Por qué crear servicios de IA generativa con FastAPI?
Los servicios de IA generativa requieren frameworks web de alto rendimiento que funcionen como motores de backend para servicios y aplicaciones basados ​​en eventos. FastAPI, uno de los frameworks web más populares en Python, [puede competir](https://oreil.ly/LmEg7) en rendimiento con otros frameworks populares como _gin (Golang)_ o _express (Node.js)_ , a la vez que conserva la riqueza del ecosistema de aprendizaje profundo de Python. Los frameworks que no son de Python carecen de esta integración directa necesaria para trabajar con un modelo de IA generativa dentro de un mismo servicio.

Dentro del ecosistema de Python, existen varios frameworks web principales para la creación de servicios API. Las opciones más populares incluyen:

**Django**
Un framework completo que viene con todo lo necesario. Es un framework maduro con una gran comunidad y mucho soporte.

**Flask**
Un microframework web ligero y extensible.

**FastAPI**
Un moderno framework web diseñado para la velocidad y el rendimiento. Es un framework full-stack que viene con todo lo necesario.

FastAPI, a pesar de su reciente incursión en el mundo de los frameworks web de Python, ha ganado popularidad y reconocimiento. Al momento de escribir este artículo, FastAPI es el framework web de Python de mayor crecimiento en cuanto a descargas de paquetes y el segundo framework web más popular en GitHub. Su popularidad está en camino de superar a la de Django, a juzgar por su creciente número de [estrellas en GitHub](https://oreil.ly/8fRO2) (alrededor de 80 000 al momento de redactar este texto).

Entre los frameworks mencionados, Flask lidera en número de descargas de paquetes debido a su reputación, el soporte de su comunidad y su extensibilidad. Sin embargo, al ser un microframework web, incluye un número limitado de funciones predeterminadas, como la validación de esquemas.

Django también es popular para la creación de API (mediante Django Rest Framework) y aplicaciones monolíticas que siguen el patrón de diseño modelo-vista-controlador (MVC). Sin embargo, su soporte para API asíncronas es menos maduro, lo que puede generar limitaciones de rendimiento, además de añadir complejidad y sobrecarga a la creación de API ligeras.

En comparación con otros frameworks web, FastAPI ofrece varias funcionalidades integradas, como validación de datos, seguridad de tipos, documentación automática y un servidor web incorporado. Por ello, es posible que los desarrolladores familiarizados con Python estén migrando de frameworks más antiguos y con enfoques rígidos como Django a FastAPI. Supongo que la excepcional experiencia de desarrollo, la libertad creativa, el excelente rendimiento y la reciente compatibilidad con modelos de IA mediante eventos del ciclo de vida contribuyen a esta tendencia.

Este libro abarca los detalles de implementación para el desarrollo de servicios de IA generativa que pueden realizar acciones de forma autónoma e interactuar con servicios externos, todo ello impulsado por el marco web FastAPI.

Para que aprendas los conceptos relevantes, te guiaré a través de un proyecto final en el que podrás trabajar mientras lees el libro. ¡Veamos!

# ¿Qué impide la adopción de servicios de IA generativa?
Las organizaciones se enfrentan a diversos desafíos al adoptar servicios de IA generativa. Existen problemas relacionados con la inexactitud, la relevancia, la calidad y la coherencia de los resultados de la IA generativa. Además, preocupan la privacidad de los datos, la ciberseguridad y el posible abuso o mal uso de los modelos si se utilizan en producción. Por ello, las empresas aún no desean otorgar plena autonomía a estos modelos. Existe cierta reticencia a conectarlos directamente con sistemas sensibles, como bases de datos internas o sistemas de pago.

La integración del servicio de IA con los sistemas existentes, como bases de datos internas, interfaces web y API externas, puede resultar compleja. Esta integración puede ser difícil debido a problemas de compatibilidad, la necesidad de conocimientos técnicos, la posible interrupción de los procesos existentes, los intentos maliciosos contra estos sistemas y otras preocupaciones similares relacionadas con la seguridad y la privacidad de los datos.

Las empresas que deseen utilizar el servicio para aplicaciones de cara al cliente querrán coherencia y relevancia en las respuestas del modelo, y asegurarse de que los resultados no sean ofensivos ni inapropiados.

También existen limitaciones para producir contenido original y de alta calidad con estos modelos generativos. Como se mencionó anteriormente, estas herramientas GenAI conectan eficazmente diversas ideas y conceptos dentro de ciertos dominios. Sin embargo, no pueden generar ideas totalmente novedosas o nunca antes vistas; más bien, recombinan y reformulan información existente de una manera que parece novedosa. Además, siguen patrones comunes durante la generación, lo que puede resultar genérico, repetitivo y poco inspirador para su uso inmediato. Finalmente, pueden producir resultados que suenan plausibles pero que son completamente incorrectos e inventados, sin basarse en hechos ni en la realidad.

Algunos desafíos, como los relacionados con la privacidad y la seguridad de los datos, pueden resolverse aplicando las mejores prácticas de ingeniería de software, sobre las que encontrará más información en este libro. Para solucionar otros desafíos, es necesario optimizar las entradas de los modelos o ajustarlos (modificando sus parámetros mediante nuevos ejemplos en un caso de uso específico) para mejorar la relevancia, la calidad, la coherencia y la consistencia de los resultados.

# Descripción general del proyecto final

En este libro, te guiaré en la creación de un servicio de IA generativa utilizando FastAPI como marco web subyacente.

El servicio incluirá:
- Integración con múltiples modelos, incluyendo un modelo de lenguaje para generación de texto y chat, un modelo de audio para conversión de texto a voz y un modelo de difusión estable para generación de imágenes.
- Genera respuestas en tiempo real a las consultas del usuario en formato de texto, audio o imagen.
- Utilice la técnica RAG para "comunicarse" con los documentos cargados mediante una base de datos vectorial.
- Extrae información de la web y comunícate con bases de datos internas, sistemas externos y API para recopilar información suficiente al responder a consultas.
- Registrar historiales de conversaciones en una base de datos relacional.
- Autenticar a los usuarios mediante credenciales basadas en tokens e inicio de sesión con la identidad de GitHub.
- Restringir las respuestas en función de los permisos del usuario mediante mecanismos de autorización.
- Proporcionar la protección suficiente contra el mal uso y el abuso mediante Guardrails de seguridad.

Dado que este libro se centra en la creación de servicios API, aprenderá a utilizar el paquete Streamlit de Python y HTML básico para desarrollar interfaces de usuario. En aplicaciones reales, podrá integrar sus servicios de IA generativa con interfaces de usuario personalizadas creadas con bibliotecas como React o frameworks como Next.js para lograr modularidad, extensibilidad y escalabilidad.

# Resumen
En este capítulo, aprendiste sobre el concepto de IA generativa y cómo puede crear datos en diversas modalidades, como texto, audio, video, etc., utilizando patrones aprendidos en sus datos de entrenamiento. También viste varios ejemplos prácticos y casos de uso de esta tecnología, y por qué la mayoría de las aplicaciones futuras se basarán en las capacidades de la IA generativa.

También aprendiste cómo la IA genómica puede facilitar el proceso creativo, eliminar intermediarios, personalizar la experiencia del usuario y democratizar el acceso a sistemas complejos y a la generación de contenido. Además, se te presentaron varios desafíos que impiden la adopción generalizada de la IA genómica, junto con diversas soluciones. Finalmente, aprendiste más sobre el servicio API de IA genómica que desarrollarás con el framework web FastAPI siguiendo los ejemplos de código de este libro.

En el próximo capítulo, aprenderá sobre FastAPI, que le permitirá implementar sus propios servicios de GenAI.

