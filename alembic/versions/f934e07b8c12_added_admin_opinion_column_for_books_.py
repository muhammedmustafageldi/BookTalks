"""Added admin_opinion column for books table and author_info column for authors table.

Revision ID: f934e07b8c12
Revises: d1c0ccddd36c
Create Date: 2025-04-30 17:35:18.291707

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f934e07b8c12'
down_revision: Union[str, None] = 'd1c0ccddd36c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('books', sa.Column('admin_opinion', sa.String(), nullable=True))
    op.add_column('authors', sa.Column('author_info', sa.String(), nullable=True))


def downgrade() -> None:
    pass
