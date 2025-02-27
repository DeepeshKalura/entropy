"""adding path to distractions

Revision ID: f55da28be48d
Revises: ccd1bd03c9cb
Create Date: 2025-02-27 10:11:17.274748

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.schema import Column
from sqlalchemy.types import String
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision: str = "f55da28be48d"
down_revision: Union[str, None] = "ccd1bd03c9cb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("distractions", Column("path", String(), nullable=True))

    conn = op.get_bind()
    # Import path utilities
    from src.utility import NotesPath

    # Get the appropriate path from utility
    conn.execute(
        text(
            f"UPDATE distractions SET path = '{os.path.join(NotesPath.tag_path(), 'YouTube.md')}'"
        )
    )

    with op.batch_alter_table("distractions") as batch_op:
        batch_op.alter_column("path", nullable=False)

def downgrade() -> None:
    op.drop_column("distractions", "path")
