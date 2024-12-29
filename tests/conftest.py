import pytest
from database.db_setup import initialize_database
import os
import sqlite3


@pytest.fixture(scope="function")
def setup_test_db():
    """
    Fixture to set up a test database for testing and clean it up afterward.
    """
    db_path = "test_main_sports.db"

    # Create the test database using the existing schema setup
    initialize_database(db_path)

    # Track active connections
    active_connections = []

    # Hook to track connections made via sqlite3.connect
    original_connect = sqlite3.connect

    def tracked_connect(*args, **kwargs):
        connection = original_connect(*args, **kwargs)
        active_connections.append(connection)
        return connection

    sqlite3.connect = tracked_connect  # Replace sqlite3.connect with the tracking function

    yield db_path  # Provide the test database path to the tests

    # Restore the original sqlite3.connect function
    sqlite3.connect = original_connect

    # Close all active connections
    for connection in active_connections:
        try:
            connection.close()
        except sqlite3.Error as e:
            print(f"Error while closing database connection: {e}")

    # Attempt to delete the database file
    try:
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"Test database {db_path} deleted successfully.")
    except PermissionError as e:
        print(f"PermissionError: Unable to delete {db_path}. Ensure no active connections. Error: {e}")
    except Exception as e:
        print(f"Unexpected error during database deletion: {e}")
