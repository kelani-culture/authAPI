"""change product_name to name

Revision ID: 5762bec50743
Revises: 54f5e77f08dc
Create Date: 2023-10-26 15:39:42.794473

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5762bec50743'
down_revision: Union[str, None] = '54f5e77f08dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('name', sa.String(), nullable=False))
    op.drop_column('products', 'product_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('product_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('products', 'name')
    # ### end Alembic commands ###
