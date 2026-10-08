"""empty message

Revision ID: c16836274ff6
Revises: b5981d3bc4f8, f5e06617d3b0
Create Date: 2026-10-08 09:58:47.561739

"""
from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = 'c16836274ff6'
down_revision: str | Sequence[str] | None = ('b5981d3bc4f8', 'f5e06617d3b0')
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    


def downgrade() -> None:
    """Downgrade schema."""
    
