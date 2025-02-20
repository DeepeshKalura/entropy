"""
`act.py` is the control thing for entropy. It means
it is the entry points for the cli which is creating with
`click` package.

"""

import os
import datetime
from uuid import uuid4
import random
from rich.console import Console
from rich.table import Table
import click
from sqlalchemy import func
from src.engine import Session
from src.models import Hobby, Task, WannaBe, Work
from src.utility import Status


session = Session()
console = Console()


@click.group()
def main():
    """Entropy CLI - Personal Growth Guide and Level up System"""


@click.command()
@click.argument("category", type=click.Choice(["hobby", "wanna_be", "work", "goal"]))
@click.argument("name")
@click.argument("description")
def add(category, name, description):
    """Add an entry to the selected category"""
    if category == "hobby":
        entry = Hobby(name=name, description=description)
    elif category == "wanna_be":
        entry = WannaBe(name=name, description=description)
    elif category == "work":
        entry = Work(name=name, description=description)
    else:
        click.echo("Invalid category")
        return

    session.add(entry)
    session.commit()
    click.echo(f"Added {name} to {category}")


@main.group()
def task():
    """
    Control the task objects.

    This group command aggregates functionality related to managing tasks within
    the application.
    """


@task.command(name="generate")
def create_random_task():
    """Pick a random open task"""


    category_task = (
        session.query(Work)
        .order_by(func.random())
        .first()
    )

    console.print(f"🎲 Random work: {category_task.name}", style="bold green")
    id = str(uuid4().hex)
    path = f"/home/deepesh/Documents/adventure/1-rough-work/{category_task.name}-{id}.md"
    with open(path, "a+", encoding="utf-8") as f:
        f.write(f"# {category_task.name}\n\n")
    console.print(f"Creating task at {path}")

    given_task = Task(
        id=id,
        name=category_task.name,
        path=path,
        status=Status.started,
        time_taken=0,
    )
    session.add(given_task)
    session.commit()
    console.print(f"✅ Task '{category_task.name}' added successfully!", style="green")


@task.command(name="view")
def view_tasks():
    """View all tasks"""
    tasks = session.query(Task).all()

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Title")
    table.add_column("Path", justify="right")
    table.add_column("Status", justify="center")
    table.add_column("Created At", style="dim", width=12)
    table.add_column("Updated At", style="dim", width=12)
    table.add_column("Time Taken", justify="right")

    for current_task in tasks:
        table.add_row(
            current_task.name,
            current_task.path,
            current_task.status,
            current_task.create_at.strftime("%d-%m-%Y"),
            current_task.update_at.strftime("%d-%m-%Y"),
            current_task.time_taken,
        )

    console.print(table)


@task.command(name="add")
@click.argument("name")
def create_task(name: str):
    """create side task to complete the work"""

    path = f"/home/deepesh/Documents/adventure/1-rough-work/{name}.md"
    console.print(f"Creating task at {path}")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "a+", encoding="utf-8") as _:
            pass

    given_task = Task(
        id=str(uuid4().hex),
        name=name,
        path=path,
        status=Status.started,
        time_taken=0,
    )
    session.add(given_task)
    session.commit()
    console.print(f"✅ Task '{name}' added successfully!", style="green")


main.add_command(add)
main.add_command(task)


if __name__ == "__main__":
    main()
