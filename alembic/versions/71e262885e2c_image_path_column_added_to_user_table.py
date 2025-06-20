"""image_path column added to user table.

Revision ID: 71e262885e2c
Revises: f934e07b8c12
Create Date: 2025-06-19 19:47:27.871755

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71e262885e2c'
down_revision: Union[str, None] = 'f934e07b8c12'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column('image_path', sa.String(), server_default='users/default_user_img.png')
    )


def downgrade() -> None:
    op.drop_column('users', 'image_path')

