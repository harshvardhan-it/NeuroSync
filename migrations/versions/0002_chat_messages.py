"""Persist tenant-scoped AI chat history."""

from alembic import op
import sqlalchemy as sa

revision = "0002_chat_messages"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "chatmessage",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("dataset_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_chatmessage_user_id", "chatmessage", ["user_id"])
    op.create_index("ix_chatmessage_dataset_id", "chatmessage", ["dataset_id"])


def downgrade():
    op.drop_index("ix_chatmessage_dataset_id", table_name="chatmessage")
    op.drop_index("ix_chatmessage_user_id", table_name="chatmessage")
    op.drop_table("chatmessage")
