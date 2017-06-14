"""Add not null constraint to bug_failure and moved
state from failure_instance to failure

Revision ID: 7514a613b106
Revises: b8dea71fabf2
Create Date: 2017-06-14 11:21:24.974585

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7514a613b106'
down_revision = 'b8dea71fabf2'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('bug_failure', 'bug_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('bug_failure', 'failure_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.add_column('failure', sa.Column('state', sa.Integer(), nullable=True))
    op.drop_column('failure_instance', 'state')


def downgrade():
    op.add_column('failure_instance', sa.Column('state', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('failure', 'state')
    op.alter_column('bug_failure', 'failure_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('bug_failure', 'bug_id',
               existing_type=sa.INTEGER(),
               nullable=True)
