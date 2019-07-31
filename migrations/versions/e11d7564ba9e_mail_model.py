"""mail model

Revision ID: e11d7564ba9e
Revises: 
Create Date: 2019-07-17 16:08:06.109457

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'e11d7564ba9e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=True),
    sa.Column('avatar', sa.String(length=200), nullable=False),
    sa.Column('is_google_user', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('armies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=16), nullable=True),
    sa.Column('coin', sa.Integer(), nullable=False),
    sa.Column('wood', sa.Integer(), nullable=False),
    sa.Column('metal', sa.Integer(), nullable=False),
    sa.Column('field', sa.Integer(), nullable=False),
    sa.Column('diamond', sa.Integer(), nullable=False),
    sa.Column('power', sa.Integer(), nullable=False),
    sa.Column('pistol', sa.Integer(), nullable=False),
    sa.Column('rifle', sa.Integer(), nullable=False),
    sa.Column('tank', sa.Integer(), nullable=False),
    sa.Column('missile_1', sa.Integer(), nullable=False),
    sa.Column('missile_2', sa.Integer(), nullable=False),
    sa.Column('missile_3', sa.Integer(), nullable=False),
    sa.Column('jet', sa.Integer(), nullable=False),
    sa.Column('clan', sa.String(length=15), nullable=True),
    sa.Column('turns', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('mails',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('recipient_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=16), nullable=True),
    sa.Column('content', sa.String(length=256), nullable=True),
    sa.Column('did_viewed', sa.Boolean(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['recipient_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('battle_results',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('attacker_army_id', sa.Integer(), nullable=True),
    sa.Column('attacked_army_id', sa.Integer(), nullable=True),
    sa.Column('attacker_result', sqlalchemy_utils.types.json.JSONType(), nullable=False),
    sa.Column('attacked_result', sqlalchemy_utils.types.json.JSONType(), nullable=False),
    sa.Column('did_attacker_win', sa.Boolean(), nullable=True),
    sa.Column('viewed_by_attacker', sa.Boolean(), nullable=False),
    sa.Column('viewed_by_attacked', sa.Boolean(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['attacked_army_id'], ['armies.id'], ),
    sa.ForeignKeyConstraint(['attacker_army_id'], ['armies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('upgrades',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('army_id', sa.Integer(), nullable=True),
    sa.Column('ground_weapons', sa.Integer(), nullable=False),
    sa.Column('bombs', sa.Integer(), nullable=False),
    sa.Column('air_weapons', sa.Integer(), nullable=False),
    sa.Column('country', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['army_id'], ['armies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('upgrades')
    op.drop_table('battle_results')
    op.drop_table('mails')
    op.drop_table('armies')
    op.drop_table('users')
