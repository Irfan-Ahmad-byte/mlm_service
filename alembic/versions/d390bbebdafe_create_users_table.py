"""create users table

Revision ID: d390bbebdafe
Revises: 
Create Date: 2025-04-16 00:30:19.806398

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd390bbebdafe'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, default=sa.text("uuid_generate_v4()"), index=True),
        sa.Column("user_id", sa.UUID(as_uuid=True), nullable=False, unique=True, index=True),
        sa.Column("parent_id", sa.UUID(as_uuid=True), sa.ForeignKey("users.user_id"), nullable=True),
        sa.Column("level", sa.Integer(), default=1),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), onupdate=sa.func.now()),
        if_not_exists=True,
    )
    # Create index for parent_id
    op.create_index("idx_users_parent_id", "users", ["parent_id"], if_not_exists=True)
    # Create index for level
    op.create_index("idx_users_level", "users", ["level"], if_not_exists=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
    op.drop_index("idx_users_parent_id", table_name="users")
    op.drop_index("idx_users_level", table_name="users")
    # drop the index for user_id
    op.drop_index("idx_users_user_id", table_name="users")