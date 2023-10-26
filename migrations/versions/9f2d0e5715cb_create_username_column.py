"""create username column

Revision ID: 9f2d0e5715cb
Revises: 178b95e292d2
Create Date: 2023-10-26 12:12:22.869956

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f2d0e5715cb'
down_revision: Union[str, None] = '178b95e292d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('is_verified', sa.Boolean, nullable=False,
                                     server_default=sa.sql.false()
                                ))


def downgrade() -> None:
    pass
