from flask import Blueprint

hello = Blueprint('hello', __name__)

@hello.route('/')
def hello_world():
    """
    # Hello, World!
    """
    return 'Hello, World!', 200