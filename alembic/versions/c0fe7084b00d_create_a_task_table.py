"""create a task table

Revision ID: c0fe7084b00d
Revises: a23159a06742
Create Date: 2025-02-18 12:58:44.246552

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.schema import Column
from sqlalchemy.sql.expression import text
from sqlalchemy.types import DateTime, String


# revision identifiers, used by Alembic.
revision: str = "c0fe7084b00d"
down_revision: Union[str, None] = "a23159a06742"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tasks",
        Column("id", String, primary_key=True),
        Column("name", String, nullable=False),
        Column("path", String, nullable=False),
        Column("status", String, nullable=False),
        Column("time_taken", String),
        Column("create_at", DateTime, server_default=text("CURRENT_TIMESTAMP")),
        Column("update_at", DateTime, server_default=text("CURRENT_TIMESTAMP")),
    )


def downgrade() -> None:
    op.drop_table("tasks")
