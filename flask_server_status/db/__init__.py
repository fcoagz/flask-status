from typing import List, Optional
from sqlalchemy.orm import sessionmaker
from .engine import engine
from .models import Logs, Routes
from .schemas import RoutesSchema, LogsSchema

session = sessionmaker(bind=engine)()

def get_routes(routes: Optional[List[str]] = None) -> List[RoutesSchema]:
    """
    Get all routes
    """
    if routes is None:
        routes = session.query(Routes).all()
    else:
        routes = session.query(Routes).filter(Routes.url.in_(routes)).all()
    return RoutesSchema().dump(routes, many=True)

def get_route(route: str) -> Routes:
    """
    Get a route

    :param route: route
    """
    route = session.query(Routes).filter(Routes.url == route).first()
    return route

def get_logs() -> List[Logs]:
    """
    Get all logs
    """
    logs = session.query(Logs).all()
    return LogsSchema().dump(logs, many=True)

def create_routes(routes: List[dict]) -> List[Routes]:
    """
    Create new routes

    :param routes: list of route schema
    """
    new_routes = [
        Routes(**route) for route in routes 
        if not session.query(Routes).filter(Routes.url == route['url']).first()
        ]
    session.add_all(new_routes)
    session.commit()
    return new_routes

def create_log(log: dict) -> Logs:
    """
    Create a new log

    :param log: log schema
    """
    new_log = Logs(**log)
    session.add(new_log)
    session.commit()
    return new_log

def modify_route(route: str, data: dict) -> Routes:
    """
    Modify a route

    :param route: route
    :param data: new route schema
    """
    route = session.query(Routes).filter(Routes.url == route).first()
    if route:
        for key, value in data.items():
            setattr(route, key, value)
        session.commit()
        return RoutesSchema().dump(route)
    else:
        raise ValueError(f'Route {route} not found')

def delete_route(route: str) -> None:
    """
    Delete a route

    :param route: route
    """
    route = session.query(Routes).filter(Routes.url == route).first()
    if route:
        session.query(Logs).filter(Logs.id_route == route.id).delete()
        session.delete(route)
        session.commit()
    else:
        raise ValueError(f'Route {route} not found')