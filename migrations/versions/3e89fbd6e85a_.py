"""empty message

Revision ID: 3e89fbd6e85a
Revises: 635d47efc8b0
Create Date: 2017-12-30 23:48:14.424140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e89fbd6e85a'
down_revision = '635d47efc8b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('desc', sa.String(length=1500), nullable=True),
    sa.Column('food_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['food_id'], ['food.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    # ### end Alembic commands ###
