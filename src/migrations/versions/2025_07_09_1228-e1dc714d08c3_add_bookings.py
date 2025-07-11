"""add bookings

Revision ID: e1dc714d08c3
Revises: cdce8e81b794
Create Date: 2025-07-09 12:28:00.020069

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e1dc714d08c3"
down_revision: Union[str, None] = "cdce8e81b794"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "facilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "rooms_facilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("rooms_id", sa.Integer(), nullable=False),
        sa.Column("facilities_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["facilities_id"],
            ["facilities.id"],
        ),
        sa.ForeignKeyConstraint(
            ["rooms_id"],
            ["rooms.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("rooms_facilities")
    op.drop_table("facilities")
