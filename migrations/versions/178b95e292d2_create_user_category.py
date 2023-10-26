"""create user category

Revision ID: 178b95e292d2
Revises: 
Create Date: 2023-10-26 11:16:23.835948

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '178b95e292d2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('is_active', sa.Boolean, nullable=False, server_default=sa.sql.false()))
    op.add_column('users',sa.Column('is_superuser', sa.Boolean, nullable=False, server_default=sa.sql.false()))
    op.add_column('users',sa.Column('is_admin', sa.Boolean, nullable=False, server_default=sa.sql.false()))


def downgrade() -> None:
    op.drop_column('users','is_active')
    op.drop_column('users', 'is_admin')
    op.drop_column('users', 'is_superuser')
