import re
from typing import List, Optional
from flask import Flask

from .cache import cache
from ..handler_logs import log_file
from ..utils.logs import parse_log_entry
from ..db import (
    create_routes as _create_routes_,
    create_log, 
    get_routes as _get_routes_
)

PATTERN_GET_LOG = r'127\.0\.0\.1 - - \[\d{2}/\w{3}/\d{4} \d{2}:\d{2}:\d{2}\] "GET /.* HTTP/1\.1" \d{3} -'

def get_logs() -> None:
    """
    Get all logs
    """
    founds_logs = cache.get('logs', [])

    log = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', log_file.getvalue().split('\n')[-2]) # remove color codes
    if re.match(PATTERN_GET_LOG, log.strip()):
        if log not in founds_logs:
            founds_logs.append(log)
            cache['logs'] = founds_logs

def get_routes(app: Flask) -> List[dict]:
    """
    Get all routes in the app

    :param app: Flask app
    :param routes: list of routes
    """
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint not in ['static', 'flask_logs', 'configure_flask_status']:
            docstring = str(app.view_functions[rule.endpoint].__doc__)
            name = rule.endpoint if not re.findall(r'# (.*)', docstring) else re.findall(r'# (.*)', docstring)[0]
            doc  = re.sub(r'# (.*)', '', docstring).strip()

            routes.append({
                'url': rule.rule,
                'name': name,
                'doc': doc
            })

    _create_routes_(routes)
    return _get_routes_()

def background_log(
        app: Flask, 
        routes: Optional[List[str]] = None):
    """
    Background log

    :param app: Flask app
    :param routes: list of routes
    """
    founds_logs = cache.get('logs', [])
    g_routes = get_routes(app)
    for log in founds_logs:
        date, url, status = parse_log_entry(log)
        for route in g_routes:
            if route['url'] == url and date.strftime('%Y-%m-%d %H:%M:%S') not in [log['time'] for log in route['logs']]:
                if 200 <= status < 400:
                    message = 'success'
                elif status == 404 or status in [500, 502, 503, 504]:
                    message = 'failure'
                else:
                    message = None
                
                if message:
                    create_log({
                        'id_route': route['id'],
                        'status_code': status,
                        'message': message,
                        'time': date
                    })
    
    founds_logs.clear()
    cache['routes'] = _get_routes_(routes)