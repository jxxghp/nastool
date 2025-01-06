"""2.0.9

Revision ID: 55390f1f77c1
Revises: bf28a012734c
Create Date: 2024-12-24 13:29:32.225532

"""
import contextlib

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '55390f1f77c1'
down_revision = 'bf28a012734c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # 整理历史记录 增加下载器字段
    with contextlib.suppress(Exception):
        op.add_column('transferhistory', sa.Column('downloader', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    pass