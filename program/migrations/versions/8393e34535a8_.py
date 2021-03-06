"""empty message

Revision ID: 8393e34535a8
Revises: 
Create Date: 2021-12-16 20:54:06.969218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8393e34535a8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('flasklogin-users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=40), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('blogs',
    sa.Column('blog_id', sa.Integer(), nullable=False),
    sa.Column('blog_title', sa.String(length=80), nullable=False),
    sa.Column('blog_content', sa.Text(), nullable=True),
    sa.Column('blog_created', sa.Date(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['flasklogin-users.user_id'], ),
    sa.PrimaryKeyConstraint('blog_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blogs')
    op.drop_table('flasklogin-users')
    # ### end Alembic commands ###
