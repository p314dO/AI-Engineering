
---

**Objetivos del capítulo**
En este capítulo aprenderás sobre:
- Qué es FastAPI
- Cómo empezar a crear tu propio proyecto FastAPI
- Características y ventajas de FastAPI
- Cómo estructurar proyectos FastAPI
- El patrón de diseño de software en capas/cebolla
- Comparación de FastAPI con otros frameworks
- Limitaciones de FastAPI
- Configurar un entorno Python administrado y las herramientas necesarias para su proyecto.

---

Al finalizar este capítulo, debería sentirse cómodo utilizando el marco web FastAPI, configurando proyectos FastAPI y explicando sus decisiones sobre la pila tecnológica para crear servicios GenAI.

# Introducción a FastAPI
[FastAPI](https://oreil.ly/2xcoR) es un framework web de interfaz de puerta de enlace asíncrona (ASGI) que permite crear API ligeras y servidores web backend. Al ser un framework ASGI, puede aprovechar la concurrencia para procesar solicitudes web. Es [rápido, comparable a los frameworks modernos](https://oreil.ly/tgwEJ) , y además incluye sólidas [integraciones con Swagger/OpenAPI para la autodocumentación](https://oreil.ly/WlwOC) , junto con funciones integradas de validación y serialización de datos a través de [Pydantic](https://oreil.ly/5-EmU) . [1](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#id507) En efecto, FastAPI es un envoltorio sobre el [framework Starlette](https://oreil.ly/tyKtQ) , creado por Encode, los mismos que crearon el framework REST de Django. Es ligero y ofrece una experiencia de desarrollo similar.

Antes de analizar FastAPI con más detalle, configuremos su entorno de desarrollo con una aplicación FastAPI en funcionamiento.

# Configuración del entorno de desarrollo
A lo largo del resto de este capítulo, te guiaré a través del proceso de instalación de FastAPI y sus dependencias esenciales, lo que te permitirá configurar un servidor web básico. También instalaremos una selección de formateadores, registradores y analizadores de código que podrás configurar para optimizar tu flujo de trabajo de desarrollo.

---

**Advertencia**
Los ejemplos de código de este libro se han probado con Python 3.11. Ejecutarlos con otras versiones de Python podría generar problemas. Además, algunos entornos de implementación y dependencias de paquetes podrían no ser compatibles con las versiones más recientes de Python.

---

Ahora puedes comenzar a configurar tu proyecto FastAPI.

## Instalación de Python, FastAPI y paquetes necesarios
Si estás en Windows, puedes usarlo `conda`para crear un entorno virtual de Python:
```
conda create -n genaiservice python=3.11
conda activate genaiservice
```

Si estás en un sistema macOS o Linux, puedes crear un entorno virtual de Python usando `venv`:
```
python3 -m venv .venv
```

`venv`crea tu entorno virtual en la `.venv`carpeta que puedes activar usando esto:
```
source .venv/bin/activate
```

Una vez activado el entorno, puede instalar los paquetes principales necesarios para ejecutar el servidor FastAPI y atender las solicitudes de la API de OpenAI:
```
pip install `"fastapi[standard]"` uvicorn openai
```

El `uvicorn`paquete es el servidor web básico sobre el que se ejecuta FastAPI. `fastapi`También instalará sus paquetes de dependencia, como `starlette`y `pydantic`.

## Creación de un servidor web FastAPI sencillo
Una vez instalados FastAPI y sus dependencias, estará listo para iniciar su propio servidor web. Para crear un servidor web sencillo con un único punto final en FastAPI, solo necesita escribir 15 líneas de código. Cree un archivo _main.py_ en la raíz de su directorio, como se muestra en [el Ejemplo 2-1](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#simple_fastapi_web_server) .

##### Ejemplo 2-1. Código de inicio para un servidor web FastAPI simple que atiende solicitudes GPT-4o

```python
from fastapi import FastAPI
from openai import OpenAI
import os
from dotenv import load_dotenv

api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI() #1
openai_client = OpenAI(api_key=api_key) #2

@app.get("/")
def root_controller():
    return {"status":"Healthy"}

@app.get("/chat") #3
def chat_controller(prompt: str = "Inspire me"): #3
    
    response = openai_client.chat.completions.create( #4
        model="gpt-4o",
        messages = [
            {"role":"system", "content": "You are a helpful assistant."},
            {"role":"user", "content":prompt},
        ],
    )

    statement = response.choice[0].message.content
    return {"statement": statement} #5
```

  
1 - Cree un objeto de aplicación FastAPI.
2 - Necesitarás una [clave API](https://oreil.ly/PP0nN) para usar la API de OpenAI.
3 - Utilice el `@app.get`decorador para crear un `GET`punto final en la `/chat`ruta.
4 - Realice una llamada a la API de OpenAI Completions para generar una respuesta del `gpt-4o`modelo.
5 - Cualquier dato que devuelva la función decorada se devolverá cuando acceda al punto final raíz.

Ahora puede iniciar el servidor usando el `fastapi dev`comando, como se muestra aquí:
```
fastapi dev
```

![[Pasted image 20260527124528.png]]

Ahora se puede acceder a su servidor web desde `http://127.0.0.1:8000`dos puntos finales expuestos en la raíz `/`y `/chat`las rutas.

Si accedes `http://127.0.0.1:8000`a través de tu navegador, deberías ver el `{"status": "healthy"}`mensaje. Además, cuando visites `http://127.0.0.1:8000/chat`, deberías ver un mensaje inspirador del `gpt-4o`modelo de OpenAI.

Enhorabuena. Ya dispone de un servicio de IA generativa básico totalmente funcional.

---

**Consejo**
Al iniciar el servidor en modo de desarrollo mediante el `fastapi dev`comando, un proceso de monitorización de archivos está atento a los cambios en su proyecto y actualiza automáticamente el servicio a medida que actualiza el código.

---

Puedes cambiar el mensaje predeterminado y actualizar el navegador para ver los cambios reflejados en tiempo real.

El `app`objeto, que se crea a partir de la `FastAPI`clase, convierte tu función de Python con un decorador en un punto final del Protocolo de Transferencia de Hipertexto (HTTP). Puedes activar ambos puntos finales enviando una solicitud HTTP.

Internamente, el `uvicorn`paquete toma el `app`objeto e inicia un servidor web que ejecuta su servicio FastAPI.

Además de obtener un servidor web sencillo listo para usar, también recibirá documentación de API generada automáticamente. Esta documentación sigue el estándar OpenAPI e incluye una `openapi.json`especificación de su servicio web y una página de documentación Swagger creada a partir del mismo archivo de especificación.

Puedes acceder a la página de documentación autogenerada yendo a la `/docs`ruta de tu servidor a través de `http://localhost:8000/docs`; verás una página similar a [la Figura 2-1](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#swagger_docs) .
![[Pasted image 20260527125046.png]]

Desde la página de documentación de Swagger, puedes enviar solicitudes a tu API para probar rápidamente un endpoint. La página de documentación también se encargará de enviar los encabezados, métodos y parámetros de solicitud correctos.

Lo que me encanta de la página de documentación de Swagger es que permite iterar rápidamente sobre diversas implementaciones mediante la interfaz de usuario, lo cual puede ser más rápido que escribir pruebas al iterar sobre el diseño de las API. Sin embargo, esto no reemplaza las pruebas tradicionales que verifican cada endpoint al realizar cambios. A medida que la aplicación crece, sigue siendo útil escribir pruebas. Una vez que las firmas de los endpoints estén bien definidas, se pueden escribir `pytest`pruebas para evaluar sistemáticamente el servicio web de principio a fin.

Además de la autodocumentación, FastAPI incluye la serialización y validación automática de datos. En [el Ejemplo 2-1](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#simple_fastapi_web_server) , devolvimos un diccionario en el controlador raíz cuando visitaste `http://localhost:8000`. Para que los datos se muestren en tu navegador, se requiere un proceso complejo. Primero, los datos deben serializarse desde un objeto Python, como un diccionario o una lista, a una cadena JSON (JavaScript Object Notation). Posteriormente, se transfieren a través de la web y tu navegador los deserializa de nuevo a un objeto JavaScript una vez completada la transmisión. Así es como las aplicaciones web se comunican entre sí.

Ahora que ya tienes un servidor FastAPI en funcionamiento, veamos las características y ventajas de FastAPI que puedes utilizar en tu proyecto.

---

# Características y ventajas de FastAPI
Necesitas un framework web adecuado que te permita crear tus servicios de IA generativa sin complicaciones. Este framework debe incluir todos los elementos esenciales de seguridad, autenticación y rendimiento, a la vez que te ofrece la flexibilidad necesaria para incorporar funciones e integraciones adicionales a medida que tu aplicación se vuelve más compleja.

[FastAPI cumple con la mayoría de estos criterios, ya que ofrece diversas funciones y ventajas de forma predeterminada](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#fastapi_limitations) . Sin embargo, como se explicará más adelante en este capítulo, los casos de uso avanzados, como las cargas de trabajo de IA que requieren muchos recursos, pueden necesitar marcos de trabajo o soluciones web especializadas, como se abordará en [el Capítulo 3](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#ch03) .

Por ahora, revisemos las características y ventajas de FastAPI antes de analizar sus limitaciones en el contexto de la creación de servicios de IA generativa.

## Inspirado en el patrón de enrutamiento de Flask.
Tanto en Flask como en FastAPI, puedes crear cualquier ruta decorando una función con un decorador especializado. Luego, puedes configurar las rutas para que acepten y validen encabezados, cookies, cuerpo, ruta y parámetros de consulta, según tu implementación.

## Manejo de operaciones asíncronas y síncronas
Al desarrollar servicios, estos deben poder gestionar múltiples solicitudes de varios usuarios para aumentar la eficiencia a medida que crece la demanda. FastAPI puede [gestionar sin problemas funciones síncronas y asíncronas en su aplicación](https://oreil.ly/gNYMg) para habilitar la concurrencia desde el principio.

Como veremos en detalle en [el Capítulo 5](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch05.html#ch05) , si define una ruta asíncrona usando `async def`, FastAPI la ejecutará en el hilo principal en el bucle principal de eventos. Por otro lado, si define una ruta síncrona (no declarada con la `async`palabra clave), FastAPI la ejecutará en un _hilo de trabajo_ para gestionar cargas de trabajo concurrentes.

---

**Advertencia**
La ejecución de operaciones multihilo conlleva una sobrecarga adicional en comparación con su ejecución asíncrona. Por lo tanto, contar con muchas rutas síncronas puede limitar la escalabilidad de su aplicación.

---

Como resultado, las solicitudes concurrentes no bloquearán el hilo principal del servidor. Esto es particularmente útil al trabajar con operaciones de entrada/salida, como consultar bases de datos, intercambiar datos con unidades de procesamiento gráfico (GPU) [³](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#id527) o realizar solicitudes HTTP.

## Soporte integrado para tareas en segundo plano
Puedes crear rutas capaces de manejar tareas de larga duración (por ejemplo, enviar correos electrónicos) sin necesidad de bibliotecas externas (por ejemplo, `celery`). FastAPI incluye una [función de tareas en segundo plano](https://oreil.ly/aO6ml) [4](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#id530) para trabajar con sistemas que necesitan tiempo para procesar datos, pero no quieres que retrasen la devolución de las respuestas a las solicitudes.

No todas las tareas pueden ser atendidas con la paciencia que tus usuarios tienen. No querrás hacerlos esperar mientras el proceso continúa. Puedes delegar la operación de larga duración a una tarea en segundo plano que se ejecute en un hilo independiente, después de responder al cliente. Como respuesta, puedes informar a los clientes que tu servicio ha aceptado su solicitud y la ha puesto en cola para procesarla en segundo plano.

Por ejemplo, en los servicios de GenAI se pueden usar tareas en segundo plano para procesar documentos grandes cargados en una base de datos vectorial sin bloquear el servidor. Esto permite que el servidor atienda otras solicitudes mientras el procesamiento de documentos se realiza en segundo plano.

Aprenderás a construir un sistema de este tipo en [el Capítulo 5](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch05.html#ch05) .

## Soporte para middleware personalizado y CORS
FastAPI te permite añadir [componentes de middleware](https://oreil.ly/uvlLC) a tu enrutador de aplicaciones para interceptar la comunicación entre los puntos finales de tu API y los clientes. Cada middleware, ubicado delante de tus puntos finales, te permite acceder a los objetos de solicitud y respuesta para modificarlos según sea necesario. Puedes añadir lógica sobre cómo se deben procesar las solicitudes antes de que se entreguen a los manejadores de ruta. Una vez generada la respuesta, puedes realizar operaciones sobre ella, como modificar encabezados, registrar eventos y establecer cookies, antes de enviarla al cliente.

Un patrón común en el desarrollo de backend es usar middleware para [agregar encabezados adicionales a una respuesta](https://oreil.ly/Yfsqg) , realizar comprobaciones básicas en las solicitudes entrantes, admitir [solicitudes CORS](https://oreil.ly/6u1dI) , [registrar y monitorear las comunicaciones](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch03.html#middleware_monitoring) , y mucho más. Incluso puedes aprovechar middleware de terceros y [personalizado](https://oreil.ly/AJKJt).

## Libertad para personalizar cualquier capa de servicio.
En ocasiones, es posible que desee liberarse de las limitaciones de su framework web actual. FastAPI ofrece una solución al permitirle definir clases personalizadas que heredan las clases base de Starlette, el framework web subyacente. Por ejemplo, puede [sobrescribir los manejadores de excepciones predeterminados](https://oreil.ly/qgvgO) , agregar [middleware ASGI personalizado](https://oreil.ly/1A8OD) o incluso [crear respuestas personalizadas](https://oreil.ly/jLXUf) .

Gracias a la potencia de los codificadores de Pydantic o [FastAPI](https://oreil.ly/MJmqJ) , también puedes crear fácilmente tus propios [serializadores personalizados](https://oreil.ly/UnzRk) para ajustar la forma en que se manejan los objetos de fecha y hora.

Esto te permite implementar funciones según tus preferencias sin tener que luchar contra FastAPI.

## Validación y serialización de datos
Para las aplicaciones que manejan grandes cantidades de datos, es importante que los datos que se van a procesar estén limpios y en un formato conocido.

A medida que aumenta la complejidad de su servicio, necesitará realizar la validación y serialización de datos. En FastAPI, puede usar Pydantic para serializar automáticamente los tipos de datos comunes (por ejemplo, listas, diccionarios, tipos primitivos) al devolverlos en las rutas de la API. También puede definir sus propios esquemas de Pydantic para los datos de solicitud y respuesta, lo que le permitirá realizar una validación de datos más rigurosa.

Por ejemplo, puede validar la contraseña de un usuario al crear una cuenta para que coincida con sus políticas de seguridad, como se muestra en [el Ejemplo 2-2](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#data_validation) .

##### Ejemplo 2-2. Validación de contraseñas de usuario en FastAPI mediante un esquema de Pydantic.
```python
from pydantic import BaseModel, Field, EmailStr, field_validator
from fastapi import FastAPI

class UserCreate(BaseModel):
    username: str
    password: str

    # @validator('password') Esta version es vieja
    @field_validator('password') #1
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long.')
        if not any(char.isdigit() for char in value):
            raise ValueError('Password must contain at least one digit.')
        if not any(char.isupper() for char in value):
            raise ValueError('Password must contain at least one uppercase letter')
        return value # 2
    
app = FastAPI()

@app.post("/user")
async def create_user_controller(user: UserCreate):
    return {"name": user.username, "message":"Account successfully created"}
```

1 - Defina un modelo Pydantic con validación de datos personalizada en el `password`campo.
2 - Levanta una alerta `ValueError`si no se cumple alguna de las políticas de contraseñas.

Esto le permite detectar, manejar y proteger sus servicios de problemas de datos que no son detectados por verificadores de tipos estáticos como `mypy`.

Los validadores de Pydantic también permiten validar tipos de datos más complejos en tiempo de ejecución, como correos electrónicos, URL, UUID y más. [El capítulo 4](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch04.html#ch04) explicará con más detalle cómo realizar la validación de datos con Pydantic.

## Rico ecosistema de complementos
Los plugins son paquetes de Python que se integran con las funcionalidades y el funcionamiento interno de FastAPI. Son similares a cualquier otro paquete de Python que instales e importes en tus scripts, y requieren una configuración mínima tras la instalación. Integrarlos te permite ampliar las funcionalidades de tu servicio sin preocuparte por el orden de las integraciones ni por problemas de compatibilidad. Además, puedes eliminarlos sin que la aplicación deje de funcionar.

Algunos complementos conocidos incluyen FastAPI Filters, Auth Users, Rate Limiting y varios otros, que puedes ver en el [repositorio Awesome FastAPI de GitHub](https://oreil.ly/nKbvP).

## Documentación automática
Con FastAPI, la documentación de Swagger UI se genera automáticamente para que puedas visualizar y probar las rutas que crees, como se muestra en [la Figura 2-1](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#swagger_docs) . Durante el desarrollo, contar con una página de documentación interactiva facilita la depuración y la creación de prototipos de tus rutas hasta que desarrolles y mantengas tus propios conjuntos de pruebas.

A medida que crees nuevos puntos de acceso, es posible que quieras volver a visitar la `/docs`página con frecuencia para probarlos.

Puede configurar una redirección desde la URL base `/`al `/docs`punto final para facilitar un acceso más rápido a la página de documentación, como se muestra en [el Ejemplo 2-3](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#setting_up_redirect) .

##### Ejemplo 2-3. Configuración de la redirección a la página de documentación generada automáticamente.
```python
from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse

@app.get("/", include_in_schema=False) #1
def docs_redirect_controller():
    return RedirectResponse(url="/docs", status_code=status.HTTP_303_SEE_OTHER) #2
```

1 - Configura un controlador para el controlador raíz base, pero no lo incluyas en las especificaciones de OpenAPI ni en la página de documentación.
2 - Devuelve una respuesta de redirección a la `/docs`página con un código de estado de redirección para que los navegadores realicen la redirección.

Una vez implementados [los ejemplos 2 y 3](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#setting_up_redirect) , podrá acceder a la `/docs`página durante el desarrollo local siempre que visite la URL base `/`del servicio.

En producción, a menos que su API sea pública, desactive esta redirección y oculte las `/docs`rutas de forma predeterminada para mejorar la seguridad.

---

**Advertencia**
Si tu API es accesible públicamente en producción, podrías exponer puntos finales no seguros e información confidencial sobre tu API. Por lo tanto, se recomienda [desactivar la página de documentación](https://oreil.ly/Dk45G) .

En cambio, puede mostrar la `/docs`página explícitamente solo en entornos seleccionados.

---

Para las API públicas, puedes configurar el controlador raíz `/`para que devuelva la versión de tu API en lugar de redirigir a la `/docs`página.

## Sistema de inyección de dependencias
OtroUn componente potente de FastAPI es su [sistema de inyección de dependencias](https://oreil.ly/eAIwR) basado en un patrón de desarrollo llamado _inversión de control_ . Usando este patrón, se divide una función en una serie de funciones que se inyectan en otras funciones como _dependencias_ .

Además de ayudar a estructurar la lógica de tu aplicación, las dependencias pueden ayudarte a reducir la duplicación. Te permiten compartir y reutilizar la lógica en toda tu API, reutilizar conexiones de base de datos abiertas, aplicar medidas de seguridad como requisitos de autenticación o autorización, y mucho más.

Por ejemplo, puede especificar parámetros de consulta comunes en todas las rutas de la API (por ejemplo, para paginación y filtrado), como se muestra en [el Ejemplo 2-4](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#dependency_pagination) .

##### Ejemplo 2-4. Reducción de la duplicación mediante una dependencia de paginación.
```python
from fastapi import FastAPI, Depends

app = FastAPI()

def paginate(skip: int=0, limit:int=10):
    return {"skip":skip, "limit":limit}

@app.get("/messages")
def list_messages_controller(pagination:dict=Depends(paginate)):
    return ...  # filter and paginate results using pagination params

@app.get("/conversations")
def list_conversations_controller(pagination:dict=Depends(paginate)):
    return ...  # filter and paginate results using pagination params
```

En FastAPI, las dependencias también se almacenan en caché dentro _del contexto de una única solicitud_ para evitar cálculos duplicados. Esto significa que una función de dependencia se ejecuta solo una vez por solicitud, y su resultado se reutiliza durante la duración de esa solicitud si se necesita nuevamente. Sin embargo, en una nueva solicitud, la función de dependencia se ejecuta de nuevo.

Gestionar las conexiones a la base de datos o verificar las credenciales del usuario en cada controlador de ruta es tedioso y viola el principio DRY ( _Don't Repeat Yourself_ ) de programación. Otro caso de uso importante del sistema de inyección de dependencias es cuando se crea una conexión a la base de datos y se desea reutilizarla para realizar múltiples solicitudes de obtención de datos mientras se procesa una sola solicitud.

Puedes crear dependencias para las funciones de tu controlador de ruta, como se muestra en [el Ejemplo 2-5](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#fastapi_dependency) .
##### Ejemplo 2-5. Inyección de dependencias en FastAPI.
```python
from fastapi import FastAPI, Depends

def get_db(): # 1
    db = ... #Create Database session
    try:
        yield db # 2
    finally:
        db.close() # 3

app = FastAPI()

@app.get("user/{email}/messages")
def get_current_user_messages(email, db=Depends(get_db)): # 4
    user = db.query(...) # db is reused
    messages = db.query(...) #db is reused
    return messages # 5
```


1 - Implementar una función para crear y gestionar una sesión de base de datos, que pueda utilizarse como dependencia en los manejadores de rutas.
2 - Cede la sesión de base de datos abierta, haciéndola disponible para cualquier función que dependa de ella `get_db`.
3 - Cierra la sesión de la base de datos una vez procesada la solicitud, evitando así fugas de recursos.
4 - Inyecte la `get_db`dependencia en el controlador de ruta para crear y reutilizar la misma sesión de base de datos durante el ciclo de vida de la solicitud. FastAPI también expondrá automáticamente los parámetros dentro de las dependencias en su punto final.
5 -   Reutilice la sesión de base de datos inyectada para realizar múltiples operaciones de base de datos dentro de una sola solicitud para devolver los mensajes de un usuario.

Como se muestra en [el Ejemplo 2-5](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#fastapi_dependency) , puede inyectar estas dependencias en otras funciones pasándolas como parámetros para `Depends()`que FastAPI evalúe y almacene en caché los resultados de su función.

Aquí se define una función de utilidad para crear una sesión de base de datos y luego se utiliza como dependencia de la `get_current_user_messages`función para inyectar la sesión de base de datos creada.

---

**Grafo de dependencia jerárquica**
También puedes inyectar dependencias dentro de otras dependencias para crear un _gráfico de dependencias jerárquico_ , lo cual es extremadamente útil para construir [flujos de autenticación y autorización en caché](https://oreil.ly/i_xHr) , lógica de recuperación de datos anidada o árboles de decisión complejos al implementar la lógica de negocio de tu aplicación.

Como ejemplo, puede reutilizar las mismas funciones de creación de sesión de base de datos o de obtención de usuarios en diferentes partes de su API, como se muestra en [la Figura 2-2](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#dependency_injection) .
![[Pasted image 20260527142945.png]]

En un gráfico de dependencia jerárquica, como se muestra en [la Figura 2-2](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#dependency_injection) , cada dependencia (y sus subdependencias) puede proporcionar (inyectar) sus resultados a otra función que depende de ella.

---

Este sistema de dependencias es solo una de las muchas características que incluye FastAPI para acelerar y simplificar el proceso de creación de servicios de backend.

## Eventos del ciclo vital
[Los eventos de ciclo de vida de FastAPI](https://oreil.ly/Cn2DB) son excelentes para gestionar la inicialización y la limpieza de su servicio cuando necesita configurar recursos que se puedan compartir entre solicitudes. [5](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#id554) Durante el inicio del servidor, puede crear grupos de conexiones de base de datos o cargar modelos GenAI en memoria para su reutilización en diferentes solicitudes. Posteriormente, antes del apagado del servidor, puede realizar la limpieza descargando los modelos de IA, cerrando los grupos de conexiones, eliminando los artefactos temporales y registrando los eventos.

Mediante el uso de eventos de ciclo de vida, su servicio FastAPI realiza operaciones de larga duración, como la carga del modelo, al inicio, antes de atender las solicitudes, y lo mantiene cargado para su reutilización entre solicitudes. Durante el apagado del servidor, puede finalizar de forma segura todas las solicitudes restantes y en cola antes de ejecutar cualquier operación de limpieza.

## Componentes de seguridad y autenticación
Como con cualquier otro framework, necesitarás componentes de seguridad y autenticación para proteger tu servicio. FastAPI no te obliga a usar una implementación específica de la capa de seguridad y autenticación. Te proporciona un conjunto de [componentes de seguridad](https://oreil.ly/zlAgl) para que puedas proteger tus servicios según tus propias necesidades.

[En el capítulo 8](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch08.html#ch08) aprenderás a implementar una capa de autenticación desde cero para tus servicios GenAI .

---

**Consejo**
Si no quieres implementar una capa de autenticación desde cero, también puedes recurrir a complementos de terceros como [FastAPI Users](https://oreil.ly/eEtMe) , que se encargan automáticamente de ello.

---

También puede integrarse con proveedores de autenticación de terceros para [flujos de inicio de sesión único en FastAPI](https://oreil.ly/vIqCd) en entornos empresariales.

## Compatibilidad con Web Socket bidireccional, GraphQL y respuestas personalizadas.
Al crear servicios, a menudo necesitará ir más allá de los _puntos finales_ _REST estándar_ .

---
**Puntos finales REST**
_Representational State Transfer_ (REST) ​​es un estilo arquitectónico para diseñar API donde se utilizan métodos HTTP comunes como `GET`, `POST`, `PUT`, y `DELETE`para acceder y manipular recursos.

Los siguientes son ejemplos comunes de puntos finales REST:
`GET endpoint /api/messages`
Recuperar una lista de mensajes.

`POST endpoint /api/messages`
Crear un nuevo mensaje.

`GET endpoint /api/messages/\{id}`
Recuperar un mensaje específico por ID.

`PUT endpoint /api/messages/\{id}`
Actualizar un mensaje específico por ID.

`PATCH endpoint /api/messages/\{id}`
Realizar una actualización parcial de un mensaje específico por ID.

`DELETE endpoint /api/messages/\{id}`
Eliminar un mensaje específico por ID.

La mayoría de las API externas en la web se basan en el patrón arquitectónico REST debido a su escalabilidad, simplicidad y naturaleza sin estado (es decir, las respuestas a cada solicitud pueden ser independientes de las demás).

---

Si estás desarrollando una aplicación de chat, es posible que también necesites comunicación cliente-servidor en tiempo real o conexiones de mayor duración donde los datos se transmitan en una dirección. Los puntos finales de WebSocket (WS) y de eventos enviados por el servidor (SSE) pueden ayudarte a transmitir los resultados de los modelos generativos a los clientes, como verás en el [Capítulo 6](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch06.html#ch06) sobre la comunicación en tiempo real con servicios de IA.

En otros casos, es posible que desee utilizar [GraphQL en FastAPI](https://oreil.ly/SL62a) para exponer puntos finales que puedan devolver esquemas dinámicos según la solicitud. FastAPI puede usar el [`strawberry`paquete](https://oreil.ly/wIzvi) [6](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#id561) para aprovechar GraphQL y utilizar esquemas dinámicos en su servicio API, de modo que los clientes puedan seleccionar los campos que deseen de un recurso y evitar así la sobrecarga de datos de su servicio. Sin embargo, no abordaremos el uso de GraphQL en este libro.

## Integración moderna de Python e IDE con valores predeterminados sensatos.
Dado que la pila tecnológica de FastAPI se basa en Python moderno (por ejemplo, con anotaciones de tipo y cadenas de documentación), todos los analizadores y formateadores de IDE pueden comprobar y formatear el código de forma nativa. La configuración predeterminada también es suficiente para empezar importando e instanciando la clase FastAPI. Gracias a su perfecta integración con las características modernas de IDE y Python, cualquiera puede empezar fácilmente a crear, probar, depurar e implementar sus propios servicios FastAPI.

# Estructuras del proyecto FastAPI
A menudo, al trabajar en un proyecto real, terminarás creando servicios que abarcan varios módulos, paquetes y directorios anidados. La decisión sobre cómo estructurar tu proyecto dependerá totalmente de ti.

Aquí es donde la mayoría de la gente tendrá dificultades y terminará con un código demasiado complejo para manejar. Acabarás frustrado, teniendo que comprender el código y la estructura del proyecto antes de poder contribuir. En algún momento, la complejidad aumentará tanto que te dará pavor volver a tocar el proyecto.

Algunos archivos terminarán siendo demasiado grandes para leer debido a funciones sobrecargadas, o habrá demasiados archivos dispersos por todas partes. También podrías terminar con millones de errores de importación o dependencias circulares que dañen tu aplicación.

Aprender a estructurar aplicaciones más grandes será aún más importante al trabajar con modelos de IA generativa. Estos modelos suelen necesitar dependencias y funciones de utilidad adicionales para su funcionamiento. Por lo tanto, deberá agregar una capa de complejidad a sus modelos sobre las capas de aplicaciones existentes.

---
**Consejo**
En comparación con los frameworks con una filosofía muy definida, como Django, en frameworks más flexibles como FastAPI es necesario seguir buenas prácticas para tener éxito en proyectos de mayor envergadura.

---

En los últimos años, trabajando con FastAPI y aplicaciones de ciencia de datos, he visto a muchos desarrolladores crear sus propias plantillas predefinidas para iniciar proyectos FastAPI. Algunos incluso recomiendan seguir una estructura popularizada por el proyecto Netflix Dispatch FastAPI para aplicaciones API más grandes, la cual ha inspirado otras plantillas.

A la hora de desarrollar aplicaciones reales, es fundamental mantener el código lo más estructurado posible. Esto redundará en tu propio beneficio, ya que te ayudará a ti y a los demás miembros de tu equipo a comprender el código en el futuro.

Sabes que tienes una buena estructura de proyecto si puedes encontrar cualquier función o componente dentro de tu código. Si empiezas a cuestionar la finalidad de un directorio o pasas horas buscando un fragmento de código, es posible que la estructura de tu proyecto no sea clara y resulte demasiado compleja para comprenderla.

En estos casos, puedes recurrir a algunas estructuras de proyecto comunes que se han popularizado recientemente en la comunidad FastAPI. Existen varias estructuras de proyecto que puedes adoptar: plana, anidada y modular.

Analicemos cada uno de ellos en detalle.

## Estructura plana
Una estructura plana es aquella en la que los archivos de la aplicación permanecen en la raíz del proyecto, sin subdirectorios. Para una mejor organización, puedes agrupar todos tus archivos en un único directorio.

La idea principal es mantener todo el código similar en módulos y ubicarlo cerca de la raíz del proyecto. Por ejemplo, coloque todos sus modelos de base de datos en _models.py_ o sus endpoints en _routes.py_ .

La estructura de proyecto más común es, sin duda, la plana, debido a su simplicidad y facilidad de uso. Esta estructura suele ser ideal para crear la primera versión de un servicio o un conjunto pequeño de microservicios. [El ejemplo 2-6](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#flat_structure) muestra cómo podría ser dicha estructura.

##### Ejemplo 2-6. Estructura de proyecto FastAPI plana
![[Pasted image 20260527150523.png]]

Como se puede observar en la estructura mostrada en [el Ejemplo 2-6](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#flat_structure) , hay algunos archivos que contienen la lógica principal de la aplicación. Si se está desarrollando un microservicio con FastAPI, por definición, conviene mantener una estructura plana para mayor simplicidad.

La simplicidad de la estructura plana permite centrarse en el desarrollo en lugar de en la estructura. Hay pocos archivos de los que preocuparse. Tampoco es necesario preocuparse por el acoplamiento, la descomposición o la reutilización, ya que hay pocas líneas de código con las que lidiar.

Por otro lado, la estructura plana será difícil de mantener a medida que tu proyecto se vuelva más complejo. En este punto, tiene sentido dividir los módulos globales de Python en paquetes propios utilizando la estructura anidada.

## Estructura anidada
La estructura anidada agrupa módulos similares en paquetes, creando así una jerarquía de módulos. Se agrupan todos los módulos similares dentro de un paquete, independientemente de la funcionalidad que soporten. Estos son módulos débilmente acoplados que contienen lógica similar para diferentes entidades del proyecto. Por ejemplo, el `models`paquete puede contener `users`modelos `profiles`de base de datos.

La documentación oficial de FastAPI recomienda la estructura anidada para proyectos de mayor envergadura .

Puedes ver un proyecto con estructura anidada en [el Ejemplo 2-7](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#nested_structure) .

##### Ejemplo 2-7. Proyecto FastAPI anidado
![[Pasted image 20260527150702.png]]

A medida que incorpore modelos de IA y diversos servicios y bases de datos externos a su proyecto, podrá adoptar una estructura anidada para gestionar la creciente complejidad.

El principal inconveniente de esta estructura de proyecto es el acoplamiento ambiguo de los módulos. Los cambios en un módulo pueden propagarse a otros, y puede resultar difícil comprender el efecto en cascada de los nuevos cambios. Con el tiempo, puede resultar difícil mantener y modificar el código sin realizar numerosas actualizaciones en otras partes del sistema. Esto se conoce como _actualizaciones masivas_ . En el contexto del desarrollo de software, las actualizaciones masivas se producen cuando resulta difícil mantener y modificar el código sin realizar numerosas actualizaciones en otras partes del sistema.

Si prevé dificultades para gestionar el acoplamiento de módulos o si espera tener que trabajar con una aplicación de gran tamaño, le recomiendo utilizar una estructura modular.

## Estructura modular
La estructura modular —popularizada por el proyecto Netflix Dispatch FastAPI— es similar a la estructura anidada, ya que permite colocar varios módulos dentro de un paquete y subpaquetes. Sin embargo, la principal diferencia radica en cómo se organiza el proyecto.

En la estructura modular, los módulos estrechamente relacionados que pertenecen a un dominio específico se agrupan. Este enfoque difiere de la estructura anidada mencionada anteriormente. Un ejemplo podría ser el `users`paquete que contiene esquemas de usuario, servicios de base de datos, dependencias y enrutadores.

Para comprender mejor esta diferencia, consulte el [Ejemplo 2-8](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#modular_structure) .

##### Ejemplo 2-8. Estructura de proyecto modular FastAPI
![[Pasted image 20260527151059.png]]

En una estructura de proyecto modular como la que se muestra en el [Ejemplo 2-8](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#modular_structure) , se agrupan componentes estrechamente interconectados en función de una funcionalidad o un sistema global que implementan (por ejemplo, autenticación, procesamiento de pagos, notificaciones, etc.) o del recurso con el que interactúan (por ejemplo, usuarios, perfiles, mensajes, etc.). Este tipo de encapsulación elimina cualquier incertidumbre respecto a las interdependencias en el código, lo que se traduce en una mayor escalabilidad y facilidad de mantenimiento.

Si necesitas incluir más funcionalidades, puedes crear un nuevo paquete que contenga todo el código necesario. Del mismo modo, si necesitas modificar o eliminar código, puedes determinar fácilmente dónde realizar los cambios y prever cómo afectarán a otras partes del código. Esto es posible gracias a que la estructura del código es transparente y está bien encapsulada, lo que permite identificar claramente las conexiones entre los diferentes componentes.

## Reorganización progresiva de su proyecto FastAPI
Un código base modular permite añadir y eliminar componentes con facilidad. Además, puedes reutilizar componentes en diferentes partes del sistema para evitar la repetición.

Al inicio de tu proyecto, la modularidad no es tan importante. Puedes comenzar con uno o pocos archivos Python para crear tus servicios fácilmente. Sin embargo, en cuanto introduzcas modelos de IA, servicios externos y lógica de negocio compleja, deberás considerar la modularización de tu código.

Puedes lograr la modularidad diseñando los componentes de tu sistema teniendo en cuenta la reutilización y la posibilidad de desecharlos. Asegúrate de que el diseño de tus módulos y funciones permita su uso en diferentes entornos y de que los coloques en el lugar correcto dentro del directorio de tu proyecto. Seleccionar la mejor estructura de proyecto es una cuestión de preferencia. Sin embargo, quizás te preguntes: "¿Qué estructura de proyecto debo adoptar para crear servicios de IA generativa con FastAPI?".

Descubrí que la mejor manera de estructurar proyectos es _reorganizarlos progresivamente,_ pasando de una estructura plana a una modular, a medida que aumenta la complejidad del servicio:

1. Plano
Si estás comenzando un nuevo proyecto y aún no tienes clara la complejidad de tu sistema, puedes concentrarte en escribir todo tu código FastAPI en un solo archivo antes de preocuparte por la estructura del proyecto. Luego, extrae tu código en varios archivos dentro del directorio raíz. Esta es la estructura inicial que adoptarás al experimentar con la primera versión de tu servicio desde cero.

2. Anidado
A medida que aumenta el número de archivos en tu código y la complejidad del servicio, puedes adoptar la estructura anidada. Puedes buscar archivos según su agrupación lógica (modelos, enrutadores, esquemas, etc.) y no preocuparte demasiado por los acoplamientos lógicos en tu código. Al realizar cambios, solo se verán afectados unos pocos archivos. En este punto, tienes un microservicio de IA.

3. Modular
Al pasar de un microservicio a un servicio backend completo, conviene adoptar una estructura modular. Ahora hay un número creciente de módulos, funcionalidades y complejidad. Se empieza a agrupar el código en paquetes según _las áreas de interés_ . El código gestiona ahora las solicitudes, la autenticación, los sistemas externos, etc., a la vez que da soporte a un modelo de IA.

---

**Consejo**
Recuerda que, si no puedes justificar la organización de archivos en tu código fuente ante otro desarrollador, es hora de reconsiderar tu estructura actual.

---

A medida que desarrolles tu servicio GenAI, inevitablemente acabarás con una gran base de código y una aplicación compleja.

Pensar en la estructura de tu aplicación FastAPI de gran tamaño es solo el primer paso para crear servicios de nivel de producción. En el siguiente paso, aprenderás más sobre un patrón de diseño de software que te ayudará a gestionar la complejidad de tus servicios de IA. Este se llama patrón de diseño de aplicaciones _en capas_ o de _cebolla_ , del que hablaremos a continuación.

# Patrón de diseño de aplicación en capas/cebolla
Si planeas desarrollar un servicio backend completo para IA generativa, te resultará útil conocer el patrón de diseño de aplicaciones en capas (o de cebolla), que se puede implementar dentro de estructuras de proyecto anidadas y modulares. El objetivo de este patrón es crear una separación de responsabilidades entre las diferentes partes de tu aplicación para simplificar el proceso de agregar, eliminar y modificar funcionalidades.

El patrón de diseño cebolla también ha influido en los frameworks web de otros lenguajes , como [Nest.js.](https://nestjs.com/)

El diseño de cebolla consta de capas, cada una con una responsabilidad y una dirección de dependencia específicas, como se muestra en [la Figura 2-3](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#onion_design_pattern) . La capa más interna contiene los modelos de dominio y la lógica de negocio, mientras que las capas externas contienen el manejo de rutas (en un servicio API) o el código de interfaz de usuario (al servir plantillas HTML).

Este patrón se denomina «cebolla» porque las capas se construyen unas sobre otras, con el modelo de dominio en el centro, rodeado de capas de abstracción creciente que facilitan la comprobación, el mantenimiento y la flexibilidad en el mantenimiento de los servicios de IA. El núcleo de la aplicación (modelo de dominio y lógica de negocio) se encuentra en las capas internas, y todas las demás capas dependen internamente de él. Este enfoque ayuda a gestionar las dependencias, promueve la separación de responsabilidades y facilita un código base más comprobable y mantenible.
![[Pasted image 20260527153344.png]]

La idea principal de este patrón es el _principio de inversión de dependencias_ , que establece que los módulos de alto nivel no deben depender directamente de la implementación de los módulos de bajo nivel, sino que deben declarar lo que necesitan de estos últimos mediante el sistema de dependencias de FastAPI. De esta forma, el sistema de dependencias puede inyectar la salida de los módulos de bajo nivel para evitar el acoplamiento entre capas.

Para implementar este diseño de software, se divide el servicio como una cebolla compuesta por capas cada vez más profundas. Cada capa (a medida que se avanza desde las capas exteriores a las interiores) introduce componentes que son responsables de un conjunto de tareas:

**Enrutadores API**
Los enrutadores son responsables de agrupar varios controladores/manejadores de rutas para aplicar una lógica común a través de varios controladores.

FastAPI proporciona la `APIRouter`clase que le ayudará con esto.

**Controladores/manejadores de rutas**
Los controladores son responsables de gestionar _las solicitudes_ entrantes y devolver _las respuestas_ al cliente mediante la ejecución lógica de los servicios o proveedores.

Un buen diseño de controlador siempre utiliza dependencias para inyectar los datos o la lógica necesarios para su ejecución. Véase [la figura 2-4](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#api_routers_controllers) .
![[Pasted image 20260527153551.png]]

**Servicios/proveedores**
Los servicios se encargan de combinar u orquestar múltiples operaciones internas para implementar una lógica de negocio (servicios), mientras que los proveedores implementan la interfaz con los sistemas externos.

Los servicios suelen utilizar repositorios para acceder a los datos e implementar lógica de negocio compleja, en lugar de simples operaciones de recuperación y modificación de datos. Cada módulo de su aplicación puede tener su propio servicio.

Los proveedores son similares a los servicios, pero se especializan en interactuar con sistemas externos, como las API internas o de terceros. Algunos ejemplos de proveedores son los clientes para servidores de correo electrónico, pasarelas de pago u otros microservicios.

En esencia, tanto los proveedores como los servicios respaldan la implementación de la lógica de negocio del controlador al facilitar las interacciones internas y externas.

Aquí tienes un ejemplo de cómo funcionan juntos dentro de un controlador de ruta: el `users`servicio de base de datos obtiene el registro de un usuario por correo electrónico y luego utiliza esa información con una pasarela de pago y clientes de servidor de correo electrónico (proveedores) para procesar pagos y enviar correos electrónicos de confirmación.

**Repositories (data adapters)**
Un repositorio es un patrón de diseño que se utiliza al implementar la lógica para el acceso a datos y las operaciones de modificación con fuentes de datos (no debe confundirse con un repositorio Git).

Los repositorios utilizan la asignación objeto-relacional (ORM) o comandos SQL puros para ejecutar consultas en su infraestructura, como una base de datos o un almacén de memoria para recuperar o modificar datos.

Puede implementar una interfaz abstracta en esta capa para garantizar un diseño coherente en todos sus repositorios, utilizando las operaciones de creación, lectura, actualización y eliminación (CRUD). Consulte [la Figura 2-5](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#services_providers_repositories) .
![[Pasted image 20260527153849.png]]

**Esquemas/modelos**
Estos componentes son responsables de garantizar la seguridad de tipos, la estructura y la lógica de validación de sus datos a medida que fluyen a través de su servicio.

También dispondrás de componentes que abarcan varias capas para dar soporte a toda la aplicación:

**Middleware**
Esto gestiona las solicitudes y respuestas antes y después de que se pasen a los controladores de la aplicación/manejadores de ruta (véase [la figura 2-6](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#middlewares) ).
![[Pasted image 20260527154000.png]]


**Dependencias**
Esto incluye funciones reutilizables que usted define y que pueden inyectarse en los controladores para dar soporte a la lógica de negocio. Las dependencias pueden almacenarse en caché y depender de otras dependencias.

**Pipe**
Se trata de funciones de transformación de datos que se pueden utilizar en todas las capas de la aplicación. Algunos ejemplos son los agregadores de datos, los limpiadores, los analizadores sintácticos, los traductores, etc.

**Mappers**
Se trata de mapeadores de datos de un esquema a otro, que a menudo transfieren datos entre capas, como desde el `UserRequest`esquema en una capa de enrutamiento hasta el `UserInDB`esquema en la capa de acceso a datos. Véase [la figura 2-7](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#models_pipes_mappers) .
![[Pasted image 20260527154131.png]]


**Exception filters**
Estos mecanismos gestionan las excepciones de forma consistente en todas las capas.

**Guards**
Estos aseguran y protegen a los controladores contra el abuso. La lógica de autenticación y autorización se puede implementar como dependencias o middleware para actuar como guardias (ver [Figura 2-8](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#guards) ).
![[Pasted image 20260527154254.png]]

Si consulta la estructura modular del proyecto que se muestra en el [Ejemplo 2-8](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#modular_structure) , observará diversos elementos del patrón de diseño de cebolla. Seguir este patrón le ayudará a crear un servicio de IA generativa FastAPI que sea mantenible, comprobable y escalable .

En los próximos capítulos, utilizarás estos patrones para construir el servicio GenAI que se muestra en [la Figura 2-9](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#genai_service) .
![[Pasted image 20260527154320.png]]

A continuación, compararemos FastAPI con otros frameworks.

# Comparación de FastAPI con otros frameworks web de Python
La mayoría de los frameworks web de Python pueden proporcionarte herramientas para crear puntos finales REST, GraphQL, WebSocket y de otros tipos.

Algunos frameworks tienen una filosofía definida, como Django (Python) y Nestjs (JavaScript), mientras que otros no. Flask o FastAPI (Python) y Express (JavaScript) te ofrecen la opción de diseñar la arquitectura de tu servicio como prefieras.

Los frameworks con una estructura definida, como Django (Python) y Nestjs (JavaScript), toman decisiones por ti basándose en ciertas suposiciones sobre cómo proporcionarás los datos a tus componentes. En la práctica, proporcionan estructura, pero restringen lo que puedes hacer. Por lo general, los frameworks con una estructura definida son más fáciles de usar. Por otro lado, los frameworks no dogmáticos como Flask o FastAPI (Python) y Express (JavaScript) son más flexibles, pero pueden ofrecer demasiada libertad: muchas posibilidades para lograr los mismos resultados.

Debido a que los marcos de trabajo flexibles como FastAPI ofrecen tanta libertad para crear servicios, es posible que experimente cierta fatiga al elegir e integrar cada paquete de soporte por su cuenta. Por ejemplo, para trabajar con una base de datos, deberá instalar e integrar varios paquetes que funcionen bien juntos: uno para acceder a la base de datos, otro para migrarla y otro que actúe como un mapeador objeto-relacional (ORM).

Al hacerlo, es posible que surjan problemas de compatibilidad con paquetes antiguos durante la integración. Esto dificulta el trabajo con frameworks no estandarizados, y a menudo se opta por utilizar un framework estandarizado como Django, que incluye un sistema ORM excelente y perfectamente integrado para interactuar con bases de datos.

Django es un framework completo que se promociona como el "framework web de Python para desarrolladores con plazos de entrega ajustados". Incluye un sistema ORM totalmente integrado y repleto de funciones que se encarga de las migraciones de bases de datos y las necesidades de acceso a los datos cuando se proporcionan los modelos de datos.

Además, te proporciona un panel de administración, un sistema de autenticación y autorización de usuarios basado en credenciales, y varias funciones de seguridad web listas para usar, por lo que no tienes que crearlas tú mismo. También lleva mucho tiempo en el mercado, lo que ha fomentado una comunidad activa que ha producido excelente documentación, tutoriales y otros recursos para el framework. En la versión 4.2 de Django, también se ha introducido el soporte para solicitudes asíncronas, lo que te permite incorporar concurrencia a tus servicios. Django espera que adoptes la arquitectura MVC, lo que requiere que definas modelos de datos y vistas. Estas vistas se convierten en rutas que sirven archivos HTML con plantillas, respuestas JSON o cualquier respuesta HTTP de forma predeterminada, incluso sin depender de `django-rest-framework`. Las capas de controlador contendrán el procesamiento de datos principal y la lógica de negocio.

Esto convierte a Django en una excelente opción para _aplicaciones web progresivas_ (PWA) monolíticas que se implementan como un único backend con un frontend. Sin embargo, a medida que las empresas tienden a crear equipos especializados para el desarrollo de backends y frontends, los patrones arquitectónicos de microservicios se están volviendo más populares. Con los microservicios, se busca separar los servicios de backend y frontend, crear APIs en lugar de PWAs y centrarse en mantener los servicios lo más ligeros posible. Si bien con Django también se pueden crear APIs, se puede terminar con una aplicación pesada que ralentice el desarrollo, la implementación y el escalado de los servicios. Por eso, los frameworks flexibles como Flask están ganando popularidad.. [7](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#id589)

Flask incluye la menor cantidad de código posible para la creación de servidores web. A diferencia de FastAPI, Flask no incluye validación de datos, autodocumentación ni un sistema de inyección de dependencias. Estas características suelen ser necesarias para desarrollar servicios backend complejos o que requieren integración con bases de datos y servicios externos.

---

**Nota**
Un nuevo framework web llamado Quart ha intentado solucionar este problema, y ​​se presenta como una buena alternativa a FastAPI. Sin embargo, al momento de escribir este artículo, Quart es relativamente nuevo y, en comparación con otros frameworks, no cuenta con una gran comunidad de usuarios ni con recursos documentados que puedan brindar ayuda en caso de que surja algún problema.

---

Además, Flask se lanzó en 2010 e implementa un protocolo de comunicación llamado _Web Server Gateway Interface_ (WSGI) para el servicio web, lo que significa que las solicitudes se procesan de forma síncrona en comparación con ASGI, que es asíncrono. Asimismo, Flask no está diseñado para manejar un gran número de conexiones simultáneas (como lo haría un framework asíncrono). Sin embargo, esto no limita la cantidad de solicitudes paralelas que el servidor puede manejar por sí solo. En producción, se pueden emplear diversas estrategias (como procesos de trabajo o hilos) para manejar múltiples solicitudes simultáneamente. Además, debido a que Flask implementa WSGI, no admite puntos finales WebSocket, que se utilizan para mantener un canal de comunicación bidireccional persistente entre un cliente y un servidor. Esto se debe a que WSGI no admite WebSocket de forma nativa. Sin embargo, se pueden instalar extensiones de Flask para integrar la compatibilidad con WebSocket.

---

**Asynchronous Server Gateway Interface**
Los frameworks basados ​​en ASGI pueden procesar múltiples solicitudes ejecutando operaciones asíncronas concurrentes en el bucle principal de eventos, lo que les permite manejar un mayor volumen de solicitudes a gran escala.

También puede utilizar un grupo de subprocesos (es decir, un conjunto de subprocesos de trabajo) para realizar tareas síncronas simultáneamente sin bloquear el subproceso principal del servidor. Una vez finalizadas las tareas, estos subprocesos devuelven el control al subproceso principal del servidor web y comparten sus resultados. Cuando un subproceso genera un error, el servidor web recopila información del subproceso de trabajo y envía una respuesta de error al cliente.

Los marcos de trabajo web modernos que implementan el estándar ASGI no solo son más eficientes, sino que también ofrecen compatibilidad con versiones anteriores de WSGI en caso de ser necesario.

---

Flask, al depender de un servidor WSGI, procesa cada solicitud de forma síncrona, mientras que FastAPI utiliza un bucle de eventos para cargas de trabajo concurrentes. Por lo tanto, FastAPI será mucho más rápido con tareas que requieren mucha entrada/salida (E/S), como por ejemplo, al comunicarse con una API externa o un almacén de datos, lo que bloquearía todo un proceso de trabajo en Flask.

En esencia, recomiendo Django y otros frameworks si quieres crear monolitos PWA, y Flask o Quart para API sencillas, y frameworks en otros lenguajes si tienes más experiencia con ellos.

Sin embargo, si estás creando un servicio de backend que requiere soporte para modelos de IA, conexión a sistemas externos y cierto nivel de complejidad en la lógica de negocio, te recomiendo considerar FastAPI como el framework web más adecuado..

# Limitaciones de FastAPI
Dadas las características y ventajas mencionadas, también existen varios inconvenientes y desventajas que debe considerar si va a adoptar FastAPI para su proyecto. En lo que respecta a los casos de uso de IA, FastAPI presenta deficiencias en varios aspectos.

## Gestión ineficiente de la memoria del modelo
FastAPI ofrece mecanismos integrados para compartir la memoria del modelo entre varias instancias o procesos del mismo contenedor. Esto significa que, al escalar los web workers horizontalmente, es necesario cargar una nueva instancia del modelo en la memoria del contenedor. Esto genera un cuello de botella de memoria y aumenta los costos operativos de los servicios de GenAI con alto tráfico.

## Número limitado de hilos
Existe un límite en la cantidad de subprocesos que FastAPI crea al iniciar la aplicación en el grupo de subprocesos interno. [8](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#id601)

Esto significa que también existe un límite en cuanto a la escalabilidad de una única instancia de FastAPI, especialmente con cargas de trabajo de IA que implican operaciones de E/S intensivas, así como operaciones que consumen muchos recursos de CPU/GPU. [9](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#id602)

## Restringido al bloqueo del intérprete global
En Python, el uso de múltiples hilos puede producir resultados poco intuitivos y, a menudo, contraproducentes debido al _Bloqueo Global del Intérprete_ (GIL).

FastAPI utiliza multihilo mediante un grupo de subprocesos interno para gestionar las solicitudes web concurrentes que llegan a una ruta síncrona. Sin embargo, incluso con puntos finales asíncronos, las solicitudes de inferencia de IA pueden bloquear el bucle principal de eventos, impidiendo que todas las demás solicitudes se procesen en el hilo principal del servidor web.

Esto se debe a que las cargas de trabajo de inferencia de IA son intensivas en CPU/GPU. Las operaciones que no son de E/S, como servir un modelo costoso o agregar grandes cantidades de datos en un trabajador, harán que otros hilos esperen, ya que Python actualmente no utiliza múltiples núcleos para la gestión de hilos. [10](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#id607) En cambio, como aprenderá más en [el Capítulo 5](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch05.html#ch05) , para este tipo de operaciones de cálculo costosas, deberá utilizar multiprocesamiento o un grupo de procesos.

## Falta de soporte para solicitudes de inferencia de procesamiento por micro-lotes
Los marcos de aprendizaje profundo ofrecen soporte para la vectorización, lo que permite agrupar las inferencias, calcularlas de forma eficiente y paralelizarlas. Desafortunadamente, en FastAPI no es posible agrupar las solicitudes de predicción, lo que provoca que cada operación de inferencia de modelo, que requiere mucha computación, bloquee otras solicitudes.

Al escalar los servicios, una solución consiste en servir los modelos complejos por separado y utilizar FastAPI para autenticar y gestionar los datos entrantes y salientes.

## No es posible dividir eficientemente las cargas de trabajo de IA entre la CPU y la GPU.
Si bien la CPU se encarga principalmente de las operaciones de transformación y validación de solicitudes, la GPU puede ejecutar y paralelizar la inferencia de modelos que requiere mucha computación. En algunos marcos de trabajo web especializados en aprendizaje automático (como BentoML), también es posible dividir de manera eficiente las cargas de trabajo de IA entre la CPU y la GPU.

---

**Nota**
Al dividir las cargas de trabajo de IA entre la CPU y la GPU, la preparación de datos y las operaciones de posprocesamiento se ejecutan en la CPU, mientras que la inferencia de aprendizaje profundo, más rápida, se realiza en la GPU.

---

Lamentablemente, FastAPI no puede distribuir eficientemente la carga de trabajo de inferencia de IA entre estos dispositivos. Esto significa que la CPU puede bloquearse e impedir el procesamiento de solicitudes incluso cuando se ejecutan procesos de inferencia en la GPU. Dado que esto representa un importante cuello de botella al trabajar con modelos complejos, será necesario servir dichos modelos fuera de FastAPI para cargas de trabajo concurrentes.

Analizaremos con más detalle las soluciones a esta limitación en [el Capítulo 5](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch05.html#ch05) .

## Conflictos de dependencia
Al implementar modelos de aprendizaje automático, se enfrentará a desafíos únicos en comparación con la implementación de aplicaciones web típicas. Esto se debe al profundo acoplamiento del entorno de ejecución del modelo con las bibliotecas nativas y el hardware. Cada entorno de implementación puede operar en hardware distinto y puede requerir el uso de versiones específicas de bibliotecas nativas y comandos de contenerización.

## Falta de soporte para cargas de trabajo de IA que requieren muchos recursos.
A pesar de sus increíbles capacidades, FastAPI se desarrolló antes del auge de la IA generativa. Por ello, sigue siendo un framework web de propósito general con soporte reciente para la implementación de IA y flujos de trabajo de aprendizaje automático. Sin embargo, para ciertos casos de uso, como la implementación de modelos complejos con miles de millones de parámetros que consumen muchos recursos, puede ser conveniente explorar otros frameworks como _BentoML_ .

---

**BentoML: Marco de trabajo inspirado en FastAPI para ejecutar modelos de IA que consumen muchos recursos.**
BentoML también se basa en Starlette y está diseñado teniendo en cuenta los patrones de FastAPI, pero específicamente para el aprendizaje automático. Su arquitectura permite escalar las solicitudes web de forma independiente de la inferencia del modelo, lo que proporciona flexibilidad en la computación de distribuciones.

Aborda los desafíos únicos del flujo de trabajo de aprendizaje automático mediante sus sistemas de ejecución, gestión de dependencias y control de versiones de modelos. Gracias a su sistema de gestión de dependencias, puede acelerar eficazmente las implementaciones al generar automáticamente Dockerfiles de forma declarativa, evitando así la necesidad de depurar comandos complejos de Docker para instalar y usar las bibliotecas CUDA para la inferencia en GPU.

Más adelante en el libro, presentaré una arquitectura FastAPI para flujos de trabajo de IA que requieren muchos recursos y que utiliza BentoML como servidor de IA subyacente. En esta arquitectura, las tareas de servicio de modelos se delegarán a BentoML, mientras que FastAPI gestionará la seguridad, el almacenamiento en caché y la lógica de negocio.

---

En los siguientes capítulos, aprenderá a crear su propio servicio GenAI con FastAPI.

Pero antes de seguir adelante, configuremos las herramientas necesarias de Python, como analizadores de código, formateadores y verificadores de tipos, en su entorno de desarrollo para facilitar el mantenimiento de su proyecto FastAPI mientras trabajamos juntos en él.

# Configuración de un entorno y herramientas Python gestionados
Para mantener un entorno de desarrollo estable y reproducible, es recomendable gestionar el entorno y las dependencias de Python.

Recomiendo:
- Using a _requirements.txt_ file with `pip` for simpler projects
- Using [uv](https://oreil.ly/Qxl7h) or [Conda](https://oreil.ly/Kfsc4) for `pip`-driven workflows
- Using [Poetry](https://oreil.ly/Rt04z) for more complex projects

Además de gestionar las dependencias, Python también cuenta con varios paquetes de terceros que permiten analizar y formatear el código antes de implementarlo en producción. [11](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#id618)

Se recomienda a los desarrolladores profesionales de Python que utilicen estas herramientas para detectar errores durante el desarrollo y antes de añadir cambios al repositorio de código. De hecho, recomiendo que realicen comprobaciones de código con estas herramientas con frecuencia para evitar que aparezcan errores en sus servicios.

Aquí tienes una lista no exhaustiva de paquetes de Python que recomiendo integrar en cualquier proyecto que inicies:

**Linters**
Estas herramientas analizan el código fuente para detectar errores de programación, errores de estilo y fragmentos de código no utilizados:
- _Autoflake_ : Elimina importaciones y variables no utilizadas del código para mejorar la legibilidad.
- _Flake8_ : Comprueba si cumple con las propuestas de mejora de Python (PEP) y los estilos de código.

**Formateadores**
Esto te permite ver mejor lo que has escrito:
- _isort_ : Ordena las importaciones en los módulos de Python.
- _Black_ : Formatea el código Python para facilitar su lectura.
- _Ruff_ : Linter y formateador basado en Rust que es extremadamente rápido y puede usarse como reemplazo de otras herramientas como `isort`, `black`, `flake8`, y posiblemente `bandit`[12](https://learning.oreilly.com/library/view/building-generative-ai/9781098160296/ch02.html#id621)

Loggers
Se utiliza en las partes del código que resultan complejas de depurar y monitorizar la aplicación:
- _Loguru_ : Reemplazando el módulo de registro integrado de Python

Escáneres
Si quieres tener la certeza de que no has introducido código o contraseñas inseguras por casualidad:
- _Bandit_ : Escaneo de vulnerabilidades de tu código Python con comprobación de problemas de seguridad comunes, como secretos codificados.
- _Safety_ : Escáner de vulnerabilidades de dependencias de Python para detectar paquetes con vulnerabilidades conocidas o paquetes maliciosos.

Type checkers
Para detectar aquellos errores que los analizadores de código normales no detectan. Además, es ideal si quieres tener la seguridad de que los cambios en tus esquemas no han dañado tu aplicación.
- _Mypy_ : Un potente verificador de tipos estático que puede ayudar a detectar muchos errores en tu código.
- _Pylance_ : Un verificador de tipos que viene incluido con la extensión de Python de Microsoft para VS Code.

Como parte de tu entorno de desarrollo, también es recomendable utilizar sistemas de control de versiones como Git para realizar un seguimiento de los cambios en el código fuente, gestionar las diferentes versiones de tu proyecto y administrar las contribuciones de código de otros desarrolladores.

---

**Consejo**
Al usar Git, también puedes agregar archivos _.gitignore_ para ayudarte a administrar los archivos y directorios que deseas excluir del seguimiento del control de versiones.

---

Los entornos de desarrollo integrados (IDE), como VS Code o JetBrains PyCharm, ofrecen complementos para ejecutar estas herramientas mientras escribes o guardas tu trabajo. Suelen requerir cierta configuración, pero una vez hecha, tendrás el formato automático y el análisis estático listos antes de empezar. En cualquier caso, recomiendo tener un script o hooks de pre-commit que analicen, revisen y den formato a tu código antes de confirmar los cambios o implementarlo en producción.

Estos son fundamentos de la programación en Python y la ingeniería de software. Se volverán cruciales cuando comience a trabajar con modelos de IA que pueden generar resultados probabilísticos, así como con servicios externos y bases de datos cuyos esquemas pueden cambiar en cualquier momento. Mantener una aplicación de IA que cambia de esquema y de parámetros constantemente sin las herramientas mencionadas puede convertirse rápidamente en un verdadero quebradero de cabeza.

# Resumen
En este capítulo, aprendiste sobre el framework FastAPI, incluyendo sus capacidades y desventajas en comparación con otros frameworks.

También aprendiste a configurar tu propio proyecto FastAPI desde cero, junto con un conjunto de herramientas que puedes usar para mejorar tu experiencia de desarrollo.

A continuación, se te presentaron varias estructuras de proyecto que puedes adoptar al crear tu propio servicio FastAPI. Como parte de esto, aprendiste más sobre el patrón de diseño de software en capas (o de cebolla) para ayudarte a gestionar la complejidad del proyecto.

Por último, hemos hablado de las herramientas que puedes usar para gestionar tus entornos Python y ayudarte a mantener el código fuente de FastAPI a medida que aumenta su complejidad.

Ahora ya deberías sentirte cómodo iniciando tus propios proyectos FastAPI y gestionando la complejidad del proyecto a medida que evoluciona con el tiempo.

En el próximo capítulo, aprenderá a implementar sus propias funciones GenAI en FastAPI para generar texto, imágenes, audio y video. Comprenderá el funcionamiento interno de cada modelo y el papel del sistema de ciclo de vida de FastAPI en la entrega de modelos, aprovechando las GPU de NVIDIA para las tareas de inferencia. Finalmente, se le presentará el sistema de tareas en segundo plano de FastAPI para descargar las operaciones de inferencia de larga duración.