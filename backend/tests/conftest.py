import pytest

from app.db.base import Base
from app.db.test_session import TestSessionLocal, test_engine
import app.models  # noqa: F401


@pytest.fixture(scope="session", autouse=True)
def create_test_schema():
    """Create database tables exclusively in the isolated test database."""
    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session():
    connection = test_engine.connect()
    transaction = connection.begin()

    session = TestSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()
