"""
creating assignment id for assignment and adding description
Revision ID: c9b1059b3b7b
Revises: 23122215e2f4
Create Date: 2025-03-09 08:09:55.532838
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision: str = "c9b1059b3b7b"
down_revision: Union[str, None] = "23122215e2f4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Check if columns exist before trying to add or remove them
    inspector = inspect(op.get_bind())
    task_columns = [col["name"] for col in inspector.get_columns("tasks")]

    # Use batch operations for SQLite
    with op.batch_alter_table("tasks") as batch_op:
        # Skip adding assignment_id if it already exists
        if "assignment_id" not in task_columns:
            batch_op.add_column(sa.Column("assignment_id", sa.String(), nullable=True))

        # Remove description column if it exists in tasks table
        if "description" in task_columns:
            batch_op.drop_column("description")

        # Create the foreign key within the batch operation
        batch_op.create_foreign_key(
            "fk_task_assignment", "assignments", ["assignment_id"], ["id"]
        )


def downgrade():
    # Get the inspector for checking columns in downgrade too
    inspector = inspect(op.get_bind())
    task_columns = [col["name"] for col in inspector.get_columns("tasks")]

    # Use batch operations for downgrade too
    with op.batch_alter_table("tasks") as batch_op:
        # Drop constraint first
        batch_op.drop_constraint("fk_task_assignment", type_="foreignkey")

        # Drop assignment_id column if it exists
        if "assignment_id" in task_columns:
            batch_op.drop_column("assignment_id")

        # Add back description column if it was removed during upgrade
        if "description" not in task_columns:
            batch_op.add_column(
                sa.Column("description", sa.Unicode(200), nullable=True)
            )
