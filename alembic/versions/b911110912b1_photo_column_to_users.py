"""photo column to users

Revision ID: b911110912b1
Revises: 4a17123661ce
Create Date: 2025-02-22 23:51:40.638067

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.schema import Column
from sqlalchemy.types import String

# revision identifiers, used by Alembic.
revision: str = "b911110912b1"
down_revision: Union[str, None] = "4a17123661ce"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", Column("photo", String, nullable=True))
    id: str = "9c3b7aed6c18407a9bea3d162c4eeaa0"
    op.execute(
        f"UPDATE users SET photo = '/home/deepesh/Documents/photo/gapu/deepesh.jpg' WHERE id = '{id}'"
    )


def downgrade() -> None:
    op.drop_column("users", "photo")
