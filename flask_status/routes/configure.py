from flask import Blueprint, request
from sqlalchemy.orm import sessionmaker
from ..db import modify_route, delete_route
from ..db.engine import get_engine
from ..utils.cache import cache

route = Blueprint('flask_status_configure', __name__)
engine = get_engine(str(cache.get('SQLALCHEMY_DATABASE_URI')))
session = sessionmaker(bind=engine)()

@route.route('/configure', methods=['DELETE', 'PUT'])
def configure_flask_status():
    """
    # Configure API
    """
    try:
        if not cache.get('API_SECRET'):
            return {'error': 'API is not enabled'}, 400
        
        if request.headers.get('Authorization') != cache.get('API_SECRET'):
            return {'error': 'Unauthorized'}, 401
        
        data = request.get_json()
        if request.method == 'DELETE': # Delete route
            rule = data.get('rule')
            if rule:
                delete_route(session, rule)
                return {'message': 'Route deleted'}, 200
            else:
                return {'error': 'No rule provided'}, 400
            
        elif request.method == 'PUT': # modify route
            rule = data.pop('rule', None)
            if rule:
                route = modify_route(session, rule, data)
                return {'message': 'Route modified', 'route': route}, 200
            else:
                return {'error': 'No rule provided'}, 400
    except Exception as e:
        return {'error': str(e)}, 400