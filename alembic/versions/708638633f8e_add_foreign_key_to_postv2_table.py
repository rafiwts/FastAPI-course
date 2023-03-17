"""add foreign key to postv2 table

Revision ID: 708638633f8e
Revises: 24d63da8dc27
Create Date: 2023-03-17 18:29:24.965241

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '708638633f8e'
down_revision = '24d63da8dc27'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('postsv2', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'post_user_fk',
        source_table='postsv2',
        referent_table='users',
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )
    pass


def downgrade():
    op.drop_constraint("post_user_fk", table_name="postsv2")
    op.drop_column('postsv2', 'owner_id')
    pass