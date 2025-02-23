"""creating skills title and categories seeder

Revision ID: 4a17123661ce
Revises: f1f602e9aaf8
Create Date: 2025-02-22 12:49:57.992215

"""

from typing import Sequence, Union
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "4a17123661ce"
down_revision: Union[str, None] = "f1f602e9aaf8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    id: str = "651001da-1379-41db-bf67-05000d5a038e"
    user_id: str = "9c3b7aed6c18407a9bea3d162c4eeaa0"
    path: str = "Documents/adventure/3-tags"
    sql_query = f"INSERT INTO character_statistics (id, user_id, strength, agility, dexterity, intellect, speed, charisma, luck, movement, stamina, perception, path, create_at, update_at) VALUES ('{id}', '{user_id}', {int(10)}, {int(10)}, {int(10)}, {int(10)}, {int(10)}, {int(10)}, {int(10)}, {int(10)}, {int(10)}, {int(10)}, '{path}', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"
    op.execute(sql_query)


def downgrade() -> None:
    id: str = "651001da-1379-41db-bf67-05000d5a038e"
    sql_query = f"DELETE FROM character_statistics WHERE id = '{id}'"
    op.execute(sql_query)
