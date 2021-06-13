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
        sa.Column("name", sa.String, nullable=False, index=True),
        sa.Column("status", sa.String(10), nullable=False, index=True),
    )

    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("full_name", sa.String, nullable=False, index=True),
        sa.Column("email", sa.String, nullable=False, index=True),
        sa.Column("hashed_password", sa.String, nullable=False, index=True),
        sa.Column("is_active", sa.Boolean, default=True, index=True),
        sa.Column("is_superuser", sa.Boolean, default=False, index=True)
    )


def downgrade():
    op.drop_table("streaming")
    op.drop_table("user")
