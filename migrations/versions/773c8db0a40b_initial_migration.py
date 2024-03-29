"""Initial migration

Revision ID: 773c8db0a40b
Revises: 
Create Date: 2023-06-27 07:48:26.233637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '773c8db0a40b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('firstname', sa.String(length=100), nullable=False),
    sa.Column('lastname', sa.String(length=100), nullable=False),
    sa.Column('password_hash', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('Author', sa.String(), nullable=False),
    sa.Column('Registered', sa.DateTime(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    op.drop_table('user')
    # ### end Alembic commands ###
