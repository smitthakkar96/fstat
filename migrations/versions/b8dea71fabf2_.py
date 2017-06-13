"""Add a table called bug_failure

 Revision ID: b8dea71fabf2
 Revises: 576e73f71990
 Create Date: 2017-05-26 17:08:18.925543

 """
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8dea71fabf2'
down_revision = '576e73f71990'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('bug_failure',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('failure_id', sa.Integer(), nullable=False),
    sa.Column('bug_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['failure_id'], ['failure.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('bug_failure')
