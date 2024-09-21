import os
from sqlalchemy import create_engine
from .models import Base

def get_engine(uri: str) -> create_engine:
    """
    Create engine for database connection
    """
    os.makedirs('tmp', exist_ok=True)
    return create_engine(uri)

def create_tables(engine) -> None:
    """
    Create tables in database
    """
    Base.metadata.create_all(engine)