"""empty message

Revision ID: 88ab45cdc7e8
Revises: 
Create Date: 2023-05-01 17:30:42.708661

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '88ab45cdc7e8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('icon', sa.String(length=128), nullable=True),
    sa.Column('add_date', sa.DateTime(), nullable=False),
    sa.Column('pub_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('add_date', sa.DateTime(), nullable=False),
    sa.Column('pub_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('desc', sa.String(length=128), nullable=False),
    sa.Column('has_type', sa.Enum('draft', 'show', name='postpublishtype'), server_default='show', nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('content', mysql.LONGTEXT(), nullable=False),
    sa.Column('add_date', sa.DateTime(), nullable=False),
    sa.Column('pub_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tags_post',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('tag_id', 'post_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tags_post')
    op.drop_table('post')
    op.drop_table('tag')
    op.drop_table('category')
    # ### end Alembic commands ###
