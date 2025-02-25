"""create goals table and create priority in work

Revision ID: 97babe2bb3cd
Revises: bfc8783ffe69
Create Date: 2025-02-26 12:34:56.789012

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97babe2bb3cd'
down_revision = 'bfc8783ffe69'
branch_labels = None
depends_on = None


def upgrade() -> None:

    with op.batch_alter_table("work", schema=None) as batch_op:
        batch_op.add_column(sa.Column("priority", sa.Integer(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table("work", schema=None) as batch_op:
        batch_op.drop_column("priority")
