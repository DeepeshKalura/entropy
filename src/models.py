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
    priority = Column(Integer, nullable=False, default=5)
    repo_url = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    
    # Add relationship to Assignment
    assignments = relationship("Assignment", back_populates="work")
    tasks = relationship("Task", back_populates="work")


class Task(Base):
    """Task is steps to complete the works. In this humans have to put time and effort"""
    __tablename__ = "tasks"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    time_taken = Column(Integer, nullable=False)
    description = Column(Unicode(200), nullable=True)
    quest_id = Column(String, ForeignKey("quests.id"), nullable=True)
    work_id = Column(String, ForeignKey("work.id"), nullable=False)
    assignment_id = Column(String, ForeignKey("assignments.id"), nullable=True)
    quest = relationship("Quest", back_populates="tasks")
    work = relationship("Work", back_populates="tasks")
    assignment = relationship("Assignment", back_populates="tasks")
    events = relationship("TaskEvents", back_populates="task")

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


class Distractions(Base):
    """Distractions represent things that take away focus from work/tasks.
    These could be social media, games, or other non-productive activities
    that need to be managed to maintain productivity."""

    __tablename__ = "distractions"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Unicode(200))
    path = Column(String, nullable=False)
    level_of_distraction = Column(String, nullable=False)
    create_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class TaskEvents(Base):
    """
    Represents events related to tasks, tracking when work happens, distractions occur,
    and what category of activity is taking place.
    """

    __tablename__ = "task_events"

    id = Column(String, primary_key=True)
    task_id = Column(String, ForeignKey("tasks.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    event_type = Column(String, nullable=False)  # work | distraction | hobby | etc
    event_category = Column(
        String, nullable=True
    )  # study | coding | knowledge_gain | diplomatic | management
    notes = Column(Unicode(500), nullable=True)
    create_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    # Relationships
    task = relationship("Task", back_populates="events")
    user = relationship("User")


class Assignment(Base):
    """
    Represent the short assignments given by the system
    """
    __tablename__ = 'assignments'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Unicode(200), nullable=True)
    status = Column(String, nullable=False)
    deadline = Column(DateTime, nullable=False)
    priority = Column(Integer, nullable=False, server_default=text("3"))
    work_id = Column(String, ForeignKey('work.id'), nullable=False)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"),
                        onupdate=text("CURRENT_TIMESTAMP"), nullable=False)
    # Relationship to the Work model and Task model
    work = relationship("Work", back_populates="assignments")
    tasks = relationship("Task", back_populates="assignment")