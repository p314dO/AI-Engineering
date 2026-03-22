
Existen cientos de bases de datos para elegir. ¿Cuál debería usar para su aplicación? La respuesta corta es: «Depende». La respuesta larga es… este libro.

Las distintas tecnologías para almacenar y procesar datos presentan diferentes ventajas y desventajas, y ningún enfoque es el mejor para todas las situaciones. Un sistema que se adapta perfectamente a una aplicación puede resultar inadecuado para otra. Este libro es una guía completa del panorama de los sistemas de datos, que no se limita a analizar un solo producto, sino que compara las fortalezas y debilidades de numerosos sistemas.

Aunque el panorama de las tecnologías para el procesamiento y almacenamiento de datos es diverso y evoluciona rápidamente, los principios fundamentales perduran. Si comprende estos principios, podrá identificar la función de cada herramienta, cómo aprovecharla al máximo y cómo evitar sus inconvenientes. Este libro se centra en dichos principios.

Si bien este libro no es un tutorial para usar una herramienta en particular, tampoco es un libro de texto repleto de teoría árida. En cambio, analizaremos numerosos ejemplos de sistemas de datos exitosos: tecnologías que constituyen la base de muchas aplicaciones populares y que deben cumplir diariamente con los requisitos de escalabilidad, rendimiento y confiabilidad en producción. Profundizaremos en el funcionamiento interno de estos sistemas, desglosaremos sus algoritmos clave y discutiremos las compensaciones que han tenido que realizar. En este recorrido, intentaremos encontrar formas útiles de _comprender_ los sistemas de datos, no solo _cómo_ funcionan, sino también _por qué_ funcionan de esa manera.

Tras leer este libro, estará en una excelente posición para determinar qué tecnologías son apropiadas para cada propósito y comprender cómo combinar herramientas para sentar las bases de una sólida arquitectura de aplicaciones. Desarrollará una gran intuición sobre el funcionamiento interno de sus sistemas, lo que le permitirá comprender su comportamiento, tomar buenas decisiones de diseño y detectar cualquier problema que pueda surgir.

La filosofía que guía este libro es reunir una amplia gama de perspectivas: tanto teóricas como prácticas, tanto recientes como antiguas. La industria informática suele sentirse atraída por lo novedoso y llamativo, y menospreciar las ideas consideradas antiguas o académicas. Esto es un error; muchas ideas fundamentales y poderosas en informática surgieron de la investigación, algunas recientes, otras de hace décadas. Por otro lado, el ámbito académico a veces carece de una idea clara de qué cuestiones son importantes en la práctica. Este libro combina lo mejor de ambos mundos: la precisión académica y la atención al detalle con un enfoque industrial centrado en la practicidad.

# ¿Quién debería leer este libro?

Si te identificas con alguna de las siguientes afirmaciones, este libro te resultará valioso:

- Eres ingeniero de software, arquitecto de software o gerente técnico y necesitas tomar decisiones sobre la arquitectura de los sistemas en los que trabajas; por ejemplo, necesitas elegir herramientas para resolver un problema determinado y averiguar la mejor manera de aplicarlas. Esto se aplica especialmente a los sistemas de backend.
    
- Eres un ingeniero de datos que desea comprender el contexto general de los sistemas con los que trabaja, o un ingeniero de la nube que busca información sobre los fundamentos de los sistemas que utiliza. Descubrirás que, si bien los sistemas distribuidos modernos ocultan gran parte de su complejidad, comprender sus principios subyacentes resulta extremadamente útil para la optimización del rendimiento y la depuración.
    
- Quieres aprender a hacer que los sistemas de datos sean escalables (por ejemplo, para dar soporte a aplicaciones con millones de usuarios), de alta disponibilidad (minimizando el tiempo de inactividad), operativamente robustos y más fáciles de mantener a largo plazo (incluso a medida que crecen y a medida que cambian los requisitos y las tecnologías).
    
- Te estás preparando para una entrevista de trabajo de "diseño de sistemas" en la que se te pedirá que diseñes la arquitectura de una aplicación, y necesitas aprender los principios de las buenas arquitecturas de datos.
    
- Sientes curiosidad por descubrir qué ocurre entre bastidores en los principales sitios web y servicios en línea, y dentro de diversas bases de datos y sistemas de procesamiento de datos, especialmente si te gusta profundizar más allá de las palabras de moda para obtener una comprensión técnica precisa y exacta de diversas tecnologías y sus ventajas e inconvenientes.
    

Este libro presupone que ya tienes experiencia en el desarrollo de aplicaciones web y que estás familiarizado con las bases de datos relacionales y SQL. Un conocimiento básico de protocolos de red comunes como TCP y HTTP resulta útil. El lenguaje de programación o el framework que utilices no influye en este libro.

# ¿Qué novedades incluye la segunda edición?

Esta segunda edición mantiene los mismos objetivos y alcance que la primera edición de _«Designing Data-Intensive Applications»_ , publicada en 2017. Sin embargo, hemos revisado exhaustivamente todo el libro para reflejar los cambios tecnológicos ocurridos en la última década y mejorar la claridad de las explicaciones.

Los cambios técnicos más significativos que han afectado a este libro desde su primera edición son el auge del interés en la IA y el desarrollo de arquitecturas de sistemas de datos nativas de la nube. Si bien este libro no trata sobre IA propiamente dicha, hemos incorporado información sobre sistemas de datos que dan soporte a la IA y al aprendizaje automático, incluyendo índices vectoriales (utilizados para la búsqueda semántica), DataFrames (utilizados para conjuntos de datos de entrenamiento) y sistemas de procesamiento por lotes para preparar grandes cantidades de datos de entrenamiento. A lo largo del libro, se han integrado conceptos propios de la nube, como la creación de sistemas de datos sobre almacenes de objetos en lugar de discos locales.

También hemos añadido discusiones sobre motores de sincronización y software con prioridad local, motores de flujo de trabajo y ejecución duradera, métodos formales y pruebas aleatorias, GraphQL y otras tecnologías que vale la pena conocer. Asimismo, hemos incluido un poco de contexto legal, explorando el impacto del Reglamento General de Protección de Datos (RGPD) de la UE y la legislación relacionada. También hemos eliminado algunas cosas; por ejemplo, dado que MapReduce está prácticamente obsoleto, hemos reescrito el capítulo sobre procesamiento por lotes y, lamentablemente, hemos decidido eliminar los mapas al estilo Tolkien.

Se han reestructurado algunos apartados y se ha modificado la numeración de los capítulos. Algunos capítulos solo requirieron una ligera revisión, mientras que otros (como [el capítulo 10](https://learning.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/ch10.html#ch_consistency) , sobre coherencia y consenso) se reescribieron casi por completo para mayor claridad. En total, la segunda edición es aproximadamente 60 páginas más larga que la primera.

# Referencias y lecturas adicionales

La mayor parte de lo que se trata en este libro ya se ha mencionado en otros lugares, de una u otra forma: en presentaciones de conferencias, artículos de investigación, entradas de blog, código, sistemas de seguimiento de errores, listas de correo o en la jerga de la ingeniería. Este libro resume las ideas más importantes de diversas fuentes e incluye referencias a la bibliografía original a lo largo del texto. Las referencias al final de cada capítulo son excelentes recursos para profundizar en algún tema, y ​​la mayoría están disponibles gratuitamente en línea.

En las ediciones digitales, hemos incluido enlaces al texto completo de los recursos en línea. Dado que los enlaces suelen romperse con frecuencia debido a la naturaleza de la web, también hemos incluido enlaces de archivo siempre que ha sido posible. Si encuentra un enlace roto o si está leyendo una copia impresa de este libro, puede usar un buscador para consultar las referencias. Para artículos académicos, busque el título en Google Scholar para encontrar archivos PDF de acceso abierto (gratuitos). Los libros pueden costar dinero, pero no debería tener que pagar por los artículos de investigación.

Como alternativa, puedes encontrar todas las referencias en [_https://github.com/ept/ddia2-references_](https://github.com/ept/ddia2-references) , donde mantenemos enlaces actualizados.