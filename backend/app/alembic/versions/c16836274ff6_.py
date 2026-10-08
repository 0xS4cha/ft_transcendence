"""empty message

Revision ID: c16836274ff6
Revises: b5981d3bc4f8, f5e06617d3b0
Create Date: 2026-10-08 09:58:47.561739

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c16836274ff6'
down_revision: Union[str, Sequence[str], None] = ('b5981d3bc4f8', 'f5e06617d3b0')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
