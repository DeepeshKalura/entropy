from sqlalchemy import Column, DateTime, String, Unicode, text
from src.engine import Base


class Hobby(Base):
    __tablename__ = 'hobbies'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Unicode(200))
    create_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    

class WannaBe(Base):
    __tablename__ = 'wanna_be'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Unicode(200))
    create_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class Work(Base):
    __tablename__ = 'work'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Unicode(200))
    create_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    
    