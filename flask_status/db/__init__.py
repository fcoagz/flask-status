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