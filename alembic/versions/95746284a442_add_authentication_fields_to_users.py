"""add authentication fields to users

Revision ID: 95746284a442
Revises: 226c24a90b7c
Create Date: 2026-09-23 21:39:49.024729

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95746284a442'
down_revision: Union[str, Sequence[str], None] = '226c24a90b7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'users',
        sa.Column('hashed_password', sa.String(length=255), nullable=True)
    )

    # Hash bcrypt de una clave temporal para registros previos a autenticación.
    op.execute(
        sa.text(
            "UPDATE users SET hashed_password = :hash "
            "WHERE hashed_password IS NULL"
        ).bindparams(
            hash="$2b$12$KIXH.placeholder.hash.for.existing.users.xxxxxxxxxxxx"
        )
    )

    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column(
            'hashed_password',
            existing_type=sa.String(length=255),
            nullable=False
        )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'hashed_password')
