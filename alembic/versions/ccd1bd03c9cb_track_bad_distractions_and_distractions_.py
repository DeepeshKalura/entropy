"""track bad distractions and distractions occur during task

Revision ID: ccd1bd03c9cb
Revises: 97babe2bb3cd
Create Date: 2025-02-27 00:15:24.971272

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.schema import Column
from sqlalchemy.types import DateTime, String, Unicode
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision: str = "ccd1bd03c9cb"
down_revision: Union[str, None] = "97babe2bb3cd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "distractions",
        Column("id", String, primary_key=True),
        Column("name", String, nullable=False),
        Column("description", Unicode(200)),
        Column("level_of_distraction", String, nullable=False),
        Column("create_at", DateTime, server_default=text("CURRENT_TIMESTAMP")),
        Column("update_at", DateTime, server_default=text("CURRENT_TIMESTAMP")),
    )

    op.execute(
        """
    INSERT INTO distractions (id, name, description, level_of_distraction) 
    VALUES (
        '64b527c9-4e7b-4768-944c-ffaee7fb2f59', 
        'YouTube', 
        'Video streaming platform people create addictive and good content here.', 
        'HIGH'
    )
    """
    )


def downgrade() -> None:
    op.drop_table("distractions")
