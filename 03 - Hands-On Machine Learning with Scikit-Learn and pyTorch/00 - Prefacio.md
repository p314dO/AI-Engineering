En 2006, Geoffrey Hinton y otros publicaron [un artículo](https://homl.info/hinton2006) 1 que mostraba cómo entrenar una red neuronal profunda capaz de reconocer dígitos escritos a mano con [una](https://learning.oreilly.com/library/view/hands-on-machine-learning/9798341607972/preface01.html#id742) precisión de vanguardia (>98%). Bautizaron esta técnica como "aprendizaje profundo".Una red neuronal profunda es un modelo (muy) simplificado de nuestra corteza cerebral, compuesto por una pila de capas de neuronas artificiales. Entrenar una red neuronal profunda se consideraba prácticamente imposible en aquel entonces, [y](https://learning.oreilly.com/library/view/hands-on-machine-learning/9798341607972/preface01.html#id744) la mayoría de los investigadores habían abandonado la idea a finales de la década de 1990. Este artículo reavivó el interés de la comunidad científica, y en poco tiempo muchos artículos nuevos demostraron que el aprendizaje profundo no solo era posible, sino capaz de lograr resultados asombrosos que ninguna otra técnica de aprendizaje automático (ML) podía igualar (con la ayuda de una enorme capacidad de cálculo y grandes cantidades de datos). Este entusiasmo pronto se extendió a muchas otras áreas del aprendizaje automático.

Una década después, el aprendizaje automático ya había conquistado muchas industrias: clasificaba resultados web, recomendaba vídeos y productos, ordenaba artículos en líneas de producción e incluso, en ocasiones, conducía coches. El aprendizaje automático solía ser noticia, por ejemplo, cuando el sistema AlphaFold de DeepMind resolvió un antiguo problema de plegamiento de proteínas que había desconcertado a los investigadores durante décadas. Pero la mayor parte del tiempo, el aprendizaje automático simplemente trabajaba discretamente en segundo plano. Sin embargo, otra década después surgió el auge de los asistentes de IA: desde ChatGPT en 2022, Gemini, Claude y Grok en 2023, y muchos otros desde entonces. La IA ha despegado definitivamente y está transformando rápidamente todas las industrias: lo que antes era ciencia ficción ahora es una realidad [.](https://learning.oreilly.com/library/view/hands-on-machine-learning/9798341607972/preface01.html#id745)

# Aprendizaje automático en tus proyectos
Así que, naturalmente, te entusiasma el aprendizaje automático y te encantaría unirte a la fiesta. ¿Quizás te gustaría dotar a tu robot casero de un cerebro propio? ¿Hacer que reconozca rostros? ¿O que aprenda a caminar?

O tal vez su empresa tenga muchísimos datos (registros de usuarios, datos financieros, datos de producción, datos de sensores de máquinas, estadísticas de la línea de atención al cliente, informes de recursos humanos, etc.), y lo más probable es que pueda descubrir información valiosa si sabe dónde buscar. Con el aprendizaje automático, podría lograr lo siguiente [y mucho más](https://homl.info/usecases) :

- Segmenta a tus clientes y encuentra la mejor estrategia de marketing para cada grupo.
- Recomendar productos a cada cliente en función de lo que hayan comprado clientes similares.
- Detectar qué transacciones tienen probabilidades de ser fraudulentas.
- Pronosticar los ingresos del próximo año.
- Predecir los picos de carga de trabajo y sugerir los niveles óptimos de personal.
- Crea un chatbot para ayudar a tus clientes.

Sea cual sea el motivo, has decidido aprender aprendizaje automático e implementarlo en tus proyectos. ¡Excelente idea!

# Objetivo y enfoque
Este libro parte de la base de que usted prácticamente no sabe nada sobre aprendizaje automático. Su objetivo es brindarle los conceptos, las herramientas y la intuición necesarios para implementar programas capaces de _aprender a partir de datos_ .

Cubriremos una gran variedad de técnicas, desde las más sencillas y comunes (como la regresión lineal) hasta algunas de las técnicas de aprendizaje profundo que suelen ganar competiciones. Para ello, utilizaremos Python, el lenguaje líder en ciencia de datos y aprendizaje automático, así como frameworks de Python de código abierto y listos para producción.

- [Scikit-Learn](https://scikit-learn.org/) Es muy fácil de usar y, a la vez, implementa muchos algoritmos de aprendizaje automático de manera eficiente, lo que lo convierte en un excelente punto de partida para aprender sobre aprendizaje automático. Fue creado por David Cournapeau en 2007, luego liderado por un equipo de investigadores del Instituto Francés de Investigación en Informática y Automatización (Inria), y más recientemente por Probabl.ai.
- [PyTorch](https://pytorch.org/) PyTorch es una biblioteca potente y flexible para el aprendizaje profundo. Permite entrenar y ejecutar todo tipo de redes neuronales de forma eficiente, y puede distribuir los cálculos entre múltiples GPU (unidades de procesamiento gráfico). PyTorch (PT) fue desarrollado por el laboratorio de investigación de IA de Facebook (FAIR) y se lanzó por primera vez en 2016. Evolucionó a partir de Torch, un marco de trabajo anterior programado en Lua. En 2022, PyTorch pasó a formar parte de la Fundación PyTorch, bajo la Fundación Linux, para promover el desarrollo impulsado por la comunidad.

También utilizaremos estas bibliotecas de aprendizaje automático de código abierto a lo largo del proceso:

- [](https://xgboost.readthedocs.io/)En [el capítulo 6 se utiliza](https://learning.oreilly.com/library/view/hands-on-machine-learning/9798341607972/ch06.html#ensembles_chapter) [XGBoost](https://xgboost.readthedocs.io/) para implementar una técnica potente llamada _potenciación de gradiente_ .
- [](https://huggingface.co/)[En los capítulos 13](https://learning.oreilly.com/library/view/hands-on-machine-learning/9798341607972/ch13.html#rnn_chapter) y [15,](https://learning.oreilly.com/library/view/hands-on-machine-learning/9798341607972/ch15.html#transformer_chapter) encontrará bibliotecas [de Hugging Face](https://huggingface.co/) para descargar conjuntos de datos y modelos preentrenados, incluidos modelos Transformer. Los Transformers son increíblemente potentes y versátiles, y constituyen el componente principal de prácticamente todos los asistentes de IA actuales.
- [Gymnasium](https://gymnasium.farama.org/) en [el Capítulo 19](https://learning.oreilly.com/library/view/hands-on-machine-learning/9798341607972/ch19.html#rl_chapter) para el aprendizaje por refuerzo (es decir, entrenamiento de agentes autónomos).


El libro apuesta por un enfoque práctico, desarrollando una comprensión intuitiva del aprendizaje automático a través de ejemplos concretos y solo un poco de teoría.

# Ejemplos de código

Todos los ejemplos de código de este libro son de código abierto y están disponibles en línea en [_https://github.com/ageron/handson-mlp_](https://github.com/ageron/handson-mlp) como cuadernos Jupyter. Se trata de documentos interactivos que contienen texto, imágenes y fragmentos de código ejecutable (Python en nuestro caso). La forma más fácil y rápida de empezar es ejecutar estos cuadernos con Google Colab: este es un servicio gratuito que permite ejecutar cualquier cuaderno Jupyter directamente en línea sin necesidad de instalar nada en tu ordenador. Solo necesitas un navegador web y una cuenta de Google.

---

En este libro, asumiré que utilizas Google Colab, pero también he probado los cuadernos en otras plataformas en línea como Kaggle y Binder, así que puedes usarlas si lo prefieres. Como alternativa, puedes instalar las bibliotecas y herramientas necesarias (o la imagen de Docker para este libro) y ejecutar los cuadernos directamente en tu ordenador. Consulta las instrucciones en [_https://homl.info/install-p_](https://homl.info/install-p) .

---

# Requisitos previos
Este libro presupone que tienes cierta experiencia programando en Python. Si aún no conoces Python, [_https://learnpython.org_](https://learnpython.org/) es un excelente punto de partida. El tutorial oficial de [Python.org](https://docs.python.org/3/tutorial) también es muy bueno.

Este libro también presupone que usted está familiarizado con las principales bibliotecas científicas de Python, en particular [NumPy](https://numpy.org/) , [pandas](https://pandas.pydata.org/) y [Matplotlib](https://matplotlib.org/) . Si nunca ha utilizado estas bibliotecas, no se preocupe; son fáciles de aprender y he creado un tutorial para cada una de ellas. Puede acceder a ellos en línea en [_https://homl.info/tutorials-p_](https://homl.info/tutorials-p) .

Además, si quieres comprender completamente cómo funcionan los algoritmos de aprendizaje automático (no solo cómo usarlos), debes tener al menos un conocimiento básico de algunos conceptos matemáticos, especialmente álgebra lineal. Específicamente, debes saber qué son los vectores y las matrices, y cómo realizar operaciones sencillas como sumar vectores o transponer y multiplicar matrices. Si necesitas una introducción rápida al álgebra lineal (¡no es tan complicado!), te ofrezco un tutorial en [_https://homl.info/tutorials-p_](https://homl.info/tutorials-p) . También encontrarás un tutorial sobre cálculo diferencial, que puede ser útil para comprender cómo se entrenan las redes neuronales, pero no es esencial para comprender los conceptos importantes. Este libro también utiliza ocasionalmente otros conceptos matemáticos, como exponenciales y logaritmos, un poco de teoría de la probabilidad y algunos conceptos básicos de estadística, pero nada demasiado avanzado. Si necesitas ayuda con alguno de estos temas, visita [_https://khanacademy.org_](https://khanacademy.org/) , que ofrece muchos cursos de matemáticas excelentes y gratuitos en línea.

---

# Hoja de ruta

Este libro está organizado en dos partes. [La Parte I, “Los fundamentos del aprendizaje automático ”](https://learning.oreilly.com/library/view/hands-on-machine-learning/9798341607972/part01.html#fundamentals_part) , abarca los siguientes temas:

- Qué es el aprendizaje automático, qué problemas intenta resolver y las principales categorías y conceptos fundamentales de sus sistemas.
- Los pasos en un proyecto típico de aprendizaje automático
- Aprendizaje mediante el ajuste de un modelo a los datos.
- Minimizar una función de coste (es decir, una medida de los errores de predicción)
- Manejo, limpieza y preparación de datos
- Selección y diseño de funcionalidades (es decir, campos de datos)
- Seleccionar un modelo y ajustar los hiperparámetros mediante validación cruzada (por ejemplo, entrenar muchas variantes del modelo y elegir la que mejor funcione con datos que no vio durante el entrenamiento).
- Los desafíos del aprendizaje automático, en particular el subajuste y el sobreajuste (la compensación entre sesgo y varianza).
- Los algoritmos de aprendizaje más comunes son: regresión lineal y polinómica, regresión logística, _k_ -vecinos más cercanos, árboles de decisión, bosques aleatorios y métodos de conjunto.
- Reducir la dimensionalidad de los datos de entrenamiento para combatir la “maldición de la dimensionalidad”.
- Otras técnicas de aprendizaje no supervisado, incluyendo agrupamiento, estimación de densidad y detección de anomalías.
    

[La segunda parte, “Redes neuronales y aprendizaje profundo”](https://learning.oreilly.com/library/view/hands-on-machine-learning/9798341607972/part02.html#neural_nets_part) , abarca los siguientes temas:

- Qué son las redes neuronales y para qué sirven
- Creación y entrenamiento de redes neuronales profundas utilizando PyTorch.
- Las arquitecturas de redes neuronales más importantes son: redes neuronales de propagación directa para datos tabulares; redes convolucionales para visión artificial; redes recurrentes y redes de memoria a corto y largo plazo (LSTM) para procesamiento de secuencias; codificadores-decodificadores, transformadores, modelos de espacio de estados (SSM) y arquitecturas híbridas para procesamiento del lenguaje natural, visión artificial y más; autoencoders, redes generativas antagónicas (GAN) y modelos de difusión para aprendizaje generativo.
- Cómo crear un agente (por ejemplo, un bot en un juego) que pueda aprender buenas estrategias mediante ensayo y error, utilizando el aprendizaje por refuerzo.
- Carga y preprocesamiento eficiente de grandes cantidades de datos

La primera parte se basa principalmente en Scikit-Learn; la segunda parte utiliza principalmente PyTorch.

---

###### Precaución

No te precipites: el aprendizaje profundo es, sin duda, una de las áreas más apasionantes del aprendizaje automático, pero primero debes dominar los fundamentos. Además, muchos problemas se pueden resolver con bastante eficacia utilizando técnicas más sencillas, como los bosques aleatorios y los métodos de conjunto (que se trataron en [la Parte I](https://learning.oreilly.com/library/view/hands-on-machine-learning/9798341607972/part01.html#fundamentals_part) ). El aprendizaje profundo es más adecuado para problemas complejos como el reconocimiento de imágenes, el reconocimiento de voz o el procesamiento del lenguaje natural, y suele requerir gran cantidad de datos, potencia de cálculo y paciencia (a menos que puedas aprovechar una red neuronal preentrenada, como verás).

---

Si le interesa especialmente un tema y quiere llegar a él lo antes posible, [la figura P-1](https://learning.oreilly.com/library/view/hands-on-machine-learning/9798341607972/preface01.html#chapter_dependencies_diagram) le mostrará qué capítulos debe leer primero y cuáles puede omitir sin problema.

![[Pasted image 20260322203639.png]]

---

# Otros recursos
Muchos recursos excelentesExisten recursos para aprender sobre aprendizaje automático. Por ejemplo, [el curso de Andrew Ng en Coursera](https://homl.info/ngcourse) es excelente, aunque requiere una inversión de tiempo considerable.

También hay muchos sitios web interesantes sobre aprendizaje automático, incluida la excepcional [Guía del usuario](https://homl.info/skdoc) de Scikit-Learn . También puede que le guste [Dataquest](https://dataquest.io/) , que proporcionatutoriales interactivos muy buenos, e infinidad de blogs y canales de YouTube sobre aprendizaje automático.

Existen muchos otros libros introductorios sobre aprendizaje automático. En particular:

- [_El libro "Data Science from Scratch"_](https://homl.info/grusbook) de Joel Grus , 2.ª edición (O'Reilly), presenta los fundamentos del aprendizaje automático e implementa algunos de los principales algoritmos en Python puro (desde cero, como su nombre indica).
- _El libro "Machine Learning: An Algorithmic Perspective"_ de Stephen Marsland , 2.ª edición (Chapman & Hall), es una excelente introducción al aprendizaje automático, que abarca una amplia gama de temas en profundidad con ejemplos de código en Python (también desde cero, pero utilizando NumPy).
- _El libro "Machine Learning with PyTorch and Scikit-Learn"_ de Sebastian Raschka , 1.ª edición (Packt Publishing), es también una excelente introducción al aprendizaje automático utilizando Scikit-Learn y PyTorch.
- _El libro Deep Learning with Python_ de François Chollet , 3.ª edición (Manning), es una obra muy práctica que abarca una amplia gama de temas de forma clara y concisa, como cabría esperar del autor de la excelente biblioteca Keras. Prioriza los ejemplos de código sobre la teoría matemática.
- El libro de Andriy Burkov, [_"The Hundred-Page Machine Learning Book_](https://themlbook.com/) " (publicado por el propio autor), es muy breve, pero abarca una impresionante variedad de temas, presentándolos en términos accesibles sin rehuir las ecuaciones matemáticas.
- _El libro Learning from Data_ (AMLBook) de Yaser S. Abu-Mostafa, Malik Magdon-Ismail y Hsuan-Tien Lin ofrece un enfoque más teórico del aprendizaje automático, proporcionando información valiosa, en particular sobre la relación entre sesgo y varianza (véase [el capítulo 4](https://learning.oreilly.com/library/view/hands-on-machine-learning/9798341607972/ch04.html#linear_models_chapter) ).
- _El libro *Inteligencia Artificial: Un Enfoque Moderno*_ , de Stuart Russell y Peter Norvig (Pearson), en su cuarta edición, es excelente (y muy extenso) y abarca una gran cantidad de temas, incluido el aprendizaje automático. Ayuda a comprender mejor el aprendizaje automático.
- [_El libro Deep Learning for Coders with fastai and PyTorch_](https://learning.oreilly.com/library/view/deep-learning-for/9781492045519/) (O'Reilly) , de Jeremy Howard y Sylvain Gugger, ofrece una introducción maravillosamente clara y práctica al aprendizaje profundo utilizando las bibliotecas fastai y PyTorch.
- _"Machine Learning Yearning",_ de Andrew Ng, es un libro electrónico gratuito que ofrece una exploración profunda del aprendizaje automático, centrándose en las consideraciones prácticas para la creación e implementación de modelos, incluyendo la calidad de los datos y el mantenimiento a largo plazo .
- [_El libro "Natural Language Processing with Transformers: Building Language Applications with Hugging Face"_](https://learning.oreilly.com/library/view/natural-language-processing/9781098136789/) (O'Reilly) , de Lewis Tunstall, Leandro von Werra y Thomas Wolf, es una excelente introducción práctica a los transformadores utilizando las populares bibliotecas de Hugging Face.
- _El libro "Hands-On Large Language Models"_ de Jay Alammar y Maarten Grootendorst es una obra bellamente ilustrada sobre modelos de lenguaje a gran escala (LLM, por sus siglas en inglés), que abarca todo lo que necesita saber para comprender, entrenar, ajustar y utilizar los LLM en una amplia variedad de tareas..

Por último, unirte a sitios web de competiciones de aprendizaje automático como [Kaggle.com](https://kaggle.com/) te permitirá practicar tus habilidades con problemas del mundo real, con la ayuda y los conocimientos de algunos de los mejores profesionales del aprendizaje automático.
