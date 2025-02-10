"""create hobby table

Revision ID: 37d224f12406
Revises: 
Create Date: 2025-02-10 17:12:22.312456

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.schema import Column
from sqlalchemy.sql.expression import text
from sqlalchemy.types import DateTime, String, Unicode
# revision identifiers, used by Alembic.
revision: str = '37d224f12406'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "hobbies",
        Column('id', String, primary_key=True),
        Column('name', String, nullable=False),
        Column('description', Unicode(200)),
        Column('create_at', DateTime, server_default=text("CURRENT_TIMESTAMP")),
        Column('update_at', DateTime, server_default=text("CURRENT_TIMESTAMP")),
    )


def downgrade() -> None:
    op.drop_table("hobbies")
