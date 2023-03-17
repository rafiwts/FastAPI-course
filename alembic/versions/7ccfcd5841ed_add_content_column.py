"""add content column

Revision ID: 7ccfcd5841ed
Revises: 8931f8eeea44
Create Date: 2023-03-17 18:12:23.351909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ccfcd5841ed'
down_revision = '8931f8eeea44'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('postsv2', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('postsv2', 'content')
    pass
