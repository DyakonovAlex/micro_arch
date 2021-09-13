"""Init

Revision ID: d10bef4e00a7
Revises: 
Create Date: 2021-09-04 10:46:51.263401

"""
from alembic import op
import sqlalchemy as sa

import sqlalchemy_utils
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd10bef4e00a7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=256), nullable=False),
        sa.Column('email', sa.String(length=128), nullable=False),
        sa.Column('password',
                  sqlalchemy_utils.types.password.PasswordType(),
                  nullable=False), sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'), sa.UniqueConstraint('name'))

    op.create_table(
        'session',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('payload', sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('session')
    op.drop_table('users')
