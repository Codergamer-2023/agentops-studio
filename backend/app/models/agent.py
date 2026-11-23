
import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    model_name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    configuration: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    project: Mapped["Project"] = relationship(
        back_populates="agents",
    )

    runs: Mapped[list["AgentRun"]] = relationship(
        back_populates="agent",
        cascade="all, delete-orphan",
    )
