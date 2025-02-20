"""
Models are representations of database tables which we mutate and query.
Currently we have hobby, wanna_be and work models and Task.

This data stored in database and correlate to each other and provide purpose for this life.

"""

from sqlalchemy import Column, DateTime, String, Unicode, text
from src.engine import Base


class Hobby(Base):
    """Represent of hobbies which is long term and fun in me."""

    __tablename__ = "hobbies"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Unicode(200))
    create_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class WannaBe(Base):
    """Represent the wanna be nature of me."""

    __tablename__ = "wanna_be"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Unicode(200))
    create_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class Work(Base):
    """Work is the thing which you have to do for certain period of time for certain purpose"""

    __tablename__ = "work"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Unicode(200))
    create_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class Task(Base):
    """Task is steps to complete the works. In this humans have to put time and effort"""

    __tablename__ = "tasks"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    path = Column(String, nullable=False)
    status = Column(String, nullable=False)
    time_taken = Column(String)
    create_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
