import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv

load_dotenv(override=True)


class Base(DeclarativeBase):
    pass


sqlalchemy_engine = create_engine(os.getenv("SQL_LITE_URL"), echo=False)


Session = sessionmaker(bind=sqlalchemy_engine)
