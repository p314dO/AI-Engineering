
---

**Objetivos del capítulo**

En este capítulo aprenderás sobre:
- Cómo funcionan los diferentes modelos de GenAI
- Cómo integrar y servir modelos generativos en FastAPI
- Cómo trabajar con texto, imágenes, audio, vídeo y modelos 3D.
- Cómo crear rápidamente una interfaz de usuario para la creación de prototipos
- Varias estrategias de modelado en FastAPI
- Cómo aprovechar el middleware para la monitorización de servicios

---

En este capítulo, aprenderá los mecanismos de varios modelos GenAI y cómo implementarlos en una aplicación FastAPI. Además, utilizando el [paquete Streamlit UI](https://oreil.ly/9BXmn) , creará un cliente web sencillo para interactuar con los puntos finales de implementación de modelos. Exploraremos diferentes estrategias de implementación de modelos, cómo precargar modelos para mayor eficiencia y cómo usar las funciones de FastAPI para la monitorización del servicio .

Para consolidar lo aprendido en este capítulo, construiremos progresivamente un servicio FastAPI utilizando modelos GenAI de código abierto que generan texto, imágenes, audio y geometrías 3D, todo desde cero. En capítulos posteriores, desarrollarás la funcionalidad para analizar documentos y contenido web para tu servicio GenAI, de modo que puedas interactuar con ellos mediante un modelo de lenguaje.

---

Al finalizar este capítulo, dispondrá de un servicio FastAPI que ofrece diversos modelos GenAI de código abierto que podrá probar en la interfaz de usuario de Streamlit. Además, su servicio podrá registrar datos de uso en disco mediante middleware.

# Al servicio de los modelos generativos
Antes de implementar modelos generativos preentrenados en tu aplicación, conviene comprender cómo se entrenan y generan datos. Con este conocimiento, podrás personalizar el funcionamiento interno de tu aplicación para optimizar los resultados que ofreces al usuario.

En este capítulo, les mostraré cómo servir modelos a través de una variedad de modalidades, que incluyen:

- _Modelos de lenguaje_ basados ​​en la arquitectura de red neuronal Transformer
- _Modelos de audio_ en servicios de conversión de texto a voz y texto a audio basados ​​en la arquitectura de transformador agresivo.
- _Modelos de visión_ para servicios de conversión de texto a imagen y texto a vídeo basados ​​en las arquitecturas de difusión estable y transformador de visión.
- _Modelos 3D_ para servicios de conversión de texto a 3D basados ​​en la arquitectura de codificador de función implícita condicional y decodificador de difusión.

Esta lista no es exhaustiva y abarca solo algunos modelos de GenAI. Para explorar otros modelos, visite el [repositorio de modelos de Hugging Face](https://oreil.ly/-4wlQ) .

## Language Models
En esta sección, hablamos de modelos de lenguaje, incluyendo transformadores y redes neuronales recurrentes (RNN).

### Transformers frente a Recurrent Neural Networks
El mundo de la IA se vio sacudido con la publicación del artículo trascendental "Attention Is All You Need".² [En](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#id631) este artículo, los autores propusieron un enfoque completamente diferente para el procesamiento del lenguaje natural (PLN) y el modelado de secuencias que se diferenciaba de las arquitecturas RNN existentes.

[La figura 3-1](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#transformer_architecture) muestra una versión simplificada de la arquitectura del transformador propuesta en el artículo original.
![[Pasted image 20260528122345.png]]

Históricamente, las tareas de generación de texto utilizaban modelos RNN para aprender patrones en datos secuenciales, como texto libre. Para procesar texto, estos modelos lo dividen en fragmentos pequeños, como palabras o caracteres llamados _tokens_ , que pueden procesarse secuencialmente.

Las redes neuronales recurrentes (RNN) mantienen un almacén de memoria llamado _vector de estado_ , que transporta información de un token al siguiente a lo largo de toda la secuencia de texto, hasta el final. Esto significa que, al llegar al final de la secuencia de texto, el impacto de los primeros tokens en el vector de estado es mucho menor en comparación con el de los tokens más recientes.

Idealmente, cada token debería ser tan importante como los demás en cualquier texto. Sin embargo, dado que las redes neuronales recurrentes (RNN) solo pueden predecir el siguiente elemento en una secuencia analizando los elementos anteriores, tienen dificultades para capturar dependencias a largo plazo y modelar patrones en grandes fragmentos de texto. Como resultado, no logran recordar ni comprender información o contexto esenciales en documentos extensos.

Con la invención de los transformadores, el modelado recurrente o convolucional podría ahora sustituirse por un enfoque más eficiente. Dado que los transformadores no mantienen una memoria de estado oculta y aprovechan una nueva capacidad denominada _autoatención_ , pueden modelar relaciones entre palabras, independientemente de la distancia que las separe en una oración. Este componente de autoatención permite que el modelo centre su atención en las palabras contextualmente relevantes dentro de una oración.

Mientras que las redes neuronales recurrentes (RNN) modelan las relaciones entre palabras vecinas en una oración, los transformadores representan las relaciones por pares entre cada palabra del texto.

[La figura 3-2](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#rnn_vs_transformer) muestra cómo las redes neuronales recurrentes (RNN) procesan las oraciones en comparación con los transformadores.
![[Pasted image 20260528122627.png]]


El sistema de autoatención funciona gracias a bloques especializados llamados __attention heads__ , que capturan patrones de pares de palabras como __attention maps__ .

[La figura 3-3](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#head_attention_map) muestra el mapa de atención de un centro de atención. [Las](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#id635) conexiones pueden ser bidireccionales, y el grosor representa la fuerza de la relación entre las palabras de la oración.
![[Pasted image 20260528122746.png]]
Un modelo Transformer contiene varias unidades de atención distribuidas entre las capas de su red neuronal. Cada unidad calcula su propio mapa de atención de forma independiente para capturar las relaciones entre las palabras, centrándose en ciertos patrones en las entradas. Mediante el uso de múltiples unidades de atención, el modelo puede analizar simultáneamente las entradas desde diversos ángulos y contextos para comprender patrones y dependencias complejos dentro de los datos.

[La figura 3-4](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#model_attention_map) muestra los mapas de atención para cada cabeza (es decir, un conjunto independiente de pesos de atención) dentro de cada capa del modelo.

![[Pasted image 20260528122931.png]]

Las redes neuronales recurrentes (RNN) también requerían una gran capacidad de procesamiento para su entrenamiento, ya que el proceso no podía paralelizarse en múltiples GPU debido a la naturaleza secuencial de sus algoritmos. Los transformadores, por otro lado, procesan las palabras de forma no secuencial, por lo que pueden ejecutar mecanismos de atención en paralelo en las GPU.

La eficiencia de la arquitectura Transformer implica que estos modelos son más escalables siempre que haya más datos, capacidad de procesamiento y memoria. Se pueden crear modelos de lenguaje con un corpus que abarque bibliotecas enteras de libros producidos por la humanidad. Solo se necesita una gran capacidad de procesamiento y datos para entrenar un modelo de lenguaje. Y eso es precisamente lo que hizo OpenAI, la empresa detrás de la famosa aplicación ChatGPT, que se basaba en varios de sus modelos de lenguaje patentados, incluido GPT-40.

Al momento de escribir este artículo, los detalles de implementación de los modelos LLM de OpenAI siguen siendo un secreto comercial. Si bien muchos investigadores tienen un conocimiento general de los métodos de OpenAI, es posible que no cuenten con los recursos necesarios para replicarlos. Sin embargo, desde entonces se han lanzado varias alternativas de código abierto para investigación y uso comercial, como Llama (Facebook), Gemma (Google), Mistral y Falcon, entre otras. [Al](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#id637) momento de escribir este artículo, el tamaño de los modelos varía entre 0,05 mil millones y 480 mil millones de parámetros (es decir, pesos y sesgos del modelo) para adaptarse a sus necesidades.

---

**Requisitos de hardware para LLM de código abierto**
En el momento de escribir este artículo, el sistema LLM de código abierto más importante es [_Snowflake Arctic_](https://oreil.ly/DLukR) , un sistema multilingüe de 480 mil millones de parámetros . El hardware recomendado para ejecutar este modelo masivo es una única instancia AWS/Azure 8xH100, que contiene ocho tarjetas GPU H100 para centros de datos, cada una con 80 GB de VRAM. Otros modelos LLM abiertos de referencia, como Llama 3.1, multilingüe y con 405 mil millones de parámetros, también requieren un hardware similar.

A partir de enero de 2024, una de las mejores tarjetas gráficas de consumo disponibles para cargas de trabajo de IA es la NVIDIA 4090 RTX, que viene con tan solo 24 GB de VRAM. Una sola GPU de consumo como la 4090 RTX podría no ser capaz de ejecutar modelos de más de 30 bytes debido a limitaciones de memoria, a menos que el modelo esté cuantizado (es decir, comprimido).

Si desea ejecutar un modelo cuantizado de 70 mil millones de llamas, es posible que necesite una [GPU con 64 GB de VRAM o varias tarjetas más pequeñas](https://oreil.ly/dJbKa) . Además de los problemas de alimentación y refrigeración que conlleva configurar un servidor doméstico con varias GPU, es posible que experimente tasas de predicción lentas al ejecutar modelos de este tamaño.

[En el capítulo 10](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch10.html#ch10) aprenderá más sobre el proceso de cuantización y el uso de LLM cuantizados .

---

Implementar LLMs sigue siendo un desafío debido a sus elevados requisitos de memoria, que se duplican si se necesita entrenarlos y ajustarlos con un conjunto de datos propio. Esto se debe a que el proceso de entrenamiento requiere el almacenamiento en caché y la reutilización de los parámetros del modelo entre lotes de entrenamiento. Por consiguiente, la mayoría de las organizaciones suelen optar por modelos ligeros (de hasta 3B) o por las API de proveedores de LLM como OpenAI, Anthropic, Cohere, Mistral, etc.

A medida que los modelos de aprendizaje automático (LLM) ganan popularidad, resulta aún más importante comprender cómo se entrenan y cómo procesan los datos, así que a continuación analizaremos los mecanismos subyacentes.

### Tokenization y embedding
Las redes neuronales no pueden procesar palabras directamente, ya que son grandes modelos estadísticos que funcionan con números. Para salvar esa brecha entre el lenguaje y los números, es necesario utilizar _la tokenización_ . Con la tokenización, se divide el texto en fragmentos más pequeños que un modelo puede procesar.

Todo texto debe dividirse primero en una lista de _tokens_ que representan palabras, sílabas, símbolos y signos de puntuación. Estos tokens se asignan luego a números únicos para poder modelar numéricamente los patrones.

Al proporcionar un vector de tokens de entrada a un transformador entrenado, la red puede predecir el siguiente mejor token para generar texto, palabra por palabra.

[La figura 3-5](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#openai_tokenizer) muestra cómo el tokenizador de OpenAI convierte el texto en una secuencia de tokens, asignando identificadores únicos a cada uno.
![[Pasted image 20260528123512.png]]

¿Qué se puede hacer después de tokenizar un texto? Estos tokens deben procesarse aún más antes de que un modelo de lenguaje pueda procesarlos.

Tras la tokenización, es necesario utilizar un _incrustador_ [5](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#id647) para convertir estos tokens en vectores densos de números reales llamados _incrustaciones_ , que capturan información semántica (es decir, el significado de cada token) en un espacio vectorial continuo. [La figura 3-6](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#embeddings) muestra estas incrustaciones.

![[Pasted image 20260528123721.png]]

---

**Consejo**
Estos vectores de incrustación utilizan _números de coma flotante_ pequeños (no enteros) para capturar relaciones sutiles entre tokens con mayor flexibilidad y precisión. Además, tienden a tener _una distribución normal_ , por lo que el entrenamiento y la inferencia del modelo de lenguaje pueden ser más estables y consistentes.

---

Tras el proceso de incrustación, a cada token se le asigna un vector de incrustación compuesto por _n_ números. Cada número del vector de incrustación se centra en una dimensión que representa un aspecto específico del significado del token.

### Training transformers
Una vez que se dispone de un conjunto de vectores de incrustación, se puede entrenar un modelo con los documentos para actualizar los valores dentro de cada incrustación. Durante el entrenamiento del modelo, el algoritmo actualiza los parámetros de las capas de incrustación para que los vectores de incrustación describan el significado de cada token con la mayor precisión posible dentro del texto de entrada.

Comprender cómo funcionan los vectores de incrustación puede resultar complicado, así que probemos con un enfoque de visualización.

Imagina que utilizas vectores de incrustación bidimensionales, es decir, vectores que contienen solo dos números. Si representas gráficamente estos vectores antes y después del entrenamiento del modelo, observarás gráficos similares a [la Figura 3-7](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#untrained_to_trained_transformer) . Los vectores de incrustación de tokens, o palabras, con significados similares estarán más próximos entre sí.
![[Pasted image 20260528124059.png]]

Para determinar la similitud entre dos palabras, se puede calcular el ángulo entre vectores mediante una fórmula conocida como _similitud del coseno_ . Ángulos más pequeños indican mayor similitud, lo que representa un contexto y significado similares. Tras el entrenamiento, el cálculo de la similitud del coseno de dos vectores de incrustación con significados similares validará que dichos vectores son muy similares entre sí.

[La figura 3-8](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#embedding_vectors) ilustra el proceso completo de tokenización, incrustación y entrenamiento.
![[Pasted image 20260528124836.png]]

Una vez que tenga una capa de incrustación entrenada, podrá usarla para incrustar cualquier texto de entrada nuevo en el modelo transformador que se muestra en la [Figura 3-1](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#transformer_architecture) .

### Positional encoding
Un paso final antes de enviar los vectores de incrustación a las capas de atención en la red transformadora es implementar _la codificación posicional_ . El proceso de codificación posicional produce los vectores de incrustación posicionales, que luego se suman con los vectores de incrustación de tokens.

Dado que los transformadores procesan las palabras simultáneamente en lugar de secuencialmente, se necesitan incrustaciones posicionales para registrar el orden y el contexto de las palabras dentro de los datos secuenciales, como las oraciones. Los vectores de incrustación resultantes capturan tanto el significado como la información posicional de las palabras en las oraciones antes de que se transmitan a los mecanismos de atención del transformador. Este proceso garantiza que los nodos de atención dispongan de toda la información necesaria para aprender patrones de forma eficaz.

[La figura 3-9](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#positional_encoding) muestra el proceso de codificación posicional donde las incrustaciones posicionales se suman con las incrustaciones de tokens.
![[Pasted image 20260528125222.png]]

### Predicción autorregresiva
El transformador es un modelo autorregresivo (es decir, secuencial) ya que las predicciones futuras se basan en los valores pasados, como se muestra en [la Figura 3-10](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#autoregressive_prediction3) .
![[Pasted image 20260528125312.png]]

El modelo recibe tokens de entrada que luego se incrustan y se pasan a través de la red para hacer la siguiente mejor predicción de token. Este proceso se repite hasta que se genera un token `<stop>`de fin de oración `<eos>`. [6](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#id658)

Sin embargo, existe un límite en la cantidad de tokens que el modelo puede almacenar en su memoria para generar el siguiente token. Este límite de tokens se conoce como la _ventana de contexto_ del modelo , un factor importante a tener en cuenta durante la fase de selección del modelo para sus servicios GenAI.

Si se alcanza el límite de la ventana de contexto, el modelo simplemente descarta los tokens menos usados. Esto significa que puede _olvidar_ las frases menos usadas en documentos o mensajes en una conversación.

---

**Nota**
En el momento de redactar este texto, el contexto del modelo OpenAI menos costoso `gpt-4o-mini`es de aproximadamente 128.000 tokens, lo que equivale a más de 300 páginas de texto.

La ventana de contexto más grande a marzo de 2025 pertenece a [Magic.Dev LTM-2-mini](https://oreil.ly/10Mj1) con 100 millones de tokens. Esto equivale a aproximadamente 10 millones de líneas de código de aproximadamente 750 novelas.

La ventana de contexto de otros modelos se sitúa en el rango de cientos de miles de tokens.

---

Los periodos de tiempo cortos conllevan la pérdida de información, dificultades para mantener las conversaciones y una menor coherencia con la consulta del usuario.

Por otro lado, las ventanas de contexto extensas requieren más memoria y pueden provocar problemas de rendimiento o ralentizar el servicio al escalar a miles de usuarios concurrentes. Además, deberá considerar los costos asociados a los modelos con ventanas de contexto más extensas, ya que suelen ser más caros debido al aumento de los requisitos de procesamiento y memoria. La elección correcta dependerá de su presupuesto y de las necesidades de los usuarios en su caso de uso.

### Integración de un modelo de lenguaje en su aplicación
Puedes descargar y utilizar un modelo de lenguaje dentro de tu aplicación con tan solo unas pocas líneas de código. En [el Ejemplo 3-1](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#language_model_usage_example) , descargarás un modelo TinyLlama que tiene 1.100 millones de parámetros y está preentrenado con 3 billones de tokens.

---

**Instalación de dependencias de TinyLlama**
Para integrar TinyLlama en tu aplicación, puedes usar la `transformers`biblioteca Hugging Face. [7](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#id665) También necesitarás instalar el marco de aprendizaje profundo PyTorch instalando el `torch`paquete. Ambos paquetes se pueden instalar a través de `pip`.

En Windows, deberá proporcionar la `--index-url`bandera al `pip`instalar `torch`que está compilado para una GPU habilitada para CUDA. [8](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#id666)

```
pip install transformers torch --index-url https://download.pytorch.org/whl/cu124
```

TinyLlama no puede generar más de unas pocas frases a la vez. También necesitarás aproximadamente 3 GB de espacio en disco y RAM para cargar este modelo en la memoria para la inferencia. Recomiendo ejecutar el modelo en una GPU NVIDIA compatible con CUDA (con el `torch`paquete compilado para CUDA), ya que la inferencia en CPU puede ser lenta. Consulta las instrucciones de instalación de CUDA de NVIDIA para [Windows](https://oreil.ly/LeA1O) o [Linux](https://oreil.ly/qjNaO) .

Además, para ejecutar [el Ejemplo 3-1](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#language_model_usage_example) en Windows, es posible que necesite instalar Visual Studio Build Tools 2022 con herramientas de desarrollo de C++ y .NET para resolver problemas con bibliotecas DLL y dependencias faltantes.

---

##### Ejemplo 3-1. Descargue y cargue un modelo de lenguaje del repositorio Hugging Face.
```python
import torch
from transformers import Pipeline, pipeline

prompt = "How to set up a FastAPI project?"
system_prompt = """
Your name is FastAPI bot and you are a helpful
chatbot responsible for teaching FastAPI to your users.
Always respond in markdown
 """

device = torch.device("cuda" if torch.cuda.is_available() else "cpu") #1

def load_text_model():
    pipe = pipeline(
        "text-generation",
        model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", #2
        torch_dtype=torch.bfloat16,
        device=device #3
    )
    return pipe

def generate_text(pipe: Pipeline, prompt: str, temperature: float=0.7) -> str:
    messages = [
        {"role":"system", "content":system_prompt},
        {"role": "user", "content":prompt},
    ] #4
    prompt = pipe.tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    ) #5
    predictions = pipe(
        prompt,
        temperature=temperature,
        max_new_tokens=256,
        do_sample=True,
        top_k=50,
        top_p=0.95,
    ) #6
    output = predictions[0]["generated_text"].split("</s>\n<|assistant|>\n")[-1]
    return output
```

1 - Comprueba si hay una GPU NVIDIA disponible y, en caso afirmativo, selecciona `device`la GPU compatible con CUDA. De lo contrario, continúa utilizando la CPU.
2 - Descarga y carga el modelo TinyLlama en la memoria con un `float16`tipo de datos de precisión tensorial.
3 - Trasladar todo el proceso a la GPU en la primera carga.
4 - Prepare la lista de mensajes, que consta de diccionarios con pares clave-valor de rol y contenido. El orden de los diccionarios determina el orden de los mensajes, del más antiguo al más reciente, en una conversación. El primer mensaje suele ser una indicación del sistema para guiar la respuesta del modelo durante la conversación.
 5 - Convierte la lista de mensajes de chat en una lista de tokens enteros para el modelo. A continuación, se le pide al modelo que genere una salida en formato de texto, no en tokens enteros `tokenize=False`. También se añade una indicación de generación al final de los mensajes de chat ( `add_generation_prompt=True`) para incentivar al modelo a generar una respuesta basada en el historial de chat.
6 - La consigna preparada se pasa al modelo con varios parámetros de inferencia para optimizar el rendimiento de la generación de texto. Algunos de estos parámetros de inferencia clave incluyen:
- `max_new_tokens`: Especifica el número máximo de nuevos tokens que se generarán en la salida.
- `do_sample`: Determina, al producir una salida, si se debe elegir un token al azar de una lista de tokens adecuados ( `True`) o simplemente elegir el token más probable en cada paso ( `False`).
- `temperature`Controla la aleatoriedad en la generación de resultados. Los valores más bajos hacen que los resultados del modelo sean más precisos, mientras que los valores más altos permiten respuestas más creativas.
- `top_k`: Restringe las predicciones de tokens del modelo a las K opciones principales. `top_k=50`Significa crear una lista de los 50 tokens más adecuados para elegir en el paso de predicción de tokens actual.
- `top_p`: Implementa _el muestreo de núcleo_ al crear una lista de los tokens más adecuados. `top_p=0.95`Esto significa crear una lista de los mejores tokens hasta que estés satisfecho de que tu lista tenga el 95 % de los tokens más adecuados para elegir, para el paso de predicción de tokens actual.
7 - El resultado final se obtiene del `predictions`objeto. El texto generado por TinyLlama incluye el historial completo de la conversación, con la respuesta generada añadida al final. El `</s>`token de parada, seguido de `\n<|assistant|>\n`otros tokens, se utiliza para extraer el contenido del último mensaje de la conversación, que es la respuesta del modelo.

[El ejemplo 3-1](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#language_model_usage_example) es un buen punto de partida; aún puedes cargar este modelo en tu CPU y obtener respuestas en un tiempo razonable. Sin embargo, TinyLlama podría no tener el mismo rendimiento que sus contrapartes más grandes. Para cargas de trabajo de producción, es recomendable usar modelos más grandes para obtener una mejor calidad de salida y un mejor rendimiento.

Ahora puede usar las funciones `load_model`y dentro de una función de controlador [10](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#id668) y luego agregar un decorador de manejo de ruta para servir el modelo a través de un punto final, como se muestra en [el Ejemplo 3-2](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#text_endpoint) .`predict`[](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#id668)[](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#text_endpoint)

##### Ejemplo 3-2. Servir un modelo de lenguaje a través de un punto final de FastAPI.
```python
from fastapi import FastAPI
from models import load_text_model, generate_text

app = FastAPI()

@app.get("/generate/text") #1
def server_llm_controller(prompt: str) -> str: #2
    pipe = load_text_model() #3
    output = generate_text(pipe, prompt) #4
    return output #5
```

1 - Crea un servidor FastAPI y añade un `/generate`controlador de ruta para servir el modelo.
2 - Es `serve_language_model_controller`responsable de tomar la solicitud de los parámetros de la consulta de la solicitud.
3 - El modelo se carga en la memoria.
4 - El controlador pasa la consulta al modelo para que realice la predicción.
5 - El servidor FastAPI envía el resultado como una respuesta HTTP al cliente

Una vez que el servicio FastAPI esté en funcionamiento, puede visitar la página de documentación de Swagger ubicada en `http://localhost:8000/docs` para probar su nuevo punto final:

```
http://localhost:8000/generate/text?prompt="¿Qué es FastAPI?"
```

Si ejecuta los ejemplos de código en una CPU, tardará aproximadamente un minuto en recibir una respuesta del modelo, como se muestra en [la Figura 3-11](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#text_gen_response) .
![[Pasted image 20260528133240.png]]

![[Pasted image 20260528133258.png]]

No es una mala respuesta para un modelo de lenguaje pequeño (SLM) que se ejecuta en la CPU de tu propio ordenador, salvo que TinyLlama ha _creído erróneamente_ que FastAPI usa Flask. Eso es incorrecto; FastAPI usa Starlette como framework web subyacente, no Flask.

_Las alucinaciones_ se refieren a resultados que no se basan en los datos de entrenamiento ni en la realidad. Si bien los modelos de lenguaje natural (SLM) de código abierto, como TinyLlama, se han entrenado con una cantidad impresionante de tokens (3 billones), un número reducido de parámetros del modelo puede haber limitado su capacidad para aprender la verdad fundamental de los datos. Además, es posible que también se hayan utilizado algunos datos de entrenamiento sin filtrar, lo que puede contribuir a que se produzcan más casos de alucinaciones.

Ahora puedes usar un cliente de navegador web en Python para probar visualmente tu servicio con mayor interactividad en comparación con el uso de un cliente de línea de comandos.

[Streamlit](https://oreil.ly/9BXmn) es un excelente paquete de Python para desarrollar rápidamente una interfaz de usuario , que permite crear interfaces de usuario atractivas y personalizables para tus servicios de IA con poco esfuerzo.

### Conectando FastAPI con el generador de interfaz de usuario de Streamlit
Streamlit te permite crear fácilmente una interfaz de usuario de chat para realizar pruebas y prototipos con modelos. Puedes instalar el `streamlit`paquete usando `pip`:

```
pip install streamlit
```

[El ejemplo 3-3](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#streamlit_chat_ui) muestra cómo desarrollar una interfaz de usuario sencilla para conectarse con su servicio.

##### Ejemplo 3-3. Interfaz de chat de Streamlit que consume el `generate`punto final de FastAPI.
```python
import requests
import streamlit as st

st.title("FastAPI Chatbot") # 1

if "messages" not in st.session_state:
    st.session_state.messages = [] # 2

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"]) # 3

if prompt := st.chat_input("Write your prompt in this input field"): # 4
    st.session_state.messages.append({"role":"user", "content": prompt}) # 5

    with st.chat_message("user"):
        st.text(prompt) # 6

    response = requests.get(
        f"http://127.0.0.1:8000/generate/text", params = {"prompt":prompt} # 7
    )

    response.raise_for_status() # 8

    with st.chat_message("assistant"):
        st.markdown(response.text) # 9
```

1 - Agregue un título a su aplicación que se mostrará en la interfaz de usuario
2 - Inicializa el chat y mantén un registro del historial de conversaciones.
3 - Mostrar los mensajes del historial de chat al reiniciar la aplicación.
4 - Espere hasta que el usuario haya enviado una solicitud a través del campo de entrada del chat.
5 - Agrega los mensajes del usuario o del asistente al historial de chat.
6 - Muestra el mensaje del usuario en el contenedor de mensajes del chat.
7 - Envía una `GET`solicitud con el parámetro de consulta especificado a tu punto final de FastAPI para generar una respuesta de TinyLlama.
8 - Validar que la respuesta sea correcta.
9 - Muestra el mensaje del asistente en el contenedor de mensajes del chat.

Ahora puede iniciar su aplicación cliente de Streamlit:
```
streamlit run client.py
```

Ahora debería poder interactuar con TinyLlama dentro de Streamlit, como se muestra en [la Figura 3-12](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#streamlit_ui_text_results) . Todo esto fue posible con unos pocos scripts de Python.
![[Pasted image 20260528141554.png]]

[La figura 3-13](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#tiny_llama_fastapi_architecture) muestra la arquitectura general del sistema de la solución que hemos desarrollado hasta el momento.

![[Pasted image 20260528141850.png]]

---

**Advertencia**
Si bien la solución del [Ejemplo 3-3](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#streamlit_chat_ui) es excelente para la creación de prototipos y la prueba de modelos, no es adecuada para cargas de trabajo de producción donde varios usuarios necesitan acceso simultáneo al modelo. Esto se debe a que, con la configuración actual, el modelo se carga y descarga en la memoria cada vez que se procesa una solicitud. Cargar y descargar un modelo grande en la memoria repetidamente es lento y bloquea las operaciones de entrada/salida.

---

El servicio TinyLlama que acabas de crear utilizaba un transformador _decodificador_ , optimizado para casos de uso conversacionales y de chat. Sin embargo, el [artículo original sobre transformadores](https://oreil.ly/RqztC) presentaba una arquitectura que constaba tanto de un codificador como de un decodificador.

---

**Variantes de Transformers**
Hay tres tipos de transformadores que debes conocer cuando trabajas con modelos de lenguaje, como se muestra en [la Figura 3-14](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#transformer_architectures) .
![[Pasted image 20260528142205.png]]

Cada variante de transformador tiene sus propias capacidades únicas y se especializa en ciertas tareas.

**Encoder-decoder transformers**
- Se utiliza para transformar una secuencia de información en otra.
- Excelente en traducción, resumen de textos y tareas de preguntas y respuestas.

**Encoder-only transformers**
- Se utiliza para comprender y representar los significados de las secuencias de entrada.
- Especializado en análisis de sentimientos, extracción de entidades y tareas de clasificación de texto.

**Decoder-only transformers**
- Se utiliza para predecir el siguiente token en una secuencia.
- Supera a otros transformadores en tareas de generación de texto, conversación y modelado del lenguaje.

En la práctica, debes seleccionar el transformador adecuado para tu caso de uso en función de su especialización y capacidades.

---

Ahora debería sentirse más seguro de comprender el funcionamiento interno de los modelos de lenguaje y cómo integrarlos en un servidor web FastAPI.

Los modelos de lenguaje representan solo una fracción de todos los modelos generativos. Las próximas secciones ampliarán sus conocimientos para incluir la función y el uso de modelos que generan audio, imágenes y videos.

Podemos empezar trabajando primero con modelos de audio.

## Modelos de audio
En los servicios de GenAI, los modelos de audio son fundamentales para crear sonidos interactivos y realistas. A diferencia de los modelos de texto, que se centran en el procesamiento y la generación de texto, los modelos de audio pueden gestionar señales de audio. Con ellos, se puede sintetizar voz, generar música e incluso crear efectos de sonido para aplicaciones como asistentes virtuales , doblaje automático, desarrollo de videojuegos y entornos de audio inmersivos .

Uno de los modelos de conversión de texto a voz y texto a audio más capaces es el modelo Bark, creado por Suno AI. Este modelo basado en transformadores puede generar voz y audio multilingües realistas, incluyendo música, ruido de fondo y efectos de sonido.

El modelo Bark consta de cuatro modelos encadenados como una tubería para sintetizar formas de onda de audio a partir de indicaciones textuales, como se muestra en [la Figura 3-15](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#bark_pipeline) .
![[Pasted image 20260528150848.png]]

1. Modelo de texto semántico
Un modelo transformador autorregresivo causal (secuencial) acepta texto de entrada tokenizado y captura su significado mediante tokens semánticos. Los modelos autorregresivos predicen valores futuros en una secuencia reutilizando sus propios resultados anteriores.

2. Modelo acústico grueso
Un transformador autorregresivo causal recibe las salidas del modelo semántico y genera las características de audio iniciales, que carecen de detalles más precisos. Cada predicción se basa en información pasada y presente de la secuencia de tokens semánticos.

3. Modelo de acústica fina
Un transformador autoencoder no causal refina la representación de audio generando las características de audio restantes. Dado que el modelo acústico grueso ha generado toda la secuencia de audio, el modelo fino no necesita ser causal.

4. Modelo de códec de audio Encodec
El modelo decodifica la matriz de audio de salida a partir de todos los códigos de audio generados previamente.


Bark sintetiza la forma de onda de audio decodificando las características de audio refinadas en la salida de audio final en forma de palabras habladas, música o efectos de audio simples.

[El ejemplo 3-4](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#small_bark) muestra cómo utilizar el modelo pequeño de Bark.

##### Ejemplo 3-4. Descargue y cargue el modelo pequeño de Bark desde el repositorio de Hugging Face.
```python
# schemas.py
from typing import Literal

VoicePresets = Literal["v2/en_speaker_1", "v2/en_speaker_9"] # 1
```


```python
# models.py
import torch
import numpy as np
from transformers import AutoProcessor, AutoModel, BarkProcessor, BarkModel
from schemas import VoicePresets

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# https://huggingface.co/suno/bark-small?library=transformers
def load_audio_model() -> tuple[BarkProcessor, BarkModel]:
    processor = AutoProcessor.from_pretrained("suno/bark-small") #2
    model = AutoModel.from_pretrained("suno/bark-small") #3
    model = model.to(device)
    return processor, model

def generate_audio(
    processor: BarkProcessor,
    model: BarkModel,
    prompt: str,
    preset: VoicePresets,
) -> tuple[np.array, int]:
    inputs = processor(text=[prompt], return_tensors="pt", voice_preset=preset) #4
    output = model.generate(**inputs, do_sample=True).cpu().numpy().squeeze() #5
    sample_rate = model.generation_config.sample_rate #6
    return output, sample_rate
```

1 - Especifique las opciones de preajuste de voz compatibles mediante un `Literal`tipo.
2 -   Descarga el pequeño procesador Bark, que prepara el texto de entrada para el modelo principal.
3 - Descarga el modelo Bark, que se utilizará para generar el audio de salida. Ambos objetos serán necesarios para la generación de audio posterior.
4 - Preprocesa el mensaje de texto con una incrustación de preajuste de voz del hablante y devuelve una matriz tensorial de PyTorch de entradas tokenizadas usando `return_tensors="pt"`.
5 - Genera una matriz de audio que contenga los valores de amplitud de la señal de audio sintetizada a lo largo del tiempo.
6 - Obtenga la frecuencia de muestreo a partir de las configuraciones de generación del modelo, que se pueden utilizar para producir el audio.

Cuando se genera audio utilizando un modelo, la salida es una secuencia de números de coma flotante que representan la _amplitud_ (o intensidad) de la señal de audio en cada instante.

Para reproducir este audio, es necesario convertirlo a un formato digital compatible con los altavoces. Esto implica muestrear la señal de audio a una frecuencia fija y cuantificar los valores de amplitud a un número fijo de bits. La `soundfile`biblioteca puede ayudarte generando el archivo de audio con una _frecuencia de muestreo determinada_ . Cuanto mayor sea la frecuencia de muestreo, mayor será el número de muestras, lo que mejora la calidad del audio, pero también aumenta el tamaño del archivo.

Puedes instalar la `soundfile`biblioteca de audio para escribir archivos de audio usando `pip`:
```python
pip install soundfile
```

[El ejemplo 3-5](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#audio_endpoint) muestra cómo se puede transmitir el contenido de audio al cliente.

##### Ejemplo 3-5. Punto final de FastAPI para devolver audio generado
```python
# utils.py
from io import BytesIO
import soundfile
import numpy as np

def audio_array_to_buffer(audio_array: np.array, sample_rate: int ) -> BytesIO:
    buffer = BytesIO()
    soundfile.write(buffer, audio_array, sample_rate, format="wav") #1
    buffer.seek(0)
    return buffer #2
```

```python
# main.py
from fastapi import FastAPI, status
from fastapi.responses import StreamingResponse

from models import load_audio_model, generate_audio
from schemas import VoicePresets
from utils import audio_array_to_buffer

app = FastAPI()

@app.get("/generate/audio", 
    responses={status.HTTP_200_OK:{"content": {"audio/wav":{}}}}, 
    response_class=StreamingResponse,
) #3
def serve_text_to_audio_model_controller(prompt:str, preset: VoicePresets="v2/en_speaker_1",):
    processor, model = load_audio_model()
    output, sample_rate = generate_audio(processor, model, prompt, preset)
    return StreamingResponse(
        audio_array_to_buffer(output, sample_rate), media_type="audio/wav"
    ) #4
```

1 - Instala la `soundfile`biblioteca para escribir la matriz de audio en el búfer de memoria utilizando su frecuencia de muestreo.
2 - Restablece el cursor del búfer al inicio del mismo y devuelve el búfer iterable.
3 - Crea un nuevo punto final de audio que devuelva el `audio/wav`tipo de contenido como `StreamingResponse`. `StreamingResponse`Normalmente se utiliza cuando se desea transmitir los datos de respuesta, como al devolver archivos grandes o al generar los datos de respuesta. Permite devolver una función generadora que produce fragmentos de datos para enviar al cliente.
4 - Convierta la matriz de audio generada en un búfer iterable que pueda pasarse a la respuesta de transmisión.

En [el Ejemplo 3-5](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#audio_endpoint) , generaste una matriz de audio usando el modelo Bark pequeño y transmitiste el búfer de memoria del contenido de audio. La transmisión es más eficiente para archivos grandes, ya que el cliente puede consumir el contenido a medida que se sirve. En ejemplos anteriores, no usamos respuestas de transmisión, ya que las imágenes o el texto generados pueden ser bastante pequeños en comparación con el contenido de audio o video.

---

**Consejo**
La transmisión de contenido de audio directamente desde un búfer de memoria es más rápida y eficiente que escribir la matriz de audio en un archivo y transmitir el contenido desde el disco duro.

Si necesitas la memoria disponible para otras tareas, puedes escribir primero el array de audio en un archivo y luego reproducirlo mediante un generador de lectores de archivos. En ese caso, estarás sacrificando memoria a cambio de una menor latencia.

---

Ahora que dispone de un punto final de generación de audio, puede actualizar el código de su cliente de interfaz de usuario de Streamlit para renderizar mensajes de audio. Actualice el código de su cliente de Streamlit como se muestra en [el Ejemplo 3-6](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#barksmall_streamlit_ui).

##### Ejemplo 3-6. Interfaz de usuario de audio de Streamlit que consume el `/audio`punto final de generación de FastAPI.
```python
import requests
import streamlit as st

st.title("Generate Audio")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        content = message["content"]
        if isinstance(content, bytes):
            st.audio(content)
        else:
            st.markdown(content)

if prompt := st.chat_input("Write your prompt in this input field"):
    response = requests.get(
        f"http://127.0.0.1:8000/generate/audio", params={"prompt":prompt}
    )
    response.raise_for_status()

    with st.chat_message("assistant"):
        st.text("Here is your generated audio")
        st.audio(response.content) #1
```

1 - Actualiza el código del cliente de Streamlit para que reproduzca contenido de audio.

Con Streamlit, puedes intercambiar componentes para renderizar cualquier tipo de contenido, incluyendo imágenes, audio y vídeo.

Ahora debería poder generar audio de voz muy realista en su interfaz de usuario de Streamlit actualizada, como se muestra en [la Figura 3-16](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#streamlit_bark_ui) .

![[Pasted image 20260528172719.png]]

Ten en cuenta que estás usando la versión comprimida del modelo Bark, pero con la versión ligera puedes generar audio de voz y música con bastante rapidez, incluso con una sola CPU. Esto se consigue a cambio de una menor calidad de generación de audio.

Ahora debería sentirse más cómodo ofreciendo contenido más extenso a sus usuarios mediante respuestas en tiempo real y trabajando con modelos de audio.

Hasta ahora, has estado creando servicios conversacionales y de conversión de texto a voz. Ahora veamos cómo interactuar con un modelo de visión para crear un servicio generador de imágenes.

## Modelos de visión
Mediante el uso de modelos de visión, puedes generar, mejorar y comprender información visual a partir de indicaciones.

Dado que estos modelos pueden producir resultados muy realistas más rápido que cualquier ser humano y pueden comprender y manipular el contenido visual existente, son extremadamente útiles para aplicaciones como generadores y editores de imágenes, detección de objetos, clasificación y subtitulado de imágenes y realidad aumentada.

Una de las arquitecturas más populares utilizadas para entrenar modelos de imágenes se llama _Difusión Estable_ (SD).

Los modelos SD se entrenan para codificar imágenes de entrada en un espacio latente. Este espacio latente es la representación matemática de los patrones de los datos de entrenamiento que el modelo ha aprendido. Si intentas visualizar una imagen codificada, solo verás ruido blanco, similar a los puntos blancos y negros que aparecen en la pantalla de tu televisor cuando pierde la señal.

[La figura 3-17](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#stable_diffusion) muestra el proceso completo de entrenamiento e inferencia, y visualiza cómo se codifican y decodifican las imágenes mediante los procesos de difusión directa e inversa. Un codificador de texto que utiliza texto, imágenes y mapas semánticos ayuda a controlar la salida mediante la difusión inversa.
![[Pasted image 20260528172956.png]]

Lo que hace mágicos a estos modelos es su capacidad para decodificar imágenes ruidosas y convertirlas de nuevo en imágenes originales. En efecto, los modelos SD también aprenden a eliminar el ruido blanco de una imagen codificada para reproducir la imagen original. El modelo realiza este proceso de eliminación de ruido a lo largo de varias iteraciones.

Sin embargo, no querrás recrear imágenes que ya tienes. Querrás que el modelo cree imágenes nuevas e inéditas. Pero, ¿cómo puede un modelo SD lograr esto? La respuesta reside en el espacio latente donde se almacenan las imágenes ruidosas codificadas. Puedes modificar el ruido en estas imágenes para que, cuando el modelo las procese y las decodifique, obtengas una imagen completamente nueva que el modelo nunca haya visto antes.

Persiste un desafío: ¿cómo controlar el proceso de generación de imágenes para que el modelo no produzca imágenes aleatorias? La solución consiste en codificar también las descripciones de las imágenes junto con ellas. Los patrones del espacio latente se asignan a descripciones textuales de lo que se observa en cada imagen de entrada. A continuación, se utilizan indicaciones textuales para muestrear el espacio latente ruidoso, de modo que la imagen de salida resultante tras el proceso de reducción de ruido sea la deseada.

Así es como los modelos SD pueden generar imágenes nuevas que nunca antes habían visto en sus datos de entrenamiento. En esencia, estos modelos navegan por un espacio latente que contiene representaciones codificadas de diversos patrones y significados.<sup> [12</sup>](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#id686) El modelo refina iterativamente este ruido mediante un proceso de eliminación de ruido para producir una imagen novedosa que no está presente en su conjunto de datos de entrenamiento.

Para descargar un modelo SD, necesitarás tener `diffusers`instalada la biblioteca Hugging Face:
```
pip install diffusers
```
[El ejemplo 3-7](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#sd_model_usage_example) muestra cómo cargar un modelo SD en la memoria.
##### Ejemplo 3-7. Descargue y cargue un modelo SD del repositorio Hugging Face.
```python
# models.py

import torch 
from diffusers import DiffusionPipeline, StableDiffusionInpaintPipelineLegacy
from PIL import image

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_image_model() -> StableDiffusionInpaintPipelineLegacy:
    pipe = DifussionPipeline.from_pretrained(
        "segmind/tiny-sd", 
        torch_dtype=torch.float32,
        device=device
    ) # 1
    return pipe

def generate_image(pipe: StableDiffusionInpaintPipelineLegacy, prompt:str) -> Image.Image:
    output = pipe(prompt, num_inference_steps=10).images[0] # 2,3
    return output # 4
```

1 - Descarga y carga el modelo TinySD en memoria con el `float32`tipo de tensor menos eficiente en cuanto a memoria. Usar `float16`, que tiene precisión limitada para modelos grandes y complejos, conduce a inestabilidad numérica y pérdida de precisión. Además, la compatibilidad de hardware para `float16`es limitada, por lo que intentar ejecutar un modelo SD en tu CPU con el `float16`tipo de tensor puede no ser posible. Fuente: [Hugging Face](https://oreil.ly/rzw8P).

2 -  `prompt`: Ingresa el texto de la solicitud al modelo para generar una lista de imágenes y seleccionar la primera. Algunos modelos permiten generar varias imágenes en un solo paso de inferencia.

3 - Este `num_inference_steps=10`parámetro especifica el número de pasos de difusión que se realizarán durante la inferencia. En cada paso de difusión, se genera una imagen con mayor ruido a partir de los pasos de difusión anteriores. El modelo genera múltiples imágenes con ruido mediante la realización de varios pasos de difusión. Con estas imágenes, el modelo puede comprender mejor los patrones de ruido presentes en los datos de entrada y aprender a eliminarlos de forma más eficaz. Cuantos más pasos de inferencia se realicen, mejores serán los resultados, pero esto conlleva un mayor consumo de recursos computacionales y tiempos de procesamiento más prolongados.

4 - La imagen generada será de tipo imagen Pillow de Python, por lo que tendrá acceso a diversos métodos de Pillow para su procesamiento y almacenamiento. Por ejemplo, puede llamar al `image.save()`método para guardar la imagen en su sistema de archivos.

---

**Nota**
Los modelos de visión consumen muchísimos recursos. Para cargar y usar un modelo pequeño como TinySD en la CPU, necesitarás aproximadamente 5 GB de espacio en disco y RAM. Sin embargo, puedes instalarlo `accelerate`para `pip install accelerate`optimizar los recursos necesarios y que el modelo utilice menos memoria de la CPU.

Al servir modelos de vídeo, necesitarás usar una GPU. Más adelante en este capítulo, te mostraré cómo aprovechar las GPU para los modelos de vídeo.

---

Ahora puede empaquetar este modelo en otro punto final de forma similar al [Ejemplo 3-2](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#text_endpoint) , con la diferencia de que la respuesta devuelta será un binario de imagen (no texto). Consulte el [Ejemplo 3-8](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#image_endpoint) .
##### Ejemplo 3-8. Punto final de FastAPI para devolver una imagen generada.
```python
# utils.py
from typing import Literal
from PIL import Image
from io import BytesIO

def img_to_bytes(image: Image.Image, img_format: Literal["PNG", "JPEG"] = "PNG") -> bytes:
    buffer = BytesIO()
    image.save(buffer, format=img_format)
    return buffer.getvalue() # 1
```

```python
# main.py
from fastapi import FastAPI, Response, status
from models import load_image_model, generate_image
from utils import img_to_bytes

app = FastAPI()

@app.get("/generate/images", 
        responses={status.HTTP_200_OK: {"content":{"image/png": {}}}}, # 2
        response_class=Response # 3
        )
def serve_text_to_image_model_controller(prompt: str):
    pipe = load_image_model()
    output = generate_image(pipe, prompt) # 4
    return Response(content=img_to_bytes(output), media_type="image/png") # 5
```

1 - Crea un búfer en memoria, guarda la imagen en este búfer en un formato determinado y, a continuación, devuelve los datos en bytes sin procesar del búfer.
2 -   Especifique el tipo de contenido multimedia y los códigos de estado para la página de documentación de la interfaz de usuario de Swagger generada automáticamente.
3 - Especifique la clase de respuesta para evitar que FastAPI la agregue `application/json` como un tipo de medio de respuesta aceptable adicional.
4 -  La respuesta que devuelva el modelo estará en formato de imagen Pillow.
5 - Necesitaremos utilizar la `Response`clase FastAPI para enviar una respuesta especial que contenga bytes de imagen con un tipo de medio PNG.

[La figura 3-18](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#tinysd_swagger_docs) muestra los resultados de probar el nuevo `/generate/image`endpoint a través de la documentación de FastAPI Swagger con el mensaje de texto `A cosy living room with trees in it`.

![[Pasted image 20260528181640.png]]

Ahora, conecta tu punto final a una interfaz de usuario de Streamlit para la creación de prototipos, como se muestra en [el Ejemplo 3-9](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#tinysd_streamlit_code) .

##### Ejemplo 3-9. Interfaz de usuario de Streamlit Vision que consume el `_/image_`punto final de generación de FastAPI.

```python
import requests
import streamlit as st

st.title("FastAPI Text to Image")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.image(message["content"]) # 1

if prompt := st.chat_input("Write your prompt in this input field"):
    st.session_state.messages.append({"role":"user", "content": prompt})

    with st.chat_message("user"):
        st.text(prompt)

    response = requests.get(
        f"http://127.0.0.1:8000/generate/image", params = {"prompt":prompt}
    ) # 2

    response.raise_for_status()
    
    with st.chat_message("assistant"):
        st.text("Here is your generated image")
        st.image(response.content)
```

1 - Las imágenes transferidas mediante el protocolo HTTP estarán en formato binario. Por lo tanto, actualizamos la función de visualización para que muestre el contenido binario de la imagen. Puedes usar este `st.image`método para mostrar las imágenes en la interfaz de usuario.
2 - Actualiza la `GET`solicitud para que llegue al `/generate/image`punto final. Luego, muestra un mensaje de texto e imagen al usuario.

[La figura 3-19](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#tinysd_streamlitui) muestra los resultados finales de la experiencia del usuario con el modelo.
![[Pasted image 20260528182429.png]]

---

**Modelos XL en funcionamiento**
Ahora verá cómo implementar puntos finales de servicio de modelos con FastAPI y Streamlit para generar texto o imágenes. Hemos utilizado versiones reducidas de estos modelos para que pueda ejecutar los ejemplos en su CPU. Sin embargo, los requisitos de hardware aumentan considerablemente si necesita utilizar las versiones XL para obtener una mejor calidad. Por ejemplo, para ejecutar el modelo SDXL, necesitará 16 GB de RAM de CPU y 16 GB de VRAM de GPU para generar una imagen. Esto se debe a que primero deberá cargar el modelo en su CPU desde el disco y luego transferirlo a su GPU para la inferencia. Explicaremos este proceso con más detalle al hablar de las estrategias de servicio de modelos.

---

Vimos cómo, incluso con un modelo SD pequeño, se pueden generar imágenes de aspecto razonable. Las versiones XL pueden producir imágenes aún más realistas, pero aún tienen sus limitaciones.

En el momento de redactar este texto, los modelos SD de código abierto actuales presentan ciertas limitaciones:

**Coherencia**
Los modelos no pueden reproducir todos los detalles descritos en las instrucciones ni las composiciones complejas.

**Tamaño de salida**
Las imágenes de salida solo pueden tener tamaños predefinidos, como 512 × 512 o 1024 × 1024 píxeles.

**Componibilidad**
No se puede controlar completamente la imagen generada ni definir la composición de la misma.

**Fotorrealismo**
Los resultados generados muestran detalles que delatan que han sido generados por IA.

**Texto legible**
Algunos modelos no pueden generar textos legibles.

El `tinysd`modelo con el que trabajaste es un modelo de fase inicial que ha sido sometido al proceso _de destilación_ (es decir, compresión) a partir del modelo SD V1.5 más grande. Como resultado, los resultados generados podrían no cumplir con los estándares de producción ni ser completamente coherentes, y podrían no incorporar todos los conceptos mencionados en las indicaciones del texto. Sin embargo, los modelos resultantes podrían funcionar bien si se [_ajustan_ mediante _la Adaptación de Bajo Rango_ (LoRA)](https://oreil.ly/Nqtkm) en conceptos o estilos específicos.

---

**Adaptación de bajo rango en el ajuste fino de modelos generativos**
LoRA es una estrategia de entrenamiento que introduce un número mínimo de parámetros entrenables en cada capa de un modelo. La mayoría de los parámetros del modelo original permanecen fijos.

Al limitar la cantidad de parámetros que deben entrenarse, LoRA reduce considerablemente la memoria de GPU necesaria para el entrenamiento. Esto resulta muy útil al ajustar o entrenar modelos a gran escala, donde las limitaciones de memoria suelen ser un gran obstáculo para la personalización.

---

Ahora puedes crear servicios de IA genómica basados ​​tanto en texto como en imágenes. Sin embargo, quizás te preguntes cómo crear servicios de conversión de texto a vídeo utilizando modelos de vídeo. A continuación, veremos más sobre los modelos de vídeo, su funcionamiento y cómo crear un servicio de animación de imágenes con ellos.

## Modelos de vídeo
Los modelos de vídeo son algunos de los modelos generativos que más recursos consumen y, a menudo, requieren una GPU para producir un fragmento corto de buena calidad. Estos modelos tienen que generar varias decenas de fotogramas para producir un solo segundo de vídeo, incluso sin contenido de audio.

Stability AI ha lanzado varios modelos de vídeo de código abierto basados ​​en la arquitectura SD para Hugging Face. Trabajaremos con la versión comprimida de su modelo de conversión de imagen a vídeo para ofrecer un servicio de animación de imágenes más rápido.

Para empezar, vamos a poner en marcha un pequeño modelo de conversión de imagen a vídeo utilizando [el Ejemplo 3-10](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#video_model_loading) .

---

**Nota**
Para ejecutar [el Ejemplo 3-10](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#video_model_loading) , es posible que necesite acceso a una GPU NVIDIA compatible con CUDA.

Asimismo, para el uso comercial del `stable-video-diffusion-img2vid`modelo, consulte su [ficha técnica](https://oreil.ly/DM-0p) .

---

##### Ejemplo 3-10. Descargue y cargue el modelo _img2vid_ de Stability AI desde el repositorio Hugging Face.
```python
import torch 
from diffusers import StableVideoDiffusionPipeline
from PIL import Image

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_vide_model() -> StableVideoDiffusionPipeline:
    pipe = StableVideoDiffusionPipeline.from_pretrained(
        "stabilityai/stable-video-diffusion-img2vid",
        torch_dtype=torch.float16,
        variant="fp16",
        device=device
    )
    return pipe 

def generate_video(pipe: StableVideoDiffusionPipeline, image: Image.Image, num_frames:int=25) -> list[Image.Image]:
    image = image.resize((1024, 576)) #1
    generator = torch.manual_seed(42) #2
    frames = pipe(
        image, decode_chunk_size = 8,
        generator=generator,
        num_frames=num_frames
    ).framesp[0]
    return frames
```

1 - Redimensiona la imagen de entrada a un tamaño estándar compatible con el modelo. Este redimensionamiento también evitará problemas con imágenes de gran tamaño.
2 - Crea un generador de tensores aleatorios con la semilla establecida en 42 para generar fotogramas de vídeo reproducibles.
3 - Ejecuta la canalización de generación de fotogramas para producir todos los fotogramas de vídeo a la vez. Toma el primer lote de fotogramas generados. Este paso requiere una cantidad considerable de memoria de vídeo. `num_frames`especifica el número de fotogramas a generar, mientras que `decode_chunk_size`especifica cuántos fotogramas generar a la vez.

Una vez implementadas las funciones de carga del modelo, ya puede crear el punto final de servicio de vídeo.

Sin embargo, antes de proceder a declarar el controlador de ruta, necesita una función de utilidad para procesar las salidas del modelo de vídeo de los fotogramas y convertirlas en un vídeo transmitible mediante un búfer de E/S.

Para exportar una secuencia de fotogramas a vídeos, es necesario codificarlos en un contenedor de vídeo utilizando una biblioteca de vídeo como `av`, que implementa enlaces de Python a la popular `ffmpeg`biblioteca de procesamiento de vídeo.

Puedes instalar la `av`biblioteca mediante:
```
pip install av
```
Ahora puede utilizar [el Ejemplo 3-11](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#frames_to_videos) para crear búferes de vídeo que se puedan transmitir en tiempo real.

##### Ejemplo 3-11. Exportación de la salida del modelo de vídeo desde fotogramas a un búfer de vídeo transmitible mediante la `av`biblioteca
```python
from io import BytesIO
from PIL import Image
import av

def export_to_video_buffer(images: list[Image.Image]) -> BytesIO:
    buffer = BytesIO()
    output = av.open(buffer, "w", format="mp4") #1
    stream = output.add_stream("h264", 30) #2
    stream.width = images[0].width
    stream.height = images[0].height
    stream.pix_fmt = "yuv444p" #3
    stream.options = {"crf":"17"} #4

    for image in images:
        frame = av.VideoFrame.from_image(image)
        packet = stream.encode(frame) #5
        output = mux(packet) #6
    packet = stream.encode(None) 
    output.mux(packet)
    return buffer #7
```

1 - Abra un búfer para escribir un archivo MP4 y luego configure una transmisión de video con el multiplexor de video de AV. [13](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#id697)
2 - Configure la codificación de vídeo a `h264`30 fotogramas por segundo y asegúrese de que las dimensiones de los fotogramas coincidan con las proporcionadas a la función.
3 - Configure el formato de píxeles del flujo de vídeo de `yuv444p`forma que cada píxel tenga la resolución completa para la `y`(luminancia o brillo) y ambos componentes `u`y (crominancia o color).`v`
4 - Configure el factor de tasa constante (CRF) del flujo para controlar la calidad y la compresión del video. Establezca el CRF en 17 para obtener un video de alta calidad sin pérdidas y con una compresión mínima.
5 - Codifique los fotogramas de entrada en paquetes codificados con el multiplexor de vídeo de flujo configurado.
6 - Agregue los fotogramas codificados al búfer del contenedor de video abierto.
7 - Vacía el codificador para eliminar los fotogramas restantes y combina el paquete resultante en el archivo de salida antes de devolver el búfer que contiene el vídeo codificado.

Para utilizar las solicitudes de imágenes con el servicio como cargas de archivos, debe instalar la `python-multipart`biblioteca: [1](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#id698)
```
pip install python-multipart
```

Una vez instalado, puede configurar el nuevo punto final utilizando [el Ejemplo 3-12](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#video_endpoint) .

##### Ejemplo 3-12. Reproducción de vídeos generados a partir del modelo de conversión de imagen a vídeo.
```python
from fastapi import status, FastAPI, File
from fastapi.responses import StreamingResponse
from io import BytesIO
from PIL import Image

from models import load_vide_model, generate_video
from utils import export_to_video_buffer

app = FastAPI()

@app.post("/generate/video", 
          responses={status.HTTP_200_OK:{"content": {"video/mp4":{}}}},
          response_class=StreamingResponse,
)
def serve_image_to_video_model_controller(image: bytes = File(...), num_frames: int=25): #1
    image = Image.open(BytesIO(image)) #2
    model = load_vide_model()
    frames = generate_video(model, image, num_frames)
    return StreamingResponse(
        export_to_video_buffer(frames), media_type="video/mp4" #3
    )

```


1 - Utilice el `File`objeto para especificarlo `image`como una carga de archivo de formulario.
2 - Crea un `Image`objeto Pillow pasando los bytes de la imagen transferidos al servicio. El pipeline del modelo espera un formato de imagen Pillow como entrada.
3 - Exporta los fotogramas generados como un vídeo MP4 y transmítelo al cliente mediante un búfer de vídeo iterable.

Una vez configurado el punto final de vídeo, ya puede subir imágenes a su servicio FastAPI para animarlas como vídeos.

En la plataforma hay otros modelos de vídeo disponibles que permiten generar GIF y animaciones. Para practicar más, puedes intentar crear un servicio GenAI con ellos. Si bien los modelos de vídeo de código abierto pueden producir vídeos con una calidad más que suficiente, el anuncio de OpenAI de un nuevo modelo de visión a gran escala (LVM, por sus siglas en inglés) llamado Sora ha sacudido la industria de la generación de vídeo.


### OpenAI Sora
Los modelos de conversión de texto a vídeo tienen capacidades de generación limitadas. Además de la enorme potencia computacional necesaria para generar secuencialmente fotogramas de vídeo coherentes, entrenar estos modelos puede resultar complicado debido a:

- _Mantener la coherencia temporal y espacial entre fotogramas_ para lograr resultados de vídeo realistas y sin distorsiones.
- _Falta de datos de entrenamiento_ con subtítulos y metadatos de alta calidad necesarios para entrenar los modelos de vídeo.
- _La creación_ de subtítulos para vídeos, al ser una tarea clara y descriptiva, requiere mucho tiempo y va más allá de redactar breves fragmentos de texto. Los subtítulos deben describir la narrativa y las escenas de cada secuencia para que el modelo pueda aprender y relacionar los complejos patrones del vídeo con el texto.

Por estos motivos, no se había producido ningún avance significativo en los modelos de generación de vídeo hasta el anuncio del modelo Sora de OpenAI.

Sora es un modelo generalista de transformación por difusión de visión a gran escala, capaz de generar vídeos e imágenes de diversas duraciones, relaciones de aspecto y resoluciones, hasta un minuto completo de vídeo en alta definición. Su arquitectura se basa en los transformadores comúnmente utilizados en los modelos LLM y en el proceso de difusión. Mientras que los modelos LLM utilizan tokens de texto, Sora utiliza parches visuales.

---

**Consejo**
El modelo Sora combina elementos y principios de las arquitecturas Transformer y SD, mientras que en [el Ejemplo 3-10](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#video_model_loading) , se utilizó el modelo SD de Stability AI para generar vídeos.

---

¿Qué hace que Sora sea diferente?

Los transformadores han demostrado una notable escalabilidad en modelos de lenguaje, visión artificial y generación de imágenes, por lo que tenía sentido que la arquitectura de Sora se basara en transformadores para procesar diversas entradas como texto, imágenes o fotogramas de vídeo. Además, dado que los transformadores pueden comprender patrones complejos y dependencias de largo alcance en datos secuenciales, Sora, como transformador de visión, también puede capturar relaciones temporales y espaciales detalladas entre fotogramas de vídeo para generar fotogramas coherentes con transiciones suaves entre ellos (es decir, que exhiben consistencia temporal).

Además, Sora aprovecha las capacidades de los modelos SD para generar fotogramas de vídeo de alta calidad y visualmente coherentes, con controles precisos mediante el proceso iterativo de reducción de ruido. El proceso de difusión permite a Sora generar imágenes con gran detalle y propiedades deseables.

Al combinar el razonamiento secuencial de los transformadores con el refinamiento iterativo de la SD, Sora puede generar vídeos de alta resolución, coherentes y fluidos a partir de entradas multimodales como texto e imágenes que contienen conceptos abstractos.

La arquitectura de red de Sora también está diseñada para reducir la dimensionalidad mediante una red en forma de U, donde los datos visuales de alta dimensión se comprimen y codifican en un espacio latente con ruido. Posteriormente, Sora puede generar parches a partir de este espacio latente mediante un proceso de difusión para la eliminación de ruido.

El proceso de difusión es similar a los modelos SD basados ​​en imágenes. En lugar de tener una U-Net 2D que se usa normalmente para imágenes, OpenAI ha entrenado una U-Net 3D donde la tercera dimensión es una secuencia de fotogramas a lo largo del tiempo (creando un video), como se muestra en [la Figura 3-20](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#images_to_videos) .
![[Pasted image 20260528213346.png]]

OpenAI ha demostrado que, al comprimir los vídeos en fragmentos, como se muestra en [la Figura 3-21](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#videos_to_patches) , el modelo puede lograr escalabilidad en el aprendizaje de representaciones de alta dimensión al entrenarse con diversos tipos de vídeos e imágenes que varían en resolución, duración y relación de aspecto.

![[Pasted image 20260528213558.png]]

Mediante el proceso de difusión, Sora procesa los fragmentos de entrada ruidosos para generar vídeos e imágenes nítidos en cualquier relación de aspecto, tamaño y resolución para dispositivos, directamente en sus tamaños de pantalla nativos.

Mientras que un transformador de texto predice el siguiente token en una secuencia de texto, el transformador de visión de Sora predice el siguiente parche para generar una imagen o un video, como se muestra en [la Figura 3-22](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#vision_transformer_sequence).

![[Pasted image 20260528213727.png]]


