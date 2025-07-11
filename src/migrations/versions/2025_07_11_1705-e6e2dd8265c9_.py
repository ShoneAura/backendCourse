"""empty message

Revision ID: e6e2dd8265c9
Revises: 235c8ff5ccfc
Create Date: 2025-07-11 17:05:24.458499

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e6e2dd8265c9"
down_revision: Union[str, None] = "235c8ff5ccfc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
