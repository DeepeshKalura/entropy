import math
import os
from pathlib import Path
from rich.console import Console
from rich.text import Text
from src.engine import Session


class Status:
    pending = "PENDING"
    started = "STARTED"
    aborted = "ABORTED"
    in_progress = "IN_PROGRESS"
    completed = "COMPLETED"
    failure = "FAILURE"


class QuestStatus:
    active = "ACTIVE"
    completed = "COMPLETED"
    failed = "FAILED"


console = Console()


def calculate_level(xp: int) -> tuple[int, float]:
    """
    Calculate level and progress to next level based on XP.
    Returns (level, progress_percentage)
    """
    # Level calculation: Each level requires 20% more XP than the previous
    # Level 1: 0-100 XP
    # Level 2: 101-220 XP
    # Level 3: 221-364 XP, etc.

    if xp == 0:
        return 1, 0.0

    level = math.floor(1 + math.log(xp / 100 * 0.2 + 1) / math.log(1.2))

    # Calculate XP needed for current and next level
    xp_current_level = 100 * (1.2 ** (level - 1) - 1) / 0.2
    xp_next_level = 100 * (1.2**level - 1) / 0.2

    # Calculate progress percentage to next level
    progress = ((xp - xp_current_level) / (xp_next_level - xp_current_level)) * 100

    return level, min(progress, 100)


def create_progress_bar(progress: float, width: int = 20) -> Text:
    """Creates a styled progress bar."""
    filled = int(width * progress / 100)
    bar = Text("█" * filled + "░" * (width - filled), style="bright_blue")
    percentage = Text(f" {progress:.1f}%", style="bright_white")
    return Text.assemble(bar, percentage)


session = Session()


user_id: str = "9c3b7aed6c18407a9bea3d162c4eeaa0"


class NotesPath:
    @staticmethod
    def tag_path():
        return os.path.join(Path.home(), "Documents/adventure/3-tags")

    @staticmethod
    def rough_path():
        return os.path.join(Path.home(), "Documents/adventure/1-rough-work")

    @staticmethod
    def note_path():
        return os.path.join(Path.home(), "Documents/adventure/6-notes")
