from sqlalchemy import create_engine 
from sqlalchemy.orm import  DeclarativeBase


class Base(DeclarativeBase):
    pass 

sqlalchemy_engine = create_engine("sqlite://", echo=True)

