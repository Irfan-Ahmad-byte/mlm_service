"""create ranks table

Revision ID: bb89cc72e0ab
Revises: b7046ec0c01c
Create Date: 2025-04-16 00:33:40.542842

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb89cc72e0ab'
down_revision: Union[str, None] = 'b7046ec0c01c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "mlm_user_ranks",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, default=sa.text("uuid_generate_v4()")),
        sa.Column("user_id", sa.UUID(as_uuid=True), nullable=False, unique=True),
        sa.Column("rank", sa.String(), nullable=False),
        sa.Column("achieved_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        if_not_exists=True,
    )
    # Create index for user_id
    op.create_index("idx_mlm_user_ranks_user_id", "mlm_user_ranks", ["user_id"], if_not_exists=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("mlm_user_ranks")
    op.drop_index("idx_mlm_user_ranks_user_id", table_name="mlm_user_ranks")
