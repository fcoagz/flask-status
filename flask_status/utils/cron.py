import re
from typing import List, Optional
from flask import Flask
from werkzeug.utils import import_string
from sqlalchemy.orm import Session

from .cache import cache
from ..handler_logs import log_file
from ..utils.logs import parse_log_entry
from ..db import create_route, create_log, get_routes as _get_routes_, get_logs as _get_logs_

def get_logs() -> None:
    """
    Get all logs
    """
    founds_logs = cache.get('logs', [])

    log = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', log_file.getvalue().split('\n')[-2])
    if re.match(r'127\.0\.0\.1 - - \[\d{2}/\w{3}/\d{4} \d{2}:\d{2}:\d{2}\] "GET /.* HTTP/1\.1" \d{3} -', log.strip()):
        if log not in founds_logs:
            founds_logs.append(log)
            cache['logs'] = founds_logs

def get_routes(app: Flask, session: Session) -> List[dict]:
    """
    Get all routes in the app

    :param app: Flask app
    :param session: sqlalchemy session
    :param routes: list of routes
    """
    monitore_routes =  []
    for rule in app.url_map.iter_rules():
        if rule.endpoint not in ['static', 'flask_logs']:
            if hasattr(app.view_functions[rule.endpoint], 'import_name'):
                import_name = app.view_functions[rule.endpoint].import_name
                obj = import_string(import_name)
                docstring = str(obj.__doc__) or '# Unknown'
                name = re.findall(r'# (.*)', docstring)[0]
                doc = re.sub(r'# (.*)', '', docstring).strip()

                monitore_routes.append({
                    'url': rule.rule,
                    'name': name,
                    'doc': doc
                })
            else:
                docstring = str(app.view_functions[rule.endpoint].__doc__) or ''
                name = re.findall(r'# (.*)', docstring)[0]
                doc = re.sub(r'# (.*)', '', docstring).strip()

                monitore_routes.append({
                    'url': rule.rule,
                    'name': name,
                    'doc': doc
                })

    get_db_routes = _get_routes_(session)
    urls_found = [] if not get_db_routes else [route['url'] for route in get_db_routes]
    for route in monitore_routes:
        if route['url'] not in urls_found:
            create_route(session, route)
    return _get_routes_(session)

def background_log(
        app: Flask, 
        session: Session, 
        routes: Optional[List[str]] = None):
    """
    Background log

    :param app: Flask app
    :param session: sqlalchemy session
    :param routes: list of routes
    """
    founds_logs = cache.get('logs', [])
    g_routes = get_routes(app, session)
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
                    create_log(session, {
                        'id_route': route['id'],
                        'status_code': status,
                        'message': message,
                        'time': date
                    })
    
    founds_logs.clear()
    cache['routes'] = _get_routes_(session, routes)