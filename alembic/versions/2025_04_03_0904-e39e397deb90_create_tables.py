"""Create tables

Revision ID: e39e397deb90
Revises:
Create Date: 2025-04-03 09:04:33.318909

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e39e397deb90"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "buyer_names",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_buyer_names")),
        sa.UniqueConstraint("name", name=op.f("uq_buyer_names_name")),
    )
    op.create_table(
        "locations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("city", sa.String(), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_locations")),
    )
    op.create_table(
        "supplies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "current_date",
            sa.Date(),
            server_default=sa.text("(CURRENT_DATE)"),
            nullable=False,
        ),
        sa.Column("quantity", sa.Float(), server_default="0", nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_supplies")),
        sa.UniqueConstraint(
            "current_date", name=op.f("uq_supplies_current_date")
        ),
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
        "sales",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("buyer_name_id", sa.Integer(), nullable=False),
        sa.Column("price", sa.Integer(), server_default="0", nullable=False),
        sa.Column("quantity", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ["buyer_name_id"],
            ["buyer_names.id"],
            name=op.f("fk_sales_buyer_name_id_buyer_names"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_sales")),
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
    op.create_table(
        "supply_sale",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("supply_id", sa.Integer(), nullable=False),
        sa.Column("sale_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["sale_id"],
            ["sales.id"],
            name=op.f("fk_supply_sale_sale_id_sales"),
        ),
        sa.ForeignKeyConstraint(
            ["supply_id"],
            ["supplies.id"],
            name=op.f("fk_supply_sale_supply_id_supplies"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_supply_sale")),
        sa.UniqueConstraint(
            "supply_id",
            "sale_id",
            name=op.f("uq_supply_sale_supply_id_sale_id"),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("supply_sale")
    op.drop_table("user_location")
    op.drop_table("sales")
    op.drop_table("users")
    op.drop_table("supplies")
    op.drop_table("locations")
    op.drop_table("buyer_names")
