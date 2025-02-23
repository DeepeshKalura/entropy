"""dropping work and create new work with data

Revision ID: f346c4eb678d
Revises: b911110912b1
Create Date: 2025-02-23 08:48:51.791293

"""

import os
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Column, String, Unicode, DateTime, text


# revision identifiers, used by Alembic.
revision: str = "f346c4eb678d"
down_revision: Union[str, None] = "b911110912b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # I know i can migrate with work but i drop because
    # it has data which i added which cannot be migrated back
    op.drop_table("work")

    op.create_table(
        "work",
        Column("id", String, primary_key=True),
        Column("name", String, nullable=False),
        Column("description", Unicode(200)),
        Column("path", String, nullable=False),
        Column("repo_url", String, nullable=False),
        Column("create_at", DateTime, server_default=text("CURRENT_TIMESTAMP")),
        Column("update_at", DateTime, server_default=text("CURRENT_TIMESTAMP")),
    )

    path = "/home/deepesh/Documents/adventure/3-tags"

    work_data = [
        {
            "id": "803184c9-080c-427c-b0f1-b0445cf5334d",
            "name": "Orca",
            "description": "A simple crypto trading bot",
            "path": "",
            "repo_url": "https://github.com/DeepeshKalura/orca",
        },
        {
            "id": "94faf2dc-7d12-48ec-b206-d55e72892db5",
            "name": "GEHU",
            "description": "My college has projects and task to do",
            "path": "",
            "repo_url": "https://github.com/DeepeshKalura/learnza",
        },
        {
            "id": "92b64d8a-adab-4bbb-b24e-140100b67dad",
            "name": "Dipisha",
            "description": "My sister have me lot's of work to do",
            "path": f"{path}",
            "repo_url": "https://github.com/rovaa-org/dipisha-book-website",
        },
        {
            "id": "3202640f-1454-4bb6-94e6-04dabdc2bf74",
            "name": "Safai",
            "description": "Safai is the business of bharat",
            "path": "",
            "repo_url": "https://github.com/DeepeshKalura/Safai",
        },
        {
            "id": "8bf2f023-d27e-46c1-89b5-51c81d47e6a0",
            "name": "eShadananda",
            "description": "Mobile application for nepal university",
            "path": "",
            "repo_url": "https://github.com/DeepeshKalura/learnza",
        },
    ]

    formatted_work_data = []
    for work in work_data:
        work_copy = work.copy()
        base_path = work_copy["path"] if work_copy["path"] else path
        work_copy["path"] = os.path.join(base_path, f"{work_copy['name']}.md")
        formatted_work_data.append(work_copy)

    from sqlalchemy import table

    work_table = table(
        "work",
        Column("id", String, primary_key=True),
        Column("name", String, nullable=False),
        Column("description", Unicode(200)),
        Column("path", String, nullable=False),
        Column("repo_url", String, nullable=False),
        Column("create_at", DateTime, server_default=text("CURRENT_TIMESTAMP")),
        Column("update_at", DateTime, server_default=text("CURRENT_TIMESTAMP")),
    )
    op.bulk_insert(work_table, formatted_work_data)


def downgrade() -> None:
    op.drop_table("work")
