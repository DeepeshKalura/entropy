"""create wanna_be table

Revision ID: 8810391027d6
Revises: 37d224f12406
Create Date: 2025-02-10 22:57:33.203925

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import String, DateTime, Unicode

# revision identifiers, used by Alembic.
revision: str = "8810391027d6"
down_revision: Union[str, None] = "37d224f12406"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "wanna_be",
        Column("id", String, primary_key=True),
        Column("name", String, nullable=False),
        Column("description", Unicode(200)),
        Column("create_at", DateTime, server_default=text("CURRENT_TIMESTAMP")),
        Column("update_at", DateTime, server_default=text("CURRENT_TIMESTAMP")),
    )


def downgrade() -> None:
    op.drop_table("wanna_be")
