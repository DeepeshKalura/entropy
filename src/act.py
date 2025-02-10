import datetime
import random
import click
from sqlalchemy import func
from src.engine import Session
from src.models import Hobby, WannaBe, Work
from uuid import uuid4


session = Session()

@click.group()
def main():
    """Entropy CLI - Manage hobbies, tasks, and goals"""
    pass


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


@click.command()
def task():
    """Pick a random open task"""
    categories = [ "wanna_be", "work"]
    category = random.choice(categories)

    task = session.query(Hobby).order_by(func.random()).first()

    number:int = random.randint(4, 15)
    date = datetime.datetime.now() + datetime.timedelta(days=number)

    click.secho(f"📅 On {date.strftime('%d-%m-%Y')}, your whole day is dedicated to: {task.name}", fg="green", bold=True)

    if category == "wanna_be":
        task = session.query(WannaBe).order_by(func.random()).first()
        click.secho(f"\n💼 Wanna Be: {task.name}", fg="cyan", bold=True)

        
        category= random.choice(categories)
        if category == "work":
            task = session.query(Work).order_by(func.random()).first()
            click.secho(f"\n🚀 Diplomatic Work: {task.name}", fg="yellow", bold=True)

        else:
            task = session.query(WannaBe).order_by(func.random()).first()
            click.secho(f"\n🚀 Diplomatic Wanna be: {task.name}", fg="yellow", bold=True)
            
    elif category == "work":

        task = session.query(Work).order_by(func.random()).first()
        click.secho(f"\n💼 Work: {task.name}", fg="cyan", bold=True)


        random.shuffle(categories)
        category = random.choice(categories)

        if category == "wanna_be":
            task = session.query(WannaBe).order_by(func.random()).first()
            click.secho(f"\n🚀 Diplomatic Wanna Be: {task.name}", fg="yellow", bold=True)

        else:

            task = session.query(Work).order_by(func.random()).first()
            click.secho(f"\n🚀 Diplomatic Wanna: {task.name}", fg="yellow", bold=True)




main.add_command(add)
main.add_command(task)


if __name__ == "__main__":
    main()
    
