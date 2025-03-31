"""Rename column

Revision ID: 179101e4d0db
Revises: 16daa0776f81
Create Date: 2025-03-31 17:11:58.520201

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "179101e4d0db"
down_revision: Union[str, None] = "16daa0776f81"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("supplies", "date_time", new_column_name="current_date")


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("supplies", "current_date", new_column_name="date_time")
