import pytest

from app.agent_runtime.lifecycle import InvalidRunTransition, RunStatus
from app.agent_runtime.service import (
    create_agent_run,
    transition_agent_run,
)
from app.models import Agent, Project, Workspace


@pytest.fixture
def sample_agent(db_session):
    workspace = Workspace(
        name="Test Workspace",
        slug="test-workspace",
    )
    db_session.add(workspace)
    db_session.flush()

    project = Project(
        workspace_id=workspace.id,
        name="Test Project",
    )
    db_session.add(project)
    db_session.flush()

    agent = Agent(
        project_id=project.id,
        name="Test Agent",
        provider="groq",
        model_name="test-model",
        configuration={},
    )
    db_session.add(agent)
    db_session.flush()

    return agent


def test_create_agent_run(db_session, sample_agent):
    run = create_agent_run(
        db_session,
        agent_id=sample_agent.id,
        input_data={"prompt": "Hello"},
    )

    assert run.id is not None
    assert run.status == RunStatus.PENDING.value
    assert run.input == {"prompt": "Hello"}
    assert run.output is None
    assert run.error is None


def test_start_agent_run(db_session, sample_agent):
    run = create_agent_run(
        db_session,
        agent_id=sample_agent.id,
        input_data={"prompt": "Hello"},
    )

    transition_agent_run(
        db_session,
        run=run,
        target=RunStatus.RUNNING,
    )

    assert run.status == RunStatus.RUNNING.value
    assert run.started_at is not None


def test_complete_agent_run(db_session, sample_agent):
    run = create_agent_run(
        db_session,
        agent_id=sample_agent.id,
        input_data={"prompt": "Hello"},
    )

    transition_agent_run(
        db_session,
        run=run,
        target=RunStatus.RUNNING,
    )

    transition_agent_run(
        db_session,
        run=run,
        target=RunStatus.COMPLETED,
        output={"response": "Hello there!"},
    )

    assert run.status == RunStatus.COMPLETED.value
    assert run.output == {"response": "Hello there!"}
    assert run.error is None
    assert run.completed_at is not None


def test_fail_agent_run(db_session, sample_agent):
    run = create_agent_run(
        db_session,
        agent_id=sample_agent.id,
        input_data={"prompt": "Hello"},
    )

    transition_agent_run(
        db_session,
        run=run,
        target=RunStatus.RUNNING,
    )

    transition_agent_run(
        db_session,
        run=run,
        target=RunStatus.FAILED,
        error="Provider unavailable",
    )

    assert run.status == RunStatus.FAILED.value
    assert run.error == "Provider unavailable"
    assert run.output is None
    assert run.completed_at is not None


def test_invalid_transition_does_not_modify_run(
    db_session,
    sample_agent,
):
    run = create_agent_run(
        db_session,
        agent_id=sample_agent.id,
        input_data={"prompt": "Hello"},
    )

    with pytest.raises(InvalidRunTransition):
        transition_agent_run(
            db_session,
            run=run,
            target=RunStatus.COMPLETED,
            output={"response": "Invalid"},
        )

    assert run.status == RunStatus.PENDING.value
    assert run.output is None


@pytest.mark.parametrize(
    ("target", "output", "error"),
    [
        (RunStatus.COMPLETED, None, None),
        (RunStatus.COMPLETED, {"response": "OK"}, "Unexpected error"),
        (RunStatus.FAILED, {"response": "OK"}, "Provider unavailable"),
        (RunStatus.FAILED, None, "   "),
    ],
)
def test_invalid_execution_results_are_rejected(
    db_session,
    sample_agent,
    target,
    output,
    error,
):
    run = create_agent_run(
        db_session,
        agent_id=sample_agent.id,
        input_data={"prompt": "Hello"},
    )

    transition_agent_run(
        db_session,
        run=run,
        target=RunStatus.RUNNING,
    )

    with pytest.raises(ValueError):
        transition_agent_run(
            db_session,
            run=run,
            target=target,
            output=output,
            error=error,
        )

    assert run.status == RunStatus.RUNNING.value
