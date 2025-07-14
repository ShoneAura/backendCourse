"""add users

Revision ID: 690f2770efd7
Revises: b1c0041b296e
Create Date: 2024-11-20 16:28:22.086350

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "690f2770efd7"
down_revision: Union[str, None] = "b1c0041b296e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
