from sqlalchemy.orm import configure_mappers

from app.db.base import Base
import app.models


def test_all_domain_models_are_registered() -> None:
    expected_tables = {
        "workspaces",
        "projects",
        "agents",
        "agent_runs",
    }

    assert set(Base.metadata.tables.keys()) == expected_tables


def test_domain_model_relationships_are_valid() -> None:
    configure_mappers()

    assert Base.metadata.tables["projects"] is not None
    assert Base.metadata.tables["agents"] is not None
    assert Base.metadata.tables["agent_runs"] is not None
