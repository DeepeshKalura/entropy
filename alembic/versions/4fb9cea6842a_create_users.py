"""create users

Revision ID: 4fb9cea6842a
Revises: c0fe7084b00d
Create Date: 2025-02-21 14:56:15.034267

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.schema import Column
from sqlalchemy.sql.expression import text
from sqlalchemy.types import DateTime, String, Unicode


# revision identifiers, used by Alembic.
revision: str = "4fb9cea6842a"
down_revision: Union[str, None] = "c0fe7084b00d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
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


def downgrade() -> None:
    op.drop_table("users")
