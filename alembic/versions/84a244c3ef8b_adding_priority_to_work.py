"""adding priority to work

Revision ID: 84a244c3ef8b
Revises: 9cf4dbba8641
Create Date: 2025-02-28 10:23:29.409627

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision: str = "84a244c3ef8b"
down_revision: Union[str, None] = "9cf4dbba8641"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    conn = op.get_bind()
    inspector = inspect(conn)
    columns = [col["name"] for col in inspector.get_columns("work")]

    if "priority" not in columns:
        op.add_column(
            "work",
            sa.Column("priority", sa.Integer(), nullable=False, server_default="5"),
        )


def downgrade():
    op.drop_column("work", "priority")
