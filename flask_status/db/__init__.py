from typing import List, Optional
from sqlalchemy.orm import Session
from .models import Logs, Routes
from .schemas import RoutesSchema, LogsSchema

def get_routes(session: Session, routes: Optional[List[str]] = None) -> List[RoutesSchema]:
    """
    Get all routes

    :param session: sqlalchemy session
    """
    if routes is None:
        routes = session.query(Routes).all()
    else:
        routes = session.query(Routes).filter(Routes.url.in_(routes)).all()
    return RoutesSchema().dump(routes, many=True)

def get_route(session: Session, route: str) -> Routes:
    """
    Get a route

    :param session: sqlalchemy session
    :param route: route
    """
    route = session.query(Routes).filter(Routes.url == route).first()
    return route

def get_logs(session: Session) -> List[Logs]:
    """
    Get all logs

    :param session: sqlalchemy session
    """
    logs = session.query(Logs).all()
    return LogsSchema().dump(logs, many=True)

def create_route(session: Session, route: dict) -> Routes:
    """
    Create a new route

    :param session: sqlalchemy session
    :param route: route schema
    """
    new_route = Routes(**route)
    session.add(new_route)
    session.commit()
    return new_route

def create_log(session: Session, log: dict) -> Logs:
    """
    Create a new log

    :param session: sqlalchemy session
    :param log: log schema
    """
    new_log = Logs(**log)
    session.add(new_log)
    session.commit()
    return new_log

def modify_route(session: Session, route: str, data: dict) -> Routes:
    """
    Modify a route

    :param session: sqlalchemy session
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

def delete_route(session: Session, route: str) -> None:
    """
    Delete a route

    :param session: sqlalchemy session
    :param route: route
    """
    route = session.query(Routes).filter(Routes.url == route).first()
    if route:
        session.query(Logs).filter(Logs.id_route == route.id).delete()
        session.delete(route)
        session.commit()
    else:
        raise ValueError(f'Route {route} not found')