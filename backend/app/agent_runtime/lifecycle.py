
from enum import Enum


class RunStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


ALLOWED_TRANSITIONS: dict[RunStatus, set[RunStatus]] = {
    RunStatus.PENDING: {
        RunStatus.RUNNING,
        RunStatus.FAILED,
        RunStatus.CANCELLED,
    },
    RunStatus.RUNNING: {
        RunStatus.COMPLETED,
        RunStatus.FAILED,
        RunStatus.CANCELLED,
    },
    RunStatus.COMPLETED: set(),
    RunStatus.FAILED: set(),
    RunStatus.CANCELLED: set(),
}


class InvalidRunTransition(ValueError):
    """Raised when an agent run attempts an invalid status transition."""


def transition_status(
    current: RunStatus | str,
    target: RunStatus | str,
) -> RunStatus:
    current_status = RunStatus(current)
    target_status = RunStatus(target)

    allowed = ALLOWED_TRANSITIONS[current_status]

    if target_status not in allowed:
        raise InvalidRunTransition(
            f"Cannot transition agent run from "
            f"'{current_status.value}' to '{target_status.value}'."
        )

    return target_status
