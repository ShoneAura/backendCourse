"""initial migration

Revision ID: 7336f154bd6c
Revises: 
Create Date: 2024-10-15 23:02:31.512962

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '7336f154bd6c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('hotels',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('location', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('hotels')
