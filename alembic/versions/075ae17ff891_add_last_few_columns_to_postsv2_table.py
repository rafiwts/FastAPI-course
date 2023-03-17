"""add last few columns to postsv2 table

Revision ID: 075ae17ff891
Revises: 708638633f8e
Create Date: 2023-03-17 18:39:36.704024

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '075ae17ff891'
down_revision = '708638633f8e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('postsv2', sa.Column('published', sa.Boolean(), nullable=False, server_default="TRUE"))
    op.add_column('postsv2', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('postsv2', 'published')
    op.drop_column('postsv2', 'created_at')
    pass
