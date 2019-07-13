"""db init

Revision ID: 023b8d65cb82
Revises: 
Create Date: 2019-06-29 12:35:51.371818

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '023b8d65cb82'
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
    op.drop_table('armies')
    op.drop_table('users')
