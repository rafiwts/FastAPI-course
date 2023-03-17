"""add user table

Revision ID: 24d63da8dc27
Revises: 7ccfcd5841ed
Create Date: 2023-03-17 18:18:03.849067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24d63da8dc27'
down_revision = '7ccfcd5841ed'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                        sa.Column('id', sa.Integer(), nullable=False),
                        sa.Column('email', sa.String(), nullable=False),
                        sa.Column('password', sa.String(), nullable=False),
                        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                        sa.PrimaryKeyConstraint('id'),
                        sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
