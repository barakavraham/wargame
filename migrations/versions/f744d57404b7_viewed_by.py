"""viewed_by

Revision ID: f744d57404b7
Revises: d6e2e3eb201f
Create Date: 2019-07-13 16:09:52.489834

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f744d57404b7'
down_revision = 'd6e2e3eb201f'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('battle_results', schema=None) as batch_op:
        batch_op.add_column(sa.Column('timestamp', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('viewed_by_attacked', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('viewed_by_attacker', sa.Boolean(), nullable=False))


def downgrade():
    with op.batch_alter_table('battle_results', schema=None) as batch_op:
        batch_op.drop_column('viewed_by_attacker')
        batch_op.drop_column('viewed_by_attacked')
        batch_op.drop_column('timestamp')
