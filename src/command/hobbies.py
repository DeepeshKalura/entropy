# @main.group()
# def hobby():
#     """
#     Manage the hobbies data.
#     """


# @hobby.command(name="view")
# def view_hobbies():
#     """View all hobbies"""
#     hobbies = session.query(Hobby).all()
#     print()
#     table = Table(
#         show_header=True,
#         header_style="bold cyan",
#         title="Hobbies",
#         title_style="bold cyan",
#     )
#     table.add_column("Name")
#     table.add_column("Description")
#     table.add_column("Path", justify="right")
#     table.add_column("Created At", style="dim", width=12)
#     table.add_column("Updated At", style="dim", width=12)

#     for hobby in hobbies:
#         table.add_row(
#             hobby.name,
#             hobby.description,
#             "N/A",
#             hobby.create_at.strftime("%d-%m-%Y"),
#             hobby.update_at.strftime("%d-%m-%Y"),
#         )

#     console.print(table)


# @hobby.command(name="add")
# @click.argument("name")
# @click.argument("description")
# def add_hobby(name, description):
#     """Add a hobby"""
#     hobby = Hobby(name=name, description=description)
#     session.add(hobby)
#     session.commit()
#     console.print(f"Added {name} to hobbies", style="green")


# @hobby.command(name="current")
# def current_hobby():
#     """Pick a random hobby"""
#     hobby = session.query(Hobby).order_by(func.random()).first()
#     console.print(f"🎲 Random hobby: {hobby.name}", style="bold green")


# @hobby.command(name="mutate")
# @click.option("--kill", is_flag=True, help="Delete a selected hobby")
# def update_hobby(kill: bool):
#     hobbies = session.query(Hobby).all()

#     table = Table(
#         show_header=True,
#         header_style="bold cyan",
#         border_style=None,
#         title="Hobbies",
#         title_style="bold cyan",
#     )
#     table.add_column("S.No", style="bold")
#     table.add_column("Name")
#     table.add_column("Description")
#     table.add_column("Path", justify="right")

#     for i, hobby in enumerate(hobbies):
#         table.add_row(
#             str(i + 1),
#             hobby.name,
#             hobby.description,
#             "N/A",
#         )

#     console.print(table)
#     serial_number: int = click.prompt(
#         "Enter the name number which you wanted to mutated", type=int
#     )
#     hobby = hobbies[serial_number - 1]

#     hobby_id = hobby.id

#     if kill:
#         result: bool = click.prompt(
#             f"Are you sure you want to delete {hobby.name}?", type=bool, default=False
#         )
#         if not result:
#             console.print("Aborted", style="red")
#             return

#         session.delete(hobby)
#         session.commit()
#         console.print(f"Deleted {hobby.name} from hobbies", style="red")
#         return

#     console.print(f"Updating hobby: {hobby.name}", style="bold green")
#     name = click.prompt("Enter the name", type=str, default=hobby.name)
#     description = click.prompt(
#         "Enter the description", type=str, default=hobby.description
#     )

#     new_hobby = Hobby(
#         id=hobby_id,
#         name=name,
#         description=description,
#         create_at=hobby.create_at,
#         update_at=datetime.datetime.now(),
#     )
#     session.merge(new_hobby)
#     session.commit()
#     console.print(f"Updated {name} to hobbies", style="green")


# main.add_command(hobby)
