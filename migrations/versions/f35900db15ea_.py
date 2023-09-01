"""empty message

Revision ID: f35900db15ea
Revises: 1dd2fb6801bb
Create Date: 2023-09-01 01:44:51.299992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f35900db15ea'
down_revision = '1dd2fb6801bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_article',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['article.id'], name=op.f('fk_user_article_article_id_article')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_user_article_user_id_user'))
    )
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.drop_constraint('fk_article_bookmarker_id_user', type_='foreignkey')
        batch_op.drop_column('bookmarker_id')

    with op.batch_alter_table('review', schema=None) as batch_op:
        batch_op.drop_constraint('fk_review_bookmarker_id_user', type_='foreignkey')
        batch_op.drop_column('bookmarker_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('review', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bookmarker_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key('fk_review_bookmarker_id_user', 'user', ['bookmarker_id'], ['id'])

    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bookmarker_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key('fk_article_bookmarker_id_user', 'user', ['bookmarker_id'], ['id'])

    op.drop_table('user_article')
    # ### end Alembic commands ###