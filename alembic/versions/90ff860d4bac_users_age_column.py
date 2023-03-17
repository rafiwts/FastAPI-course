"""users_age column

Revision ID: 90ff860d4bac
Revises: ae792f8df0b5
Create Date: 2023-03-17 21:49:21.524344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90ff860d4bac'
down_revision = 'ae792f8df0b5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('users_age', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'users_age')
    # ### end Alembic commands ###
