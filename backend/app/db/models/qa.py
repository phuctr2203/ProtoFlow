import uuid
from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class QAReportRecord(Base):
    __tablename__ = "qa_reports"
    __table_args__ = (UniqueConstraint("project_id", "mvp_version", name="uq_qa_project_mvp"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    mvp_version: Mapped[int] = mapped_column(Integer, nullable=False)
    demo_ready: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    data: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
