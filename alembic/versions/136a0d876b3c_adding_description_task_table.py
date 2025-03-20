"""adding description task table
Revision ID: 136a0d876b3c
Revises: c9b1059b3b7b
Create Date: 2025-03-09 08:36:52.509861
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision: str = "136a0d876b3c"
down_revision: Union[str, None] = "c9b1059b3b7b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Check if description column already exists
    inspector = inspect(op.get_bind())
    task_columns = [col["name"] for col in inspector.get_columns("tasks")]

    # Only add description if it doesn't already exist
    if "description" not in task_columns:
        op.add_column("tasks", sa.Column("description", sa.Unicode(200), nullable=True))


def downgrade() -> None:
    # Drop the description column if it exists
    inspector = inspect(op.get_bind())
    task_columns = [col["name"] for col in inspector.get_columns("tasks")]

    if "description" in task_columns:
        with op.batch_alter_table("tasks") as batch_op:
            batch_op.drop_column("description")
