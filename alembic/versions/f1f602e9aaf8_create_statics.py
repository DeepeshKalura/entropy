"""create statics

Revision ID: f1f602e9aaf8
Revises: 4fb9cea6842a
Create Date: 2025-02-21 15:51:36.692288

"""

import os
from pathlib import Path
from typing import Sequence, Union
from alembic import op
from sqlalchemy import Float, Integer
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.types import DateTime, String, Unicode


# revision identifiers, used by Alembic.
revision: str = "f1f602e9aaf8"
down_revision: Union[str, None] = "4fb9cea6842a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # first i have user i will fill it values and seed it with data.

    directory_path = os.path.join(Path.home(), "Documents/adventure/3-tags")
    os.makedirs(directory_path, exist_ok=True)

    tags_list = [
        "Strength",
        "Agility",
        "Dexterity",
        "Intellect",
        "Speed",
        "Charisma",
        "Luck",
        "Movement",
        "Stamina",
        "Perception",
    ]

    for tag in tags_list:
        file_path = os.path.join(directory_path, f"{tag}.md")
        with open(file_path, "w") as file:
            file.write(f"# How to measure {tag}? \n")

    op.create_table(
        "character_statistics",
        Column("id", String, primary_key=True),
        Column(
            "user_id",
            String,
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        Column("strength", Integer, nullable=False, server_default="10"),
        Column("agility", Integer, nullable=False, server_default="10"),
        Column("dexterity", Integer, nullable=False, server_default="10"),
        Column("intellect", Integer, nullable=False, server_default="10"),
        Column("speed", Integer, nullable=False, server_default="10"),
        Column("charisma", Integer, nullable=False, server_default="10"),
        Column("luck", Integer, nullable=False, server_default="10"),
        Column("movement", Integer, nullable=False, server_default="10"),
        Column("stamina", Integer, nullable=False, server_default="10"),
        Column("perception", Integer, nullable=False, server_default="10"),
        Column("path", String, nullable=False),
        Column("create_at", DateTime, server_default=text("CURRENT_TIMESTAMP")),
        Column("update_at", DateTime, server_default=text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "skills",
        Column("id", String, primary_key=True),
        Column("name", String, nullable=False),
        Column("path", String, nullable=False),
        Column(
            "description",
            Unicode(200),
        ),
        Column("create_at", DateTime, server_default=text("CURRENT_TIMESTAMP")),
        Column("update_at", DateTime, server_default=text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "user_skills",
        Column("id", String, primary_key=True),
        Column(
            "user_id",
            String,
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        Column(
            "skill_id",
            String,
            ForeignKey("skills.id", ondelete="CASCADE"),
            nullable=False,
        ),
        Column("current_level", Integer, nullable=False, server_default="0"),
        Column("path", String, nullable=False),
        Column("max_level", Integer, nullable=False, server_default="100"),
        Column("unlocked_at", DateTime),
        Column("create_at", DateTime, server_default=text("CURRENT_TIMESTAMP")),
        Column("update_at", DateTime, server_default=text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "titles",
        Column("id", String, primary_key=True),
        Column("name", String, nullable=False),
        Column("path", String, nullable=False),
        Column(
            "description",
            Unicode(200),
        ),
        Column("create_at", DateTime, server_default=text("CURRENT_TIMESTAMP")),
        Column("update_at", DateTime, server_default=text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "user_titles",
        Column("id", String, primary_key=True),
        Column(
            "user_id",
            String,
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        Column(
            "title_id",
            String,
            ForeignKey("titles.id", ondelete="CASCADE"),
            nullable=False,
        ),
        Column("path", String, nullable=False),
        Column("create_at", DateTime, server_default=text("CURRENT_TIMESTAMP")),
        Column("update_at", DateTime, server_default=text("CURRENT_TIMESTAMP")),
    )

    op.add_column("users", Column("xp", Integer, nullable=False, server_default="1"))
    op.add_column(
        "users", Column("height", Float, nullable=False, server_default="172")
    )
    op.add_column(
        "users",
        Column(
            "weight",
            Float,
            nullable=False,
            server_default="78",
        ),
    )


def downgrade() -> None:
    op.drop_column("users", "xp")
    op.drop_column("users", "height")
    op.drop_column("users", "weight")

    op.drop_table("user_titles")

    op.drop_table("titles")
    op.drop_table("user_skills")

    op.drop_table("skills")
    op.drop_table("character_statistics")

    directory_path = os.path.join(Path.home(), "/Documents/adventure/3-tags")

    tags_list = [
        "Strength",
        "Agility",
        "Dexterity",
        "Intellect",
        "Speed",
        "Charisma",
        "Luck",
        "Movement",
        "Stamina",
        "Perception",
    ]

    for tag in tags_list:
        directory_path = os.path.join(
            Path.home(), "/Documents/adventure/3-tags", f"{tag}.md"
        )
        os.remove(directory_path)
