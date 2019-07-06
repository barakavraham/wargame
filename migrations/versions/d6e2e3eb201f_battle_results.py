"""battle results

Revision ID: d6e2e3eb201f
Revises: 023b8d65cb82
Create Date: 2019-07-06 10:11:29.395163

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'd6e2e3eb201f'
down_revision = '023b8d65cb82'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('battle_results',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('attacker_army_id', sa.Integer(), nullable=True),
                    sa.Column('attacked_army_id', sa.Integer(), nullable=True),
                    sa.Column('attacker_result', sqlalchemy_utils.types.json.JSONType(), nullable=False),
                    sa.Column('attacked_result', sqlalchemy_utils.types.json.JSONType(), nullable=False),
                    sa.Column('did_attacker_win', sa.Boolean(), nullable=True),
                    sa.ForeignKeyConstraint(['attacked_army_id'], ['armies.id'], ),
                    sa.ForeignKeyConstraint(['attacker_army_id'], ['armies.id'], ),
                    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('battle_results')
