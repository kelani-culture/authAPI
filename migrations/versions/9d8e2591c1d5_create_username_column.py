"""create username column

Revision ID: 9d8e2591c1d5
Revises: 9f2d0e5715cb
Create Date: 2023-10-26 12:13:01.258748

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d8e2591c1d5'
down_revision: Union[str, None] = '9f2d0e5715cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('username', sa.String, nullable=False,
                                     unique=True))


def downgrade() -> None:
    op.drop_column('users', 'username')
