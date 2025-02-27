"""adding a work_id column in task

Revision ID: 9cf4dbba8641
Revises: da5ad720dcce
Create Date: 2025-02-27 13:16:16.564815

"""

from typing import Sequence, Union
from alembic import op
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String


# revision identifiers, used by Alembic.
revision: str = "9cf4dbba8641"
down_revision: Union[str, None] = "da5ad720dcce"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("tasks", schema=None) as batch_op:
        batch_op.add_column(
            Column(
                "work_id",
                String,
                ForeignKey("work.id", name="fk_tasks_work_id"),
                nullable=True,
            )
        )


def downgrade() -> None:
    with op.batch_alter_table("tasks", schema=None) as batch_op:
        batch_op.drop_column("work_id")
