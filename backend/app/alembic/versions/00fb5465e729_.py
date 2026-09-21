"""empty message

Revision ID: 00fb5465e729
Revises: 488416a5f04f, c9e76d9ccd90
Create Date: 2026-09-21 10:04:00.803588

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00fb5465e729'
down_revision: Union[str, Sequence[str], None] = ('488416a5f04f', 'c9e76d9ccd90')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
