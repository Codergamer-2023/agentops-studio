
from datetime import datetime, timezone
from dbm import error
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.agent_runtime.lifecycle import (
    RunStatus,
    transition_status,
)
from app.models.agent_run import AgentRun


def create_agent_run(
    db: Session,
    *,
    agent_id: UUID,
    input_data: dict[str, Any],
) -> AgentRun:
    """Create and persist a new pending agent run."""

    run = AgentRun(
        agent_id=agent_id,
        status=RunStatus.PENDING.value,
        input=input_data,
    )

    db.add(run)
    db.flush()

    return run


def transition_agent_run(
    db: Session,
    *,
    run: AgentRun,
    target: RunStatus | str,
    output: dict[str, Any] | None = None,
    error: str | None = None,
) -> AgentRun:
    """Validate and persist an agent run status transition."""

    target_status = RunStatus(target)

    # Validate transition before modifying the database model.
    new_status = transition_status(run.status, target_status)
    # Validate execution result data.
    if new_status == RunStatus.COMPLETED:
        if output is None:
            raise ValueError("Completed runs must contain an output.")
        if error is not None:
            raise ValueError("Completed runs cannot contain an error.")

    elif new_status == RunStatus.FAILED:
        if not error or not error.strip():
            raise ValueError("Failed runs must contain an error message.")
        if output is not None:
            raise ValueError("Failed runs cannot contain an output.")

    elif output is not None or error is not None:
        raise ValueError(
            "Output and error are only accepted for completed or failed runs."
        )
    now = datetime.now(timezone.utc)

    run.status = new_status.value

    if new_status == RunStatus.RUNNING:
        run.started_at = now

    elif new_status in {
        RunStatus.COMPLETED,
        RunStatus.FAILED,
        RunStatus.CANCELLED,
    }:
        run.completed_at = now

    if new_status == RunStatus.COMPLETED:
        run.output = output

    elif new_status == RunStatus.FAILED:
        run.error = error

    db.flush()

    return run
