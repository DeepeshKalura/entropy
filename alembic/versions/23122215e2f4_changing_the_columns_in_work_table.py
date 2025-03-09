"""changing the columns in work table
Revision ID: 23122215e2f4
Revises: ab73093d0b71
Create Date: 2025-03-09 07:46:19.466732
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '23122215e2f4'
down_revision: Union[str, None] = 'ab73093d0b71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Rename create_at to created_at
    op.alter_column('work', 'create_at', new_column_name='created_at')
    
    # Rename update_at to updated_at
    op.alter_column('work', 'update_at', new_column_name='updated_at')

def downgrade() -> None:
    # Revert changes if needed to rollback
    op.alter_column('work', 'created_at', new_column_name='create_at')
    op.alter_column('work', 'updated_at', new_column_name='update_at')