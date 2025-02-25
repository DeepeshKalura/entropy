"""
quest is most important feature of the system which gives you
mission and experience
"""

from datetime import datetime, timedelta
import os
import random
from typing import List, Optional
import uuid

from sqlalchemy import select
from src.models import Quest, Task, User, Work
from src.utility import session, Status, QuestStatus, user_id, NotesPath


class QuestManager:
    def __init__(self):
        self.base_path = NotesPath.rough_path()
        self.required_completion_rate = 0.10

    def ensure_directory_exists(self, path) -> None:
        """Ensure the directory exists, create if it doesn't"""
        if not os.path.exists(path):
            os.makedirs(path)

    def get_active_quest(self):
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
        """Create specified number of tasks for a quest"""
        created_tasks = []
        works = session.execute(select(Work)).scalars().all()

        for _ in range(num_tasks):
            work = random.choice(works)
            task_name = self.generate_task_name(work.name)
            # Create task file

            task = Task(
                id=str(uuid.uuid4()),
                quest_id=quest.id,
                name=task_name,
                status=Status.pending,
                time_taken="0",
            )

            session.add(task)
            created_tasks.append(task)

        return created_tasks

    def quest_template(self, list_work_name: List[Task], expiry_date) -> str:
        tags = ""

        for work_name in list_work_name:
            tags += f"[[{work_name.name}]]"
            tags += ", "

        """Create the markdown content for the task"""
        task_list = ""
        for task in list_work_name:
            task_list += f"- {task.name}\n"
        template = f"""Tags: {tags}
    **time**: {{date}} {{time}}
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
        template = self.quest_template(list_of_work, expiry_date)
        with open(quest_path, "w") as f:
            f.write(template)

    def check_quest_progress(self) -> Optional[Quest]:
        """Check progress of the active quest"""
        active_quest = self.get_active_quest()
        if not active_quest:
            print("No active quest found")
            return None

    def generate(self) -> Optional[Quest]:
        """Main entry point for managing quests and tasks"""
        # Check if there's an active quest
        current_time = datetime.now()
        active_quest = self.get_active_quest()

        if active_quest:
            if current_time <= active_quest.expiry_date:
                return active_quest
            else:
                total_tasks = (
                    session.query(Task).filter(Task.quest_id == active_quest.id).count()
                )
                completed_tasks = (
                    session.query(Task)
                    .filter(
                        Task.quest_id == active_quest.id,
                        Task.status == Status.completed,
                    )
                    .count()
                )

                completion_rate = (
                    completed_tasks / total_tasks if total_tasks > 0 else 0
                )

                users = session.query(User).filter(User.id == user_id).first()
                if completion_rate >= active_quest.required_completion_rate:
                    active_quest.status = QuestStatus.completed

                    users.xp += 100
                else:
                    # Quest failed due to insufficient completion
                    active_quest.status = QuestStatus.failed
                    users.xp -= 150

                session.commit()

        days = random.randint(3, 8)
        return self.create_quest(days_to_complete=days)


questManager = QuestManager()
