"""
`act.py` is the control thing for entropy. It means
it is the entry points for the cli which is creating with
`click` package.

"""

from pathlib import Path
import time
from typing import Optional
import importlib.metadata
import click
from rich.table import Table
from rich.layout import Layout
from rich.text import Text
from rich.markdown import Markdown
from rich.box import SIMPLE
from src.animations_manager import AnimationManager
from src.models import (
    Task,
    User,
    CharacterStatistics,
    UserTitle,
)
from src.utility import (
    Status,
    calculate_level,
    create_progress_bar,
    console,
    session,
    user_id,
)
from src.quest_manager import questManager
from datetime import datetime


def display_welcome_banner(animator: AnimationManager, vers: Optional[str] = None):
    """Displays the welcome banner with optional version and animations."""
    console.clear()

    # Display main title
    animator.animate_ascii_art("PARTH", delay=0.03)

    # Show version if provided
    if vers:
        animator.animate_text(f"v{vers}", style="bold blue", delay=0.01)

    # Display welcome message
    welcome_text = (
        "Welcome to Parth - Where Life Becomes an Epic Game! 🎮\n"
        "Level up, conquer challenges, and transform your journey into an adventure."
    )
    animator.animate_text(welcome_text, style="bold green", delay=0.02)

    # Display feature highlights
    features = (
        "🏆 Complete quests and earn rewards\n"
        "⭐ Unlock achievements and titles\n"
        "📈 Track your progress and growth\n"
    )
    if not animator.skip_animations:
        time.sleep(0.5)
    animator.animate_text(features, style="bold yellow", delay=0.03)


def create_stats_table(
    level: int, xp: int, level_progress: float, height: float, weight: float
) -> Table:
    """Creates a formatted stats table."""
    table = Table(show_header=False, box=SIMPLE, show_edge=False, pad_edge=False)

    table.add_column("Stat", style="bright_white")
    table.add_column("Value", style="bright_cyan")

    table.add_row("Level", str(level))
    table.add_row("XP", f"{xp:,}")
    table.add_row("Progress", create_progress_bar(level_progress))
    table.add_row("Height", f"{height} cm")
    table.add_row("Weight", f"{weight} kg")

    return table


def display_profile(user: User):
    """Displays the user profile with a simplified layout."""
    console.clear()

    # Calculate level and progress
    level, level_progress = calculate_level(user.xp)

    # Display name in "larger" text using padding and bold
    name_display = f"\n\n{user.name}"
    console.print(name_display, style="bold cyan")
    console.print("\n[bold bright_blue]Level[/bold bright_blue]", level, end="")
    console.print(f"\nHeight: {user.height}cm | Weight: {user.weight}kg", style="dim")

    if user.path:
        path_file = Path(user.path)
        if path_file.exists():
            path_content = path_file.read_text()
            console.print(Markdown(path_content))
        else:
            console.print("[italic]Path file not found[/italic]")
    else:
        console.print("[italic]No path information available[/italic]")
    # Display level and XP
    console.print("[bright_white]Progress:[/bright_white] ", end="")

    console.print(create_progress_bar(level_progress))

    # Add a separator
    console.print("\n" + "─" * 50 + "\n", style="bright_black")


@click.group(invoke_without_command=True)
@click.option("--no-animations", is_flag=True, help="Disable all animations")
@click.option("--no-version", is_flag=True, help="Hide version information")
@click.pass_context
def main(ctx, no_animations: bool, no_version: bool) -> None:
    """
    🎮 PARTH - Transform Your Life Into An Epic Game! 🎮

    Level up your life by completing tasks, earning points, and tracking your progress.
    Make every day an exciting adventure with PARTH!
    """
    if ctx.invoked_subcommand is None:
        animator = AnimationManager(skip_animations=no_animations)
        ver = None if no_version else importlib.metadata.version("entropy")
        display_welcome_banner(animator, ver)


@main.command()
def profile():
    """Displays the user profile."""
    id: str = "9c3b7aed6c18407a9bea3d162c4eeaa0"
    user = session.query(User).filter_by(id=id).first()
    if user:
        display_profile(user)
    else:
        console.print("[red]User not found![/red]")


@main.command()
def version():
    """Displays the version of the application."""
    ver = importlib.metadata.version("entropy")
    console.print(f"🎮 PARTH v-{ver}", style="bold green")


@main.command()
def stats():
    """Shows stats about the master"""

    # Mock ID for demonstration
    id: str = "9c3b7aed6c18407a9bea3d162c4eeaa0"

    # Get data from database
    user = session.query(User).filter_by(id=id).first()
    character_stats = session.query(CharacterStatistics).filter_by(user_id=id).first()
    user_titles = session.query(UserTitle).filter_by(user_id=id).all()

    # Create layout
    layout = Layout()
    layout.split_column(
        Layout(name="header"), Layout(name="main"), Layout(name="footer")
    )
    layout["main"].split_row(Layout(name="stats"), Layout(name="skills"))

    # Header with master info
    header_text = Text()
    header_text.append(f"\n{user.name}", style="bold cyan")
    header_text.append(f" - Level {user.xp // 100}", style="yellow")
    header_text.append(f"\nPath: {user.path}", style="blue")
    header_text.append(
        f"\nHeight: {user.height}cm | Weight: {user.weight}kg", style="dim"
    )
    if user.description:
        header_text.append(f"\n{user.description}", style="italic")

    # Create stats table
    stats_table = Table(
        title=f"{user.name} Statistics", show_header=False, border_style="bright_blue"
    )
    stats_table.add_column("Stat", style="cyan")
    stats_table.add_column("Value", justify="right")

    stats_mapping = {
        "Strength": character_stats.strength,
        "Agility": character_stats.agility,
        "Dexterity": character_stats.dexterity,
        "Intellect": character_stats.intellect,
        "Speed": character_stats.speed,
        "Charisma": character_stats.charisma,
        "Luck": character_stats.luck,
        "Movement": character_stats.movement,
        "Stamina": character_stats.stamina,
        "Perception": character_stats.perception,
    }

    for stat, value in stats_mapping.items():
        bar = "█" * (value // 2) + "░" * (50 - value // 2)
        stats_table.add_row(stat, f"{value} {bar}")

    # Create titles panel
    titles_text = Text()
    for i, title in enumerate(user_titles):
        titles_text.append(
            f"[{title.title_id}]", style=("bold cyan" if i == 0 else "dim")
        )
        if i < len(user_titles) - 1:
            titles_text.append(" • ")

    # Combine all elements
    # console.print(Panel(header_text, title="Master Profile", border_style="cyan"))
    console.print(stats_table)
    # console.print(Panel(titles_text, title="Earned Titles", border_style="yellow"))

    console.print(
        f"\nMaster created: {user.create_at.strftime('%Y-%m-%d %H:%M:%S')}",
        style="dim",
        justify="right",
    )


@main.group()
def guild():
    """
    Control the task objects.

    This group command aggregates functionality related to managing tasks within
    the application.
    """


@guild.command(name="quest")
def create_random_task():
    """Pick a random open task"""

    quest = questManager.get_active_quest()
    if quest is None:
        quest = questManager.generate()

        if not quest:
            console.print("Damn! raise the github issue!", style="Bold Red")
        else:
            console.print(
                f"Your {quest.name} is this, use view to see more details",
                style="Bold Cyan",
            )

    else:
        console.print(
            f"This time is {quest.name}, use view to see more details",
            style="Bold Yellow",
        )


@main.command(name="view")
def view_quest():
    """View all tasks"""
    quest = questManager.get_active_quest()

    if quest is None:
        console.print(
            "You've never visited the guild before, so you cannot view any quest yet.",
            style="bold red",
        )
        console.print(
            "Visit the quest store to start viewing and getting quests.",
            style="bold green",
        )
    else:
        tasks = session.query(Task).filter(Task.quest_id == quest.id).all()

        console.print(quest.name, style="bold cyan")
        console.print(f"Status: {quest.status}", style="green", end="      ")
        time_left = quest.expiry_date - datetime.now()
        days_left = time_left.days
        hours_left = time_left.seconds // 3600
        console.print(
            f"Time remaining: {days_left} days, {hours_left} hours", style="red"
        )
        console.print(f"Path: {quest.path}")
        console.print()

        table = Table(show_header=True, header_style="bold cyan", title="Quest")
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Status")

        # Define a mapping of status to style
        status_color_map = {
            Status.pending: "yellow",
            Status.started: "bright_blue",
            Status.aborted: "bold red",
            Status.in_progress: "blue",
            Status.completed: "green",
            Status.failure: "red",
        }

        for current_task in tasks:
            # Apply color based on the status of the current task
            task_status_color = status_color_map.get(
                current_task.status, "white"
            )  # Default to white if no match
            status_with_color = (
                f"[{task_status_color}]{current_task.status}[/{task_status_color}]"
            )

            table.add_row(
                current_task.id,
                current_task.name,
                status_with_color,
            )

        console.print(table)


@guild.group(name="task")
def task_group():
    """Group of commands to manage tasks"""
    pass


@task_group.command(name="assign")
def assign_task_to_himself():
    """Assign a task to yourself and change its status to 'STARTED'"""
    quest = questManager.get_active_quest()

    if quest is None:
        console.print(
            "No active quest found. Please start a quest first.", style="bold red"
        )
        return

    tasks = (
        session.query(Task)
        .filter(Task.quest_id == quest.id)
        .filter(Task.status == Status.pending)
        .all()
    )

    if not tasks:
        console.print("No tasks available for assignment.", style="bold red")
        return

    console.print(f"Quest: {quest.name}", style="bold cyan")

    # Show the tasks with Serial Number and Name for selection
    table = Table(show_header=True, header_style="bold cyan", title="Available Tasks")
    table.add_column("S.No")
    table.add_column("Task Name")

    for i, task in enumerate(tasks, start=1):
        table.add_row(str(i), task.name)

    console.print(table)

    task_number = int(
        console.input("[bold green]Select a task by entering the S.No: [/bold green]")
    )

    if 1 <= task_number <= len(tasks):
        selected_task = tasks[task_number - 1]
        console.print(f"You have selected: {selected_task.name}", style="bold cyan")
        message = console.input(
            "[bold green]Enter a message for this assignment (optional): [/bold green]"
        )

        if message:
            # Append the message to the quest's path
            with open(quest.path, "a") as file:
                file.write(
                    f"\nTask assigned: {selected_task.name}\nMessage: {message}\n"
                )

        # Update the task status to 'STARTED'
        selected_task.status = Status.started

        session.commit()
        console.print(f"Task '{selected_task.name}' is now started", style="bold green")
    else:
        console.print("Invalid task number.", style="bold red")


@task_group.command(name="completed")
def mark_task_completed():
    """Mark a task as completed"""
    quest = questManager.get_active_quest()

    if quest is None:
        console.print(
            "No active quest found. Please start a quest first.", style="bold red"
        )
        return

    tasks = (
        session.query(Task)
        .filter(Task.quest_id == quest.id)
        .filter(Task.status == Status.started)
        .all()
    )

    if not tasks:
        console.print("No tasks available for completion.", style="bold red")
        return

    console.print(f"Quest: {quest.name}", style="bold cyan")

    # Show the tasks with Serial Number and Name for selection
    table = Table(show_header=True, header_style="bold cyan", title="In-progress Tasks")
    table.add_column("S.No")
    table.add_column("Task Name")

    for i, task in enumerate(tasks, start=1):
        table.add_row(str(i), task.name)

    console.print(table)

    task_number = int(
        console.input("[bold green]Select a task by entering the S.No: [/bold green]")
    )

    if 1 <= task_number <= len(tasks):
        selected_task = tasks[task_number - 1]
        console.print(f"You have selected: {selected_task.name}", style="bold cyan")

        # Update the task status to 'COMPLETED'
        selected_task.status = Status.completed
        users = session.query(User).filter(User.id == user_id).first()
        users.xp += 50
        console.print(
            f"Task '{selected_task.name}' has been completed.", style="bold green"
        )
        session.commit()

    else:
        console.print("Invalid task number.", style="bold red")


main.add_command(guild)

if __name__ == "__main__":
    main()
