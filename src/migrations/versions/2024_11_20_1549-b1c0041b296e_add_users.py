"""add users

Revision ID: b1c0041b296e
Revises: 860d0fafd98a
Create Date: 2024-11-20 15:49:16.577934

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b1c0041b296e"
down_revision: Union[str, None] = "860d0fafd98a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
