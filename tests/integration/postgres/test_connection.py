from pytest import fixture
from sqlmodel import text
from config import DATABASE_URL


def test_database_connection(db_session):
    assert db_session is not None
    result = db_session.execute(text("SELECT 1")).scalar()
    assert result == 2
