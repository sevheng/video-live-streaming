"""create_main_tables

Revision ID: 68cd076d9e27
Revises: 
Create Date: 2021-06-06 07:06:43.007421

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '68cd076d9e27'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    
    op.create_table(
        "streaming",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False, index=True),
        sa.Column("status", sa.String(10), nullable=False, index=True),
    )


def downgrade():
    op.drop_table("streaming")
