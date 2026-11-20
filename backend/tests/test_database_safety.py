
from sqlalchemy import text

from app.core.config import get_settings


def test_database_session_uses_isolated_test_database(db_session) -> None:
    settings = get_settings()

    database_name = db_session.execute(
        text("SELECT current_database()")
    ).scalar_one()

    assert database_name == settings.test_database_name
    assert database_name != settings.postgres_db
