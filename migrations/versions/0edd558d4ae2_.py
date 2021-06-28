"""empty message

Revision ID: 0edd558d4ae2
Revises: 707fe809e7a1
Create Date: 2021-06-27 16:30:52.703468

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0edd558d4ae2'
down_revision = '707fe809e7a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('timeline', 'text',
               existing_type=mysql.LONGTEXT(),
               type_=sa.Text(length=4294000000),
               existing_nullable=False)
    op.alter_column('user', 'user_id',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.BigInteger(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'user_id',
               existing_type=sa.BigInteger(),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=False)
    op.alter_column('timeline', 'text',
               existing_type=sa.Text(length=4294000000),
               type_=mysql.LONGTEXT(),
               existing_nullable=False)
    # ### end Alembic commands ###