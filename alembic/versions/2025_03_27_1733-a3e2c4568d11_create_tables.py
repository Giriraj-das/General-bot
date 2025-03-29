"""Create tables

Revision ID: a3e2c4568d11
Revises:
Create Date: 2025-03-27 17:33:41.661380

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a3e2c4568d11"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "locations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("city", sa.String(), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_locations")),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_tg_id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("username", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    )
    op.create_table(
        "user_location",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("location_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["location_id"],
            ["locations.id"],
            name=op.f("fk_user_location_location_id_locations"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_user_location_user_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_location")),
        sa.UniqueConstraint(
            "user_id",
            "location_id",
            name=op.f("uq_user_location_user_id_location_id"),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("user_location")
    op.drop_table("users")
    op.drop_table("locations")
