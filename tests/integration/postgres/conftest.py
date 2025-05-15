from app.postgreDB import engine
import sys
import pytest
from sqlmodel import Session
from pathlib import Path

# Ajouter le répertoire racine du projet au chemin Python
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))


@pytest.fixture(scope="session")
def db_engine():
    """ Yields engine objects """
    yield engine


@pytest.fixture(scope="function")
def db_session(db_engine):
    """ Yields session objects """
    assert engine is not None
    session = Session(db_engine)
    yield session
    session.close()


if __name__ == '__main__':
    db_connection()
