
import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from sqlalchemy import CheckConstraint, text

class AgentRun(Base):
    __tablename__ = "agent_runs"

    __table_args__ = (
    CheckConstraint(
        "status IN ('pending', 'running', 'completed', 'failed', 'cancelled')",
        name="ck_agent_runs_valid_status",
    ),
)

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    agent_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("agents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="pending",
        server_default=text("'pending'"),
        nullable=False,
        index=True,
    )

    input: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
    )

    output: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    agent: Mapped["Agent"] = relationship(
        back_populates="runs",
    )
