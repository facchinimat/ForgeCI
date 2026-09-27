import os
import tempfile
from pathlib import Path


# Create a temporary SQLite database just for pytest.
file_descriptor, database_path = tempfile.mkstemp(
    prefix="forgeci_test_",
    suffix=".db"
)

os.close(file_descriptor)

database_path = Path(database_path).as_posix()

# Override DATABASE_URL before ForgeCI imports database.py.
os.environ["DATABASE_URL"] = (
    f"sqlite+pysqlite:///{database_path}"
)


from forgeci.database import Base, engine
from forgeci.models import Build


# Create the tables needed by the tests.
Base.metadata.create_all(bind=engine)


def pytest_sessionfinish(session, exitstatus):
    # Remove tables and temporary database after pytest finishes.
    Base.metadata.drop_all(bind=engine)

    try:
        os.remove(database_path)
    except FileNotFoundError:
        pass