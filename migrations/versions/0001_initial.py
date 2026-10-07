"""Initial NeuroSync schema."""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("focus_score", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("streak", sa.Integer(), nullable=False, server_default="0"),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    op.create_index("ix_user_email", "user", ["email"], unique=True)

    op.create_table(
        "dataset",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("filename", sa.String(), nullable=False),
        sa.Column("file_type", sa.String(), nullable=False),
        sa.Column("rows", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("columns", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(), nullable=False, server_default="uploaded"),
        sa.Column("analysis_result", sa.JSON(), nullable=True),
        sa.Column("uploaded_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_dataset_user_id", "dataset", ["user_id"])
    op.create_index("ix_dataset_filename", "dataset", ["filename"])


def downgrade():
    op.drop_index("ix_dataset_filename", table_name="dataset")
    op.drop_index("ix_dataset_user_id", table_name="dataset")
    op.drop_table("dataset")
    op.drop_index("ix_user_email", table_name="user")
    op.drop_table("user")
