import pytest
from finalproject import DatabaseConnection

@pytest.fixture(scope="session")
def db_connection():
    # Setup and teardown for database connection
    connection = DatabaseConnection()
    connection.connect()

    yield connection  # Provide the fixture object

    # Teardown code
    connection.close()

