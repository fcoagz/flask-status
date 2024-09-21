import logging
from io import StringIO

log_file = StringIO()

flask_logger = logging.getLogger('werkzeug')
flask_logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler(log_file)
stream_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

flask_logger.addHandler(stream_handler)
flask_logger.addHandler(console_handler)
