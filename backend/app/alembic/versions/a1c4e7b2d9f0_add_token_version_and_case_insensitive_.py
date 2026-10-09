from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = 'a1c4e7b2d9f0'
down_revision: str | Sequence[str] | None = '5d803711036f'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column('token_version', sa.Integer(), server_default=sa.text('0'), nullable=False),
    )
    op.create_index(
        'uq_users_username_lower',
        'users',
        [sa.text('lower(username)')],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index('uq_users_username_lower', table_name='users')
    op.drop_column('users', 'token_version')
