# from rich.layout import Layout
# from rich.text import Text

# @main.command()
# def stats():
#     """Shows stats about the master"""

#     # Mock ID for demonstration
#     id: str = "9c3b7aed6c18407a9bea3d162c4eeaa0"

#     # Get data from database
#     user = session.query(User).filter_by(id=id).first()
#     character_stats = session.query(CharacterStatistics).filter_by(user_id=id).first()
#     user_titles = session.query(UserTitle).filter_by(user_id=id).all()

#     # Create layout
#     layout = Layout()
#     layout.split_column(
#         Layout(name="header"), Layout(name="main"), Layout(name="footer")
#     )
#     layout["main"].split_row(Layout(name="stats"), Layout(name="skills"))

#     # Header with master info
#     header_text = Text()
#     header_text.append(f"\n{user.name}", style="bold cyan")
#     header_text.append(f" - Level {user.xp // 100}", style="yellow")
#     header_text.append(f"\nPath: {user.path}", style="blue")
#     header_text.append(
#         f"\nHeight: {user.height}cm | Weight: {user.weight}kg", style="dim"
#     )
#     if user.description:
#         header_text.append(f"\n{user.description}", style="italic")

#     # Create stats table
#     stats_table = Table(
#         title=f"{user.name} Statistics", show_header=False, border_style="bright_blue"
#     )
#     stats_table.add_column("Stat", style="cyan")
#     stats_table.add_column("Value", justify="right")

#     stats_mapping = {
#         "Strength": character_stats.strength,
#         "Agility": character_stats.agility,
#         "Dexterity": character_stats.dexterity,
#         "Intellect": character_stats.intellect,
#         "Speed": character_stats.speed,
#         "Charisma": character_stats.charisma,
#         "Luck": character_stats.luck,
#         "Movement": character_stats.movement,
#         "Stamina": character_stats.stamina,
#         "Perception": character_stats.perception,
#     }

#     for stat, value in stats_mapping.items():
#         bar = "█" * (value // 2) + "░" * (50 - value // 2)
#         stats_table.add_row(stat, f"{value} {bar}")

#     # Create titles panel
#     titles_text = Text()
#     for i, title in enumerate(user_titles):
#         titles_text.append(
#             f"[{title.title_id}]", style=("bold cyan" if i == 0 else "dim")
#         )
#         if i < len(user_titles) - 1:
#             titles_text.append(" • ")

#     # Combine all elements
#     # console.print(Panel(header_text, title="Master Profile", border_style="cyan"))
#     console.print(stats_table)
#     # console.print(Panel(titles_text, title="Earned Titles", border_style="yellow"))

#     console.print(
#         f"\nMaster created: {user.create_at.strftime('%Y-%m-%d %H:%M:%S')}",
#         style="dim",
#         justify="right",
#     )
