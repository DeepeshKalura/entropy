"""
quest is most important feature of the system which gives you
mission and experience
"""

import os
import random
import uuid
from datetime import datetime, timedelta
from typing import List, Optional

from src.models import Distractions, Quest, Task, TaskEvents, User, Work, Assignment
from src.utility import (
    EventType,
    NotesPath,
    QuestStatus,
    Status,
    TaskCategories,
    session,
    user_id,
)


class QuestManager:
    def __init__(self):
        self.base_path = NotesPath.rough_path()
        self.required_completion_rate = 0.10

    def ensure_directory_exists(self, path) -> None:
        """Ensure the directory exists, create if it doesn't"""
        if not os.path.exists(path):
            os.makedirs(path)

    def get_active_quest(self) -> Optional[Quest]:
        """Get the currently active quest or None if no active quest exists"""
        return session.query(Quest).filter(Quest.status == QuestStatus.active).first()

    def create_quest(self, days_to_complete=7, num_tasks=None) -> Optional[Quest]:
        """Create a new quest only if no active quest exists"""
        active_quest = self.get_active_quest()
        if active_quest:
            print(f"Active quest already exists: {active_quest.name}")
            return active_quest

        # Generate between 1-5 tasks if num_tasks not specified
        num_tasks = num_tasks or random.randint(3, 5)
        name = f"Quest_{datetime.now().strftime('%Y%m%d_%H%M')}"
        quest_path = os.path.join(self.base_path, f"{name}.md")
        expiry_date: datetime = datetime.now().replace(microsecond=0) + timedelta(
            days=days_to_complete
        )
        quest = Quest(
            name=f"Quest_{datetime.now().strftime('%Y%m%d_%H%M')}",
            status=QuestStatus.active,
            path=quest_path,
            required_completion_rate=0.1,
            expiry_date=expiry_date,
        )

        session.add(quest)

        # Create tasks for the quest
        created_tasks = self.create_tasks_for_quest(quest, num_tasks)

        try:
            session.commit()

            # create the quest material
            self.create_quest_file(
                list_of_work=created_tasks,
                quest_path=quest_path,
                expiry_date=expiry_date,
            )
            print(f"Created new quest '{quest.name}' with {len(created_tasks)} tasks")
            print(
                f"Complete {quest.required_completion_rate * 100}% of tasks by {quest.expiry_date.strftime('%Y-%m-%d %H:%M')}"
            )
            return quest
        except Exception as e:
            session.rollback()
            print(f"Error creating quest: {e}")
            return None

    def create_tasks_for_quest(self, quest, num_tasks) -> List[Task]:
        """Create specified number of tasks for a quest, including one assignment with earliest deadline if available"""
        created_tasks = []
        works = session.query(Work).all()

        # First, try to get the assignment with earliest deadline
        earliest_assignment = (
            session.query(Assignment)
            .filter(Assignment.status != "completed")  # Only non-completed assignments
            .order_by(Assignment.deadline)  # Sort by deadline ascending
            .first()
        )
        
        # If we found an assignment, create a task for it and reduce num_tasks by 1
        if earliest_assignment and num_tasks > 0:
            # Get the work for this assignment
            assignment_work = session.query(Work).filter(Work.id == earliest_assignment.work_id).first()
            
            if assignment_work:
                task_name = f"ASSIGNMENT: {earliest_assignment.name} (due: {earliest_assignment.deadline.strftime('%Y-%m-%d')})"
                
                task = Task(
                    id=str(uuid.uuid4()),
                    quest_id=quest.id,
                    name=task_name,
                    status=Status.pending,
                    time_taken="0",
                    work_id=assignment_work.id  # Link to the assignment's work
                )
                
                session.add(task)
                created_tasks.append(task)
                num_tasks -= 1  
                
                # Update the task's description in database to reference this assignment
                task.description = f"Complete assignment: {earliest_assignment.description}\nID: {earliest_assignment.id}"
                
                print(f"Added assignment '{earliest_assignment.name}' to quest as a task")
        
        # Create the remaining random tasks as before
        weight_work: List[str] = []
        for work in works:
            weight_work += [str(work.name)] * work.priority

        for _ in range(num_tasks):
            work_name = random.choice(weight_work)
            task_name = self.generate_task_name(work_name)
            
            # Find the corresponding work object
            work = next((w for w in works if str(w.name) == work_name), None)
            
            task = Task(
                id=str(uuid.uuid4()),
                quest_id=quest.id,
                name=task_name,
                status=Status.pending,
                time_taken="0",
                work_id=work.id if work else None
            )

            session.add(task)
            created_tasks.append(task)

        return created_tasks

    def quest_template(self, list_work_name: List[Task], expiry_date) -> str:
        tags = ""

        for work_name in list_work_name:
            tags += f"[[{work_name.work.name}]]"
            tags += ", "

        """Create the markdown content for the task"""
        task_list = ""
        for task in list_work_name:
            task_list += f"- {task.name}\n"
        template = f"""Tags: {tags}
        **time**: {datetime.now()}
        **Status**: #{QuestStatus.active}
        **Expiry Date**: {expiry_date.strftime("%Y-%m-%d %H:%M")}

        ### Choose any one task and complete it to earn 50XP!

        ### Task List:
        {task_list}
        """
        return template

    def generate_task_name(self, work_name) -> str:
        """Generate a unique task name"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        return f"task_{work_name.lower()}_{timestamp}"

    def create_quest_file(
        self, list_of_work: List[Task], quest_path: str, expiry_date: datetime
    ):
        """Create the markdown file for the task"""
        self.ensure_directory_exists(os.path.dirname(quest_path))
        template = self.quest_template(
            list_work_name=list_of_work, expiry_date=expiry_date
        )
        with open(quest_path, "w") as f:
            f.write(template)

    def check_quest_progress(self) -> Optional[Quest]:
        """Check progress of the active quest"""
        active_quest = self.get_active_quest()
        if not active_quest:
            print("No active quest found")
            return None

    def closing_counter(self, quest: Quest):
        try:
            # Get all tasks for the quest
            tasks = session.query(Task).filter(Task.quest_id == quest.id).all()
            total_tasks = len(tasks)

            # Update status of incomplete tasks
            for task in tasks:
                if task.status in [Status.started, Status.pending]:
                    task.status = Status.failure

            completed_tasks = (
                session.query(Task)
                .filter(
                    Task.quest_id == quest.id,
                    Task.status == Status.completed,
                )
                .count()
            )

            completion_rate = completed_tasks / total_tasks if total_tasks > 0 else 0

            users = session.query(User).filter(User.id == user_id).first()
            if completion_rate >= quest.required_completion_rate:
                quest.status = QuestStatus.completed
                users.xp += 100
            else:
                quest.status = QuestStatus.failed
                users.xp -= 150

            session.commit()

        except Exception as e:
            session.rollback()
            print(f"Error in closing counter: {str(e)}")

    def generate(self) -> Optional[Quest]:
        """Main entry point for managing quests and tasks"""
        # Check if there's an active quest
        current_time = datetime.now()
        active_quest = self.get_active_quest()

        if active_quest:
            if current_time <= active_quest.expiry_date:
                return active_quest
            else:
                print(
                    "your quest time is up, we are sending your request to closing counter"
                )
                self.closing_counter(active_quest)

        days = random.randint(3, 8)
        return self.create_quest(days_to_complete=days)

    def started_task_of_quest(self, quest: Quest) -> Optional[Task]:
        task = (
            session.query(Task)
            .filter(Task.quest_id == quest.id)
            .filter(Task.status == Status.started)
            .first()
        )

        return task

    def task_event_exist(self) -> Optional[TaskEvents]:
        try:
            return (
                session.query(TaskEvents).order_by(TaskEvents.start_time.desc()).first()
            )
        except Exception as e:
            print(f"Error getting latest task event: {e}")
            return None

    def add_new_event(
        self,
        task: Task,
        event_type: str,
        event_category: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Optional[TaskEvents]:
        """
        Add a new event entry for a task, tracking the work or distraction activity.
        """
        try:
            # Generate unique ID
            event_id: str = str(uuid.uuid4())

            start_time = datetime.now()

            # Validate the event type
            if event_type not in [EventType.work, EventType.distraction]:
                raise ValueError(
                    f"Invalid event type: {event_type}. Must be one of {EventType.__dict__}"
                )

            # Validate event category based on event type
            if event_type == EventType.work:
                # For work events, category should be from TaskCategories
                if event_category not in [
                    TaskCategories.visual,
                    TaskCategories.study,
                    TaskCategories.diplomatic,
                    TaskCategories.implementation,
                ]:
                    raise ValueError(
                        f"Invalid task category for work: {event_category}"
                    )

            elif event_type == EventType.distraction:
                # For distraction events, validate against the distractions table
                distraction = (
                    session.query(Distractions)
                    .filter(Distractions.name == event_category)
                    .first()
                )
                if not distraction:
                    distraction = event_category

            if notes:
                quest_path = task.quest.path
                if os.path.exists(quest_path):
                    with open(quest_path, "a+") as f:
                        f.write(notes)
                        f.write("\n")

            new_event = TaskEvents(
                id=event_id,
                task_id=task.id,
                user_id=user_id,
                start_time=start_time,
                end_time=None,
                event_type=event_type,
                event_category=event_category,
                notes=notes,
            )

            # Add to database
            session.add(new_event)
            session.commit()

            return new_event

        except Exception as e:
            session.rollback()
            print(f"Error adding new event: {str(e)}")
            return None

    def end_current_event(
        self, event: TaskEvents, path: str, end_notes: Optional[str] = None
    ) -> Optional[TaskEvents]:
        """
        End an ongoing event by setting its end_time to the current time

        Args:
            event_id: ID of the event to end
            end_notes: Optional notes to append about how the event ended

        Returns:
            The updated TaskEvents object or None if update failed
        """
        try:
            event.end_time = datetime.now()

            # If there are end notes, append them to the existing notes file
            if end_notes is not None:
                with open(path, "a") as f:
                    f.write(end_notes)
                    f.write("\n")

                if event.notes is None:
                    event.notes = ""
                event.notes += f"\n{end_notes}"
            session.commit()
            return event

        except Exception as e:
            session.rollback()
            print(f"Error ending event: {str(e)}")
            return None


questManager = QuestManager()
