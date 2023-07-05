from sqlalchemy.ext.declarative import declarative_base
from db import engine
from sqlalchemy import Column, Integer, String, DateTime, func


Base = declarative_base(bind=engine)

class Advert(Base):

    __tablename__ = 'adverts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False)
    content = Column(String, nullable=False)
    creation_time = Column(DateTime, server_default=func.now())
  
    
Base.metadata.create_all()  