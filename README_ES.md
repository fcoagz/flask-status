[In English](https://github.com/fcoagz/statuspage/blob/main/README.md)

# FlaskStatus

Es una extensión de Flask para visualizar incidentes provocados por el servidor.

<img src="https://github.com/fcoagz/statuspage/blob/main/assets/dashboard.png?raw=true" style="border-radius: 10px;">

Esto se maneja en función de las solicitudes que realizan los usuarios. Captura la respuesta del servidor y utiliza la expresión condicional para clasificar rápidamente si la solicitud fue exitosa o si ha fallado.

**Nota**: Actualizaciones cada minuto

## Codes HTTP

Algunos de los estados de HTTP que el servidor toma en cuenta son:

- `200 OK`: Indica que la solicitud ha sido completada con éxito.
- `404 Not Found`: Indica que el recurso solicitado no se encuentra disponible en el servidor.

- `500 Internal Server Error`: Indica que ha ocurrido un error interno en el servidor al procesar la solicitud del cliente.

- `502 Bad Gateway`: Indica que existe un error de comunicación entre servidores, generalmente cuando un servidor actúa como intermediario y no puede obtener una respuesta válida.

- `503 Service Unavailable:` Indica que el servidor no está disponible en ese momento, posiblemente debido a mantenimiento o sobrecarga.

- `504 Gateway Timeout`: Indica que el servidor no ha recibido una respuesta a tiempo de un servidor upstream, lo que puede indicar problemas de conectividad.

## Uso

- Importar y configurar FlaskStatus en tu aplicación Flask. Necesita una base de datos para registrar los registros.

```py
from flask import Flask
from flask_status import FlaskStatus

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/status.db'
FlaskStatus(app)
```

Puedes configurar qué rutas quieres que se muestren:

```py
FlaskStatus(app, routes=['/'])
```

- Definir rutas. El uso de docstring. Se utilizará para definir el nombre de la ruta. `# <NOMBRE DE LA RUTA>`

```py
@app.route('/')
def index():
    """
    # Index
    """ # This is the docstring
    return 'Welcome to API!', 200 # 200 is the status code
```

La ruta por defecto es: `/status`

## API

FlaskStatus viene con una API incorporada para configurar las rutas que se generan en la base de datos.

```
app.config['API_ENABLED'] = True
app.config['API_SECRET'] = 'tSx0L5exSjiPqqXs'
```

### Endpoints

- `PUT /flask-status/configure`: Le permite modificar una ruta. `json={'rule': '/', 'name': 'Hello World!', 'doc': ''}`

- `DELETE /flask-status/configure`: Le permite eliminar una ruta. `json={'rule': '/'}`

### Ejemplo

```py
import requests

r = requests.delete('http://127.0.0.1:5000/flask-status/configure', headers={
    'Authorization': 'Bearer tSx0L5exSjiPqqXs'
    }, json={
    'rule': '/'
})
```

## Forked from 

La página fue construida por Statsig's Open-Source Status Page.