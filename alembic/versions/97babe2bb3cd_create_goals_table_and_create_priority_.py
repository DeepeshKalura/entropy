"""create goals table and create priority in work

Revision ID: 97babe2bb3cd
Revises: bfc8783ffe69
Create Date: 2025-02-26 12:34:56.789012

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "97babe2bb3cd"
down_revision = "bfc8783ffe69"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("work", sa.Column("priority", sa.Integer(), server_default="5"))


def downgrade() -> None:
    op.drop_column("work", "priority")
