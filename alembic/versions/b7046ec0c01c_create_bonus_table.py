"""create bonus table

Revision ID: b7046ec0c01c
Revises: d390bbebdafe
Create Date: 2025-04-16 00:32:09.798269

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7046ec0c01c'
down_revision: Union[str, None] = 'd390bbebdafe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "mlm_bonuses",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, default=sa.text("uuid_generate_v4()")),
        sa.Column("user_id", sa.UUID(as_uuid=True), nullable=False),
        sa.Column("source_user_id", sa.UUID(as_uuid=True), nullable=False),
        sa.Column("level", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("type", sa.String(), default="referral"),
        sa.Column("status", sa.String(), default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        if_not_exists=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("mlm_bonuses")
