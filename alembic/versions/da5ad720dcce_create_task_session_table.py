"""create task session table

Revision ID: da5ad720dcce
Revises: f55da28be48d
Create Date: 2025-02-27 10:37:11.566307

"""

from typing import Sequence, Union
from alembic import op
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, DateTime, Unicode
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "da5ad720dcce"
down_revision: Union[str, None] = "f55da28be48d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "task_events",
        Column("id", String, primary_key=True),
        Column("task_id", String, ForeignKey("tasks.id"), nullable=False),
        Column("user_id", String, ForeignKey("users.id"), nullable=False),
        Column("start_time", DateTime, nullable=False),
        Column("end_time", DateTime, nullable=True),
        Column(
            "event_type", String, nullable=False
        ),  # work | distraction | hobby | etc
        Column(
            "event_category", String, nullable=True
        ),  # study | coding | knowledge_gain | diplomatic | management
        Column("notes", Unicode(500), nullable=True),
        Column("create_at", DateTime, server_default=text("CURRENT_TIMESTAMP")),
        Column("update_at", DateTime, server_default=text("CURRENT_TIMESTAMP")),
    )


def downgrade() -> None:
    op.drop_table("task_events")
