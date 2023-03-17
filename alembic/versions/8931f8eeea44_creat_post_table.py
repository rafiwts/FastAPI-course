"""creat post table

Revision ID: 8931f8eeea44
Revises: 
Create Date: 2023-03-17 12:45:24.250451

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8931f8eeea44'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('postsv2', sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('postsv2')