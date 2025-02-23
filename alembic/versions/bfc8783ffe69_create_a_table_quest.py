"""create a table quest

Revision ID: bfc8783ffe69
Revises: f346c4eb678d
Create Date: 2025-02-23 10:54:34.738618

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bfc8783ffe69"
down_revision: Union[str, None] = "f346c4eb678d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "quests",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("path", sa.String(), nullable=False),
        sa.Column(
            "required_completion_rate", sa.Float(), server_default=sa.text("0.1")
        ),
        sa.Column("expiry_date", sa.DateTime(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")
        ),
    )
    with op.batch_alter_table("tasks", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "quest_id",
                sa.String(),
                sa.ForeignKey("quests.id", name="fk_tasks_quest_id"),
                nullable=True,
            )
        )
        batch_op.drop_column("path")


def downgrade() -> None:
    with op.batch_alter_table("tasks", schema=None) as batch_op:
        batch_op.add_column(sa.Column("path", sa.String(), nullable=False))
        batch_op.drop_column("quest_id")
    op.drop_table("quests")
