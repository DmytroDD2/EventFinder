"""add_models_friendship_unique

Revision ID: a7090ec585c8
Revises: 29e2a0015206
Create Date: 2023-12-23 12:25:40.624798

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7090ec585c8'
down_revision: Union[str, None] = '29e2a0015206'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('_friends_user_uc', 'friendships', ['user_id', 'friend_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('_friends_user_uc', 'friendships', type_='unique')
    # ### end Alembic commands ###
