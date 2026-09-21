"""empty message

Revision ID: 00fb5465e729
Revises: 488416a5f04f, c9e76d9ccd90
Create Date: 2026-09-21 10:04:00.803588

"""
from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = '00fb5465e729'
down_revision: str | Sequence[str] | None = ('488416a5f04f', 'c9e76d9ccd90')
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""

def downgrade() -> None:
    """Downgrade schema."""
