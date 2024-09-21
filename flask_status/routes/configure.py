from flask import Blueprint, request
from ..db import modify_route, delete_route
from ..utils.cache import cache

route = Blueprint('flask_status_configure', __name__)

@route.route('/configure', methods=['DELETE', 'PUT'])
def configure_flask_status():
    """
    # Configure API
    """
    if not cache.get('API_SECRET'):
        return {'error': 'API is not enabled'}, 400
    
    if request.headers.get('Authorization') != cache.get('API_SECRET'):
        return {'error': 'Unauthorized'}, 401
    
    data = request.get_json()
    if request.method == 'DELETE': # Delete route
        rule = data.get('rule')
        if rule:
            delete_route(rule)
        else:
            return {'error': 'No rule provided'}, 400
        
    elif request.method == 'PUT': # modify route
        rule = data.pop('rule', None)
        if rule:
            modify_route(rule, data)
        else:
            return {'error': 'No rule provided'}, 400