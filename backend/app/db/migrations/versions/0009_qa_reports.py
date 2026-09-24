"""qa reports

Revision ID: 0009
Revises: 0008
Create Date: 2026-09-24

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0009"
down_revision: str | None = "0008"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "qa_reports",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("mvp_version", sa.Integer(), nullable=False),
        sa.Column("demo_ready", sa.Boolean(), nullable=False),
        sa.Column("data", sa.JSON(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("project_id", "mvp_version", name="uq_qa_project_mvp"),
    )


def downgrade() -> None:
    op.drop_table("qa_reports")
