from flask import Flask
from flask_server_status import FlaskStatus

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
FlaskStatus(app)

@app.route('/')
def hello_world():
    """
    # Hello, World!
    """ # This is the docstring
    return 'Hello, World!', 200 # 200 is the status code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)