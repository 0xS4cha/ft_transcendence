"""add chat message

Revision ID: 8d90eb2110fc
Revises: fd8a5a76ed71
Create Date: 2026-09-17 13:51:52.917453

"""
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '8d90eb2110fc'
down_revision: str | Sequence[str] | None = 'fd8a5a76ed71'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'chat_message',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('chat_message')