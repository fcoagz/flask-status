from flask import Blueprint

bye = Blueprint('bye', __name__)

@bye.route('/')
def bye_world():
    """
    # Bye, World!
    """
    return 'Bye, World!', 200