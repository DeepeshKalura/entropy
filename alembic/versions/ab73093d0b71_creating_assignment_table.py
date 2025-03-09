"""creating assignment table
Revision ID: ab73093d0b71
Revises: a17e6eb97d86
Create Date: 2025-03-08 08:06:13.407836
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab73093d0b71'
down_revision: Union[str, None] = 'a17e6eb97d86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the assignment table
    op.create_table(
        'assignments',
        sa.Column('id', sa.String(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Unicode(200), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('deadline', sa.DateTime(), nullable=False),
        sa.Column('priority', sa.Integer(), nullable=False, server_default=sa.text("3")),
        sa.Column('work_id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), 
                  onupdate=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(['work_id'], ['work.id'], ),
    )
    
    


def downgrade() -> None:
    
    op.drop_table('assignments')