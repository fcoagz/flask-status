[En español](https://github.com/fcoagz/statuspage/blob/main/README_ES.md)

# FlaskStatus

It is a Flask extension to view incidents caused by the server.

<img src="https://github.com/fcoagz/statuspage/blob/main/assets/dashboard.png?raw=true" style="border-radius: 10px;">

This is handled based on the requests that users make. Captures the server response and uses the conditional expression to quickly classify whether the request was successful or failed.

**Note**: Updates every minute

## Codes HTTP

Some of the HTTP states that the server takes into account are:

- `200 OK`: Indicates that the request has been completed successfully.
- `404 Not Found`: Indicates that the requested resource is not available on the server.

- `500 Internal Server Error`: Indicates that an internal server error has occurred while processing the client request.

- `502 Bad Gateway`: Indicates that there is a communication error between servers, generally when one server acts as an intermediary and cannot obtain a valid response.

- `503 Service Unavailable:` Indicates that the server is currently unavailable, possibly due to maintenance or overload.

- `504 Gateway Timeout`: Indicates that the server has not received a timely response from an upstream server, which may indicate connectivity problems.

## Install

```sh
pip install flask-server-status
```

## Use

- Import and configure FlaskStatus in your Flask application. You need a database to record the logs.

```py
from flask import Flask
from flask_server_status import FlaskStatus

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/status.db'
FlaskStatus(app)
```

You can configure which routes you want to be shown:

```py
FlaskStatus(app, routes=['/'])
```

- Define routes. The use of docstring. It will be used to define the route name. `# <ROUTE NAME>`

```py
@app.route('/')
def index():
    """
    # Index
    """ # This is the docstring
    return 'Welcome to API!', 200 # 200 is the status code
```

The default path is: `/status`

## API

FlaskStatus comes with a built-in API to configure the routes that are generated in the database.

```
app.config['API_ENABLED'] = True
app.config['API_SECRET'] = 'tSx0L5exSjiPqqXs'
```

### Endpoints

- `PUT /flask-status/configure`: Allows you to modify a route. `json={'rule': '/', 'name': 'Hello World!', 'doc': ''}`

- `DELETE /flask-status/configure`: Allows you to delete a route. `json={'rule': '/'}`

### Example

```py
import requests

r = requests.delete('http://127.0.0.1:5000/flask-status/configure', headers={
    'Authorization': 'Bearer tSx0L5exSjiPqqXs'
    }, json={
    'rule': '/'
})
```

## Forked from 

The page was built by Statsig's Open-Source Status Page.