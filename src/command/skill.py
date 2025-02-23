# @main.command()
# def skill():
#     """shows player skills which he acquired"""
#     id: str = "9c3b7aed6c18407a9bea3d162c4eeaa0"

#     user_skills = session.query(UserSkill).filter_by(user_id=id).all()

#     skills_table = Table(title="Skills", border_style="bold cyan")
#     skills_table.add_column("Skill", style="cyan")
#     skills_table.add_column("Level", justify="right")
#     skills_table.add_column("Progress", justify="center")

#     for skill in user_skills:
#         progress = (skill.current_level / skill.max_level) * 100
#         bar = "█" * int(progress // 10) + "░" * (10 - int(progress // 10))
#         skills_table.add_row(
#             skill.skill_id,
#             f"{skill.current_level}/{skill.max_level}",
#             f"{bar} {progress:.1f}%",
#         )

#     console.print(skills_table)
