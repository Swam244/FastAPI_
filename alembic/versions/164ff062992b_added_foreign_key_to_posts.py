"""added Foreign key to posts

Revision ID: 164ff062992b
Revises: 1ef4f2d591d6
Create Date: 2024-10-27 18:43:41.739968

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '164ff062992b'
down_revision: Union[str, None] = '1ef4f2d591d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    op.create_foreign_key(
        'posts_users_fk', source_table="posts", referent_table="users",
        local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk',table_name="posts")
    op.drop_column('posts','owner_id')
    op.drop_column('posts','content')
    pass
