"""empty message

Revision ID: 9ed9bb995c44
Revises: 15a496239ca0
Create Date: 2017-12-07 00:52:22.358744

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9ed9bb995c44'
down_revision = '15a496239ca0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('food', 'desc')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('food', sa.Column('desc', mysql.VARCHAR(charset=u'latin1', length=200), nullable=True))
    # ### end Alembic commands ###