"""db init

Revision ID: 02cdd54b9810
Revises: 
Create Date: 2019-05-14 23:00:22.524324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02cdd54b9810'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=True),
    sa.Column('avatar', sa.String(length=100), nullable=False),
    sa.Column('is_google_user', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('army',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('gold', sa.Integer(), nullable=False),
    sa.Column('wood', sa.Integer(), nullable=False),
    sa.Column('metal', sa.Integer(), nullable=False),
    sa.Column('field', sa.Integer(), nullable=False),
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
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('army')
    op.drop_table('user')
    # ### end Alembic commands ###
