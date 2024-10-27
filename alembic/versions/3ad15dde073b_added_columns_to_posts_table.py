"""Added columns to posts table

Revision ID: 3ad15dde073b
Revises: 164ff062992b
Create Date: 2024-10-27 18:51:26.148288

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ad15dde073b'
down_revision: Union[str, None] = '164ff062992b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
