from flask import Flask
from flask_status import FlaskStatus
from routes.hello import hello
from routes.bye import bye

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
FlaskStatus(app)

@app.route('/')
def index():
    """
    # Index
    """ # This is the docstring
    return 'Welcome to API!', 200 # 200 is the status code

app.register_blueprint(hello, url_prefix='/hello')
app.register_blueprint(bye, url_prefix='/bye')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)