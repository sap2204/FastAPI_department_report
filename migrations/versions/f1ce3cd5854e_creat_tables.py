"""Creat tables

Revision ID: f1ce3cd5854e
Revises: 
Create Date: 2024-10-30 10:40:52.660057

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1ce3cd5854e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('workers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('surname', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('middle_name', sa.String(), nullable=False),
    sa.Column('login', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('worker_id', sa.Integer(), nullable=False),
    sa.Column('task', sa.String(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('days_per_task', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['worker_id'], ['workers.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks')
    op.drop_table('workers')
    # ### end Alembic commands ###
