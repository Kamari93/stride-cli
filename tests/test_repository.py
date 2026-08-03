import pytest
from app.database import ActivityRepository

# Test the repository initialization

def test_repository_initializes():
    '''Repository should create successfully.'''
    repository = ActivityRepository(":memory:") # SQLite creates a temporary in-memory database that disappears after the test.

    assert repository is not None
    repository.close()

def test_repository_creates_table():
    '''Verify the table exists and schema creation'''
    repository = ActivityRepository(":memory:")
    cursor = repository.connection.cursor()

    cursor.execute('''
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name='activities'
        '''
    )

    table = cursor.fetchone()
    assert table is not None
    repository.close()

if __name__ == "__main__":
    pytest.main([__file__])