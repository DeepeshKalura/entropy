"""
creating assignment id for assignment and adding description
Revision ID: c9b1059b3b7b
Revises: 23122215e2f4
Create Date: 2025-03-09 08:09:55.532838
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'c9b1059b3b7b'
down_revision: Union[str, None] = '23122215e2f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Add assignment_id and description columns to tasks table
    op.add_column('tasks', sa.Column('assignment_id', sa.String(), nullable=True))
    op.add_column('tasks', sa.Column('description', sa.Unicode(200), nullable=True))
    
    # Add foreign key constraint
    op.create_foreign_key(
        'fk_task_assignment',
        'tasks', 'assignments',
        ['assignment_id'], ['id']
    )

def downgrade() -> None:
    # Drop foreign key constraint first
    op.drop_constraint('fk_task_assignment', 'tasks', type_='foreignkey')
    
    # Then drop the columns
    op.drop_column('tasks', 'assignment_id')
    op.drop_column('tasks', 'description')