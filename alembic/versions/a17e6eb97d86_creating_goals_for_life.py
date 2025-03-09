"""creating goals for life

Revision ID: a17e6eb97d86
Revises: 84a244c3ef8b
Create Date: 2025-03-08 07:03:16.315503

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a17e6eb97d86'
down_revision: Union[str, None] = '84a244c3ef8b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("goals")
    op.create_table(
        "goals",
        sa.Column("id",  sa.String, primary_key=True),
        sa.Column("what",  sa.Unicode(200), nullable=False),
        sa.Column("path", sa.String, nullable=False),
        sa.Column("status", sa.String, nullable=False),
        sa.Column("created_at",  sa.DateTime, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime, server_default=sa.text("CURRENT_TIMESTAMP"))   
    )   


def downgrade() -> None:
    op.drop_table("goals")
