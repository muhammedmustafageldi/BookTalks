"""Create number of pages for books table

Revision ID: d1c0ccddd36c
Revises: 
Create Date: 2025-02-18 13:18:19.853727

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1c0ccddd36c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('books', sa.Column('page_count', sa.Integer(), nullable=True))

def downgrade() -> None:
    pass
