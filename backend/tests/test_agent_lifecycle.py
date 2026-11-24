
import pytest

from app.agent_runtime.lifecycle import (
    InvalidRunTransition,
    RunStatus,
    transition_status,
)


@pytest.mark.parametrize(
    ("current", "target"),
    [
        (RunStatus.PENDING, RunStatus.RUNNING),
        (RunStatus.PENDING, RunStatus.FAILED),
        (RunStatus.PENDING, RunStatus.CANCELLED),
        (RunStatus.RUNNING, RunStatus.COMPLETED),
        (RunStatus.RUNNING, RunStatus.FAILED),
        (RunStatus.RUNNING, RunStatus.CANCELLED),
    ],
)
def test_valid_status_transitions(current, target):
    assert transition_status(current, target) == target


@pytest.mark.parametrize(
    ("current", "target"),
    [
        (RunStatus.PENDING, RunStatus.COMPLETED),
        (RunStatus.RUNNING, RunStatus.PENDING),
        (RunStatus.COMPLETED, RunStatus.RUNNING),
        (RunStatus.FAILED, RunStatus.COMPLETED),
        (RunStatus.CANCELLED, RunStatus.RUNNING),
    ],
)
def test_invalid_status_transitions(current, target):
    with pytest.raises(InvalidRunTransition):
        transition_status(current, target)


def test_transition_accepts_database_status_strings():
    result = transition_status("pending", "running")

    assert result == RunStatus.RUNNING
