"""1.0.10

Revision ID: d633ca6cd572
Revises: a521fbc28b18
Create Date: 2023-10-12 08:54:49.728638

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'd633ca6cd572'
down_revision = 'a521fbc28b18'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    try:
        with op.batch_alter_table("subscribe") as batch_op:
            batch_op.add_column(sa.Column('quality', sa.String, nullable=True))
            batch_op.add_column(sa.Column('resolution', sa.String, nullable=True))
            batch_op.add_column(sa.Column('effect', sa.String, nullable=True))
    except Exception:
        pass
    # ### end Alembic commands ###


def downgrade() -> None:
    pass
