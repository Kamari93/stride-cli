import pytest
from app.database import ActivityRepository
from app.models import Activity

@pytest.fixture
def repository():
    repo = ActivityRepository(":memory:") # SQLite creates a temporary in-memory database that disappears after the test.
    yield repo # pause the fixture to run the test
    repo.close()


# Test the repository initialization

def test_repository_initializes(repository):
    '''Repository should create successfully.'''
    # repository = ActivityRepository(":memory:") # SQLite creates a temporary in-memory database that disappears after the test.

    assert repository is not None
    # repository.close()

def test_repository_creates_table(repository):
    '''Verify the table exists and schema creation'''
    # repository = ActivityRepository(":memory:")
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
    # repository.close()

def test_create_activity(repository):
    '''Repository should store an activity. Verifies that method executes, no exceptions, and returned object'''
    activity = Activity(activity_type="run", distance=3.2, duration=28, notes="Morning run",)
    created = repository.create_activity(activity)

    assert created == activity

if __name__ == "__main__":
    pytest.main([__file__])