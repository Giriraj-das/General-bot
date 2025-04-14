"""Add unique in locations city

Revision ID: 0241d52860f1
Revises: fad8206ceb23
Create Date: 2025-04-14 17:49:18.734226

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0241d52860f1"
down_revision: Union[str, None] = "fad8206ceb23"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("locations", schema=None) as batch_op:
        batch_op.create_unique_constraint("uq_locations_city", ["city"])


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("locations", schema=None) as batch_op:
        batch_op.drop_constraint("uq_locations_city", type_="unique")
