from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .engine import engine

Base = declarative_base()

class Routes(Base):
    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    url  = Column(String(50), nullable=False)
    doc  = Column(String(50), nullable=True)
    logs = relationship('Logs', backref='routes')

class Logs(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    id_route    = Column(Integer, ForeignKey('routes.id'))
    status_code = Column(Integer, nullable=False)
    message     = Column(String(50), nullable=False)
    time        = Column(DateTime, nullable=False)

Base.metadata.create_all(engine)