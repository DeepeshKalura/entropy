"""
`act.py` is the control thing for entropy. It means
it is the entry points for the cli which is creating with
`click` package.

"""

import os
import uuid
from pathlib import Path
import time
from typing import List, Optional
import importlib.metadata
import click
from rich.table import Table
from rich.markdown import Markdown
from rich.box import SIMPLE, ROUNDED
from sqlalchemy import or_
from src.animations_manager import AnimationManager
from src.models import Task, TaskEvents, User, Work, Distractions
from src.utility import (
    DistractionLevel,
    NotesPath,
    Status,
    calculate_level,
    create_progress_bar,
    console,
    session,
    user_id,
    EventType,
    TaskCategories,
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
        minutes_left = (time_left.seconds % 3600) // 60
        seconds_left = time_left.seconds % 60

        if days_left < 0:
            questManager.closing_counter(quest=quest)
            console.print("Time's up! The quest has expired.", style="bold red")
            console.print("Go to guild to get new quest", style="bold green")
            return

        console.print(
            f"Time remaining: {days_left} days, {hours_left} hours, {minutes_left} minutes, {seconds_left} seconds",
            style="red",
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


@main.command(name="event")
@click.option("--notes", "-n", help="Additional notes for the event")
def add_new_event(notes: str):
    """Add a events for a given task"""

    quest = questManager.get_active_quest()

    if quest is None:
        console.print("Please go to guild and get your quest first!", style="bold red")
        return

    task = questManager.started_task_of_quest(quest)

    if task is None:
        console.print(
            "You didn't started any task from current quest. Go! dude take the task from quest",
            style="bold red",
        )
        return

    last_task_event: Optional[TaskEvents] = questManager.task_event_exist()

    if last_task_event:
        last_notes = console.input(
            "[bold green]Write about your last events? [/bold green]"
        )
        questManager.end_current_event(
            event=last_task_event, path=quest.path, end_notes=last_notes
        )

    console.print("\nSelect event type:")
    for idx, event_type in enumerate([EventType.work, EventType.distraction], 1):
        console.print(f"{idx}. {event_type}", style="Bold Cyan")

    # Get user selection
    choice = console.input("\n[bold green]Enter number (1 or 2): [/bold green]")

    try:
        selected_idx = int(choice) - 1
        if selected_idx in [0, 1]:
            selected_event = [EventType.work, EventType.distraction][selected_idx]

            if selected_event == EventType.work:
                console.print("Select event type: ", end=" ")
                for idx, event_type in enumerate(
                    [
                        TaskCategories.visual,
                        TaskCategories.study,
                        TaskCategories.diplomatic,
                        TaskCategories.implementation,
                    ],
                    1,
                ):
                    console.print(f"{idx}. {event_type}", style="Cyan")

                choice = console.input(
                    "\n[bold green]Enter number (1, 2 etc): [/bold green]"
                )

                selected_idx = int(choice) - 1

                if selected_idx in [0, 1, 2, 3]:
                    selected_event_category = [
                        TaskCategories.visual,
                        TaskCategories.study,
                        TaskCategories.diplomatic,
                        TaskCategories.implementation,
                    ][selected_idx]
                    questManager.add_new_event(
                        task=task,
                        event_type=selected_event,
                        event_category=selected_event_category,
                        notes=notes,
                    )
                    console.print(
                        "[bold green]New event has been introduced![/bold green]"
                    )

            elif selected_event == EventType.distraction:
                list_of_distraction: List[Distractions] = session.query(
                    Distractions
                ).all()

                console.print("Select distraction:")
                for idx, distraction in enumerate(list_of_distraction, 1):
                    level_color = (
                        "red"
                        if distraction.level_of_distraction == DistractionLevel.high
                        else "yellow"
                        if distraction.level_of_distraction == DistractionLevel.medium
                        else "green"
                    )
                    console.print(
                        f"{idx}. {distraction.name} [{level_color}]({distraction.level_of_distraction})[/{level_color}]"
                    )

                choice = console.input("\n[bold green]Enter number: [/bold green]")
                try:
                    selected_idx = int(choice) - 1
                    if 0 <= selected_idx < len(list_of_distraction):
                        selected_distraction = list_of_distraction[selected_idx]
                        questManager.add_new_event(
                            task=task,
                            event_type=selected_event,
                            event_category=selected_distraction.name,
                            notes=notes,
                        )
                        console.print(
                            "[bold green]New distraction event has been recorded![/bold green]"
                        )
                    else:
                        console.print("[bold red]Invalid selection.[/bold red]")
                except ValueError:
                    console.print("[bold red]Please enter a valid number.[/bold red]")
            else:
                pass

        else:
            console.print("[bold red]Invalid choice. Please select 1 or 2.[/bold red]")
            return
    except ValueError:
        console.print("[bold red]Please enter a valid number.[/bold red]")
        return


@main.group()
def admin():
    """This admin command let you add works currently"""


@admin.group()
def work():
    """The things which brings towards your goal"""


@work.command(name="add")
@click.argument("name")
def add_work(name: str):
    """Add a new work"""
    id = str(uuid.uuid4())
    description = console.input(
        f"[bold green]Enter a description for {name}: [/bold green]"
    )
    repo_url = console.input("[bold green]Enter the github repo URL: [/bold green]")
    created_resources = []
    try:
        path = os.path.join(NotesPath.tag_path(), f"{name}.md")
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write(f"# {name}\n{description}")
        created_resources.append(("file", path))

        work = Work(
            id=id, name=name, description=description, path=path, repo_url=repo_url
        )
        try:
            session.add(work)
            session.commit()
            console.print(
                "[bold green]✓ Work has been created successfully![/bold green]"
            )
        except Exception as db_error:
            session.rollback()
            raise db_error

    except Exception as e:
        # Rollback and clean up created resources
        for resource_type, resource_id in created_resources:
            if resource_type == "file" and os.path.exists(resource_id):
                try:
                    os.remove(resource_id)
                except Exception as cleanup_error:
                    console.print(
                        f"[bold red]Failed to clean up file {resource_id}: {cleanup_error}[/bold red]"
                    )

            elif resource_type == "db_record":
                try:
                    session.query(Work).filter(Work.id == resource_id).delete()
                    session.commit()
                except Exception as cleanup_error:
                    console.print(
                        f"[bold red]Failed to clean up database record {resource_id}: {cleanup_error}[/bold red]"
                    )

        console.print(f"[bold red]Error creating work item: {e}[/bold red]")


@work.command(name="view")
@click.option("--filter", "-f", help="Filter works by name or description")
@click.option(
    "--sort",
    "-s",
    type=click.Choice(["name", "create_at", "update_at"]),
    default="create_at",
    help="Sort works by field",
)
@click.option("--desc", is_flag=True, help="Sort in descending order")
def view_work(filter, sort, desc):
    """View all work items in a formatted table."""
    try:
        query = session.query(Work)

        # Apply filter if provided
        if filter:
            query = query.filter(
                or_(
                    Work.name.ilike(f"%{filter}%"),
                    Work.description.ilike(f"%{filter}%"),
                )
            )

        # Apply sorting
        order_column = getattr(Work, sort)
        if desc:
            query = query.order_by(order_column.desc())
        else:
            query = query.order_by(order_column)

        works = query.all()

        if not works:
            console.print("[yellow]No work items found.[/yellow]")
            return

        # Create a rich table with wider repository column
        table = Table(show_header=True, header_style="bold blue", box=ROUNDED)
        table.add_column("Name", style="cyan", width=20)
        table.add_column("Description", style="green", width=40)
        table.add_column("Priority", style="Bold red", width=3)
        table.add_column("Repository", style="magenta", width=40)
        table.add_column("Created", style="yellow", width=16)
        table.add_column("Updated", style="yellow", width=16)

        for work in works:
            # Format dates nicely
            created = (
                work.create_at.strftime("%Y-%m-%d %H:%M") if work.create_at else "N/A"
            )
            updated = (
                work.update_at.strftime("%Y-%m-%d %H:%M") if work.update_at else "N/A"
            )

            # Extract username/repo from GitHub URL
            repo_display = work.repo_url
            if "github.com" in repo_display:
                try:
                    # Extract username/repo from GitHub URL
                    url_parts = repo_display.split("github.com/")
                    if len(url_parts) > 1:
                        # Get username/repo part and remove .git if present
                        repo_display = url_parts[1].rstrip("/").replace(".git", "")
                except Exception:
                    # If parsing fails, use fallback truncation
                    if len(repo_display) > 38:
                        repo_display = repo_display[:35] + "..."
            else:
                # For non-GitHub URLs, use regular truncation but with higher limit
                if len(repo_display) > 38:
                    repo_display = repo_display[:35] + "..."

            # Truncate description if too long
            desc_display = work.description
            if desc_display and len(desc_display) > 50:
                desc_display = desc_display[:47] + "..."

            table.add_row(
                work.name,
                desc_display or "No description",
                str(work.priority),
                repo_display,
                created,
                updated,
            )

        # Add summary
        console.print(f"\n[bold green]Work Items[/bold green] - {len(works)} total")
        if filter:
            console.print(f"[italic]Filtered by: {filter}[/italic]")
        console.print(table)

        # Add interaction hints
        console.print(
            "\n[dim]Tip: Use --filter/-f to search, --sort/-s to change sorting, --desc for descending order[/dim]"
        )
        console.print("[dim]Example: view --filter project --sort name --desc[/dim]\n")

    except Exception as e:
        console.print(f"[bold red]Error viewing work items: {e}[/bold red]")


@work.command(name="update")
def update_work():
    """update priority"""

    works = session.query(Work).all()

    table = Table(show_header=True, header_style="bold blue", box=ROUNDED)
    table.add_column("S.NO.", style="Bold Cyan", width=10)
    table.add_column("Name", style="cyan", width=20)
    table.add_column("Priority", style="Bold red", width=10)
    table.add_column("created", style="yellow", width=16)

    for i, work in enumerate(works, 1):
        table.add_row(
            str(i),
            work.name,
            str(work.priority),
            work.create_at.strftime("%Y-%m-%d %H:%M"),
        )

    console.print(table)

    selected_work = console.input(
        "\n[bold green]Enter the S.NO. of work to update priority: [/bold green]"
    )

    try:
        selected_idx = int(selected_work) - 1
        if 0 <= selected_idx < len(works):
            work = works[selected_idx]
            new_priority = console.input(
                "\n[bold green]Enter new priority (1-10): [/bold green]"
            )

            try:
                priority = int(new_priority)
                if 1 <= priority <= 10:
                    work.priority = priority
                    session.commit()
                    console.print(
                        f"\n[bold green]Successfully updated priority for {work.name}![/bold green]"
                    )
                else:
                    console.print(
                        "[bold red]Priority must be between 1 and 10[/bold red]"
                    )
            except ValueError:
                console.print(
                    "[bold red]Please enter a valid number for priority[/bold red]"
                )
        else:
            console.print("[bold red]Invalid work selection[/bold red]")
    except ValueError:
        console.print("[bold red]Please enter a valid work number[/bold red]")

@work.command(name="delete")
@click.argument("name", required=True)
@click.option("--force", "-f", is_flag=True, help="Delete without confirmation")
def delete_work(name, force):
    """Delete a work item by name.

    This will remove the work item from the database and optionally delete the associated file.
    """
    try:
        # Find the work item
        work = session.query(Work).filter(Work.name == name).first()

        if not work:
            console.print(
                f"[bold red]Error:[/bold red] No work item found with name '{name}'"
            )
            return

        # Show work details before deletion
        console.print("\n[bold]Work item details:[/bold]")
        console.print(f"  [cyan]Name:[/cyan] {work.name}")
        console.print(
            f"  [cyan]Description:[/cyan] {work.description or 'No description'}"
        )
        console.print(f"  [cyan]Repository:[/cyan] {work.repo_url}")
        console.print(f"  [cyan]File path:[/cyan] {work.path}")
        console.print(
            f"  [cyan]Created:[/cyan] {work.create_at.strftime('%Y-%m-%d %H:%M') if work.create_at else 'N/A'}"
        )

        # Get confirmation unless force flag is used
        if not force:
            confirmation = console.input(
                "\n[bold red]Are you sure you want to delete this work item? (y/n): [/bold red]"
            ).lower()

            if confirmation != "y" and confirmation != "yes":
                console.print("[yellow]Deletion cancelled.[/yellow]")
                return

        # Track what was deleted for reporting
        deleted_items = []

        # Delete the file if it exists
        if work.path and os.path.exists(work.path):
            try:
                os.remove(work.path)
                deleted_items.append("file")
            except Exception as file_error:
                console.print(
                    f"[bold red]Warning:[/bold red] Failed to delete file: {file_error}"
                )

        # Delete from database
        try:
            session.delete(work)
            session.commit()
            deleted_items.append("database record")
        except Exception as db_error:
            session.rollback()
            console.print(
                f"[bold red]Error:[/bold red] Failed to delete from database: {db_error}"
            )
            return

        # Show success message
        success_message = (
            f"[bold green]Successfully deleted[/bold green] work item '{name}'"
        )
        if deleted_items:
            success_message += f" ({', '.join(deleted_items)})"
        console.print(success_message)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@admin.group()
def distraction():
    """Things which pure wasteful for time"""


@distraction.command(name="add")
@click.option("--name", prompt="Distraction name", help="Name of the distraction")
@click.option(
    "--description", prompt="Description", help="Description of the distraction"
)
@click.option(
    "--level",
    prompt="Level of distraction",
    type=click.Choice(
        [DistractionLevel.low, DistractionLevel.medium, DistractionLevel.high],
        case_sensitive=False,
    ),
    help="How distracting is this item (LOW, MEDIUM, HIGH)",
)
def create_distraction(name, description, level):
    """Create a new distraction record"""

    path = NotesPath.tag_path() + f"/{name}.md"

    # Create the file if it doesn't exist
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(f"# {name}\n\n{description}")

    distraction = Distractions(
        id=str(uuid.uuid4()),
        name=name,
        description=description,
        path=path,
        level_of_distraction=level,
    )

    session.add(distraction)
    session.commit()

    level_color = (
        "red"
        if level == DistractionLevel.high
        else "yellow"
        if level == DistractionLevel.medium
        else "green"
    )

    console.print(
        f"[green]Successfully created distraction:[/green] {name} with level [{level_color}]{level}[/{level_color}]"
    )


@distraction.command(name="view")
def view_distractions():
    """View the existing distractions"""
    distractions = session.query(Distractions).all()

    if not distractions:
        console.print("[yellow]No distractions found.[/yellow]")
        return

    table = Table(
        show_header=True, header_style="bold cyan", title="List of Distractions"
    )
    table.add_column("Name")
    table.add_column("Description")
    table.add_column("Path")
    table.add_column("Level")
    table.add_column("Created At")

    for d in distractions:
        # Color-code based on distraction level
        level_color = (
            "red"
            if d.level_of_distraction == DistractionLevel.high
            else "yellow"
            if d.level_of_distraction == DistractionLevel.medium
            else "green"
        )

        level_formatted = f"[{level_color}]{d.level_of_distraction}[/{level_color}]"

        table.add_row(
            d.name,
            d.description or "N/A",
            d.path,
            level_formatted,
            d.create_at.strftime("%Y-%m-%d %H:%M:%S") if d.create_at else "N/A",
        )

    console.print()
    console.print(table)


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
main.add_command(admin)

if __name__ == "__main__":
    main()
