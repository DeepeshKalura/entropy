"""
Models are representations of database tables which we mutate and query.
Currently we have hobby, wanna_be and work models and Task.

This data stored in database and correlate to each other and provide purpose for this life.

"""

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    String,
    Unicode,
    text,
    Integer,
)
from sqlalchemy.orm import relationship
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
    path = Column(String, nullable=False)
    repo_url = Column(String, nullable=False)
    create_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class Task(Base):
    """Task is steps to complete the works. In this humans have to put time and effort"""

    __tablename__ = "tasks"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    time_taken = Column(Integer, nullable=False)
    quest_id = Column(String, ForeignKey("quests.id"), nullable=True)
    quest = relationship("Quest", back_populates="tasks")


class User(Base):
    """User is the person who is using this application"""

    __tablename__ = "users"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    path = Column(String, nullable=False)
    description = Column(Unicode(200))
    xp = Column(Integer, nullable=False, server_default="1")
    photo = Column(String, nullable=True)
    height = Column(Float, nullable=False, server_default="172")
    weight = Column(Float, nullable=False, server_default="78")
    create_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class CharacterStatistics(Base):
    """CharacterStatistics is the statistics of the user which can be improved"""

    __tablename__ = "character_statistics"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    strength = Column(Integer, nullable=False, server_default="10")
    agility = Column(Integer, nullable=False, server_default="10")
    dexterity = Column(Integer, nullable=False, server_default="10")
    intellect = Column(Integer, nullable=False, server_default="10")
    speed = Column(Integer, nullable=False, server_default="10")
    charisma = Column(Integer, nullable=False, server_default="10")
    luck = Column(Integer, nullable=False, server_default="10")
    movement = Column(Integer, nullable=False, server_default="10")
    stamina = Column(Integer, nullable=False, server_default="10")
    perception = Column(Integer, nullable=False, server_default="10")
    path = Column(String, nullable=False)
    create_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class Skill(Base):
    """Skill is the ability to do certain task which can be received by the users"""

    __tablename__ = "skills"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    path = Column(String, nullable=False)
    description = Column(Unicode(200))
    create_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class UserSkill(Base):
    """UserSkill is the skill which user have and can be improved"""

    __tablename__ = "user_skills"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    skill_id = Column(String, nullable=False)
    current_level = Column(Integer, nullable=False, server_default="0")
    max_level = Column(Integer, nullable=False, server_default="100")
    unlocked_at = Column(DateTime)
    create_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class Title(Base):
    """Title is the name which can be received by the users"""

    __tablename__ = "titles"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    path = Column(String, nullable=False)
    description = Column(Unicode(200))
    create_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class UserTitle(Base):
    """UserTitle is the title which user earned and can be evolved"""

    __tablename__ = "user_titles"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    title_id = Column(String, nullable=False)
    create_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class Quest(Base):
    """Quest represents a collection of tasks that need to be completed"""

    __tablename__ = "quests"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    path = Column(String, nullable=False)
    required_completion_rate = Column(Float, default=0.1)  # 10% by default
    expiry_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    tasks = relationship("Task", back_populates="quest")
