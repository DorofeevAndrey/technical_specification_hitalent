import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base
from app.db.deps import get_db
from app.main import app


@pytest.fixture(scope="session")
def test_db_url(tmp_path_factory: pytest.TempPathFactory) -> str:
    db_path: Path = tmp_path_factory.mktemp("db") / "test.db"
    return f"sqlite+pysqlite:///{db_path.as_posix()}"


@pytest.fixture()
def client(test_db_url: str) -> TestClient:
    # Use separate test engine + session and override FastAPI dependency.
    engine = create_engine(test_db_url, connect_args={"check_same_thread": False})

    # SQLite doesn't enable FK constraints by default; enable them so CASCADE works in tests.
    @event.listens_for(engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, connection_record):  # noqa: ARG001
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
