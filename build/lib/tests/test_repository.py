import pytest
from app.database import ActivityRepository
from app.models import Activity
from uuid import uuid4

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

def test_create_activity_inserts_row(repository):
    '''Repository should insert a row into SQLite.'''
    activity = Activity(activity_type="walk", distance=2.5, duration=40, notes="Evening walk", route="Buffalo Bayou")
    repository.create_activity(activity)

    cursor = repository.connection.cursor()
    cursor.execute(
        '''
        SELECT *
        FROM activities
        '''
    )

    row = cursor.fetchone()

    assert row is not None
    assert row["activity_type"] == "walk"
    assert row["distance"] == 2.5
    assert row["duration"] == 40
    assert row["notes"] == "Evening walk"
    assert row["route"] == "Buffalo Bayou"

def test_create_activity_stores_uuid(repository):
    '''Repository should store the Activity UUID.'''
    activity = Activity(activity_type="run", distance=5, duration=45,)
    repository.create_activity(activity)

    cursor = repository.connection.cursor()
    cursor.execute(
        '''
        SELECT id FROM activities
        '''
    )

    row = cursor.fetchone()

    assert row["id"] == str(activity.id)

def test_create_activity_with_no_optional_fields(repository):
    '''Repository should allow notes and route to be NULL.'''

    activity = Activity(activity_type="walk", distance=1, duration=18,)
    repository.create_activity(activity)

    cursor = repository.connection.cursor()
    cursor.execute(
        '''
        SELECT notes, route 
        FROM activities
        '''
    )

    row = cursor.fetchone()

    assert row["notes"] is None
    assert row["route"] is None

def test_get_all_activites_empty(repository):
    '''Repository should be an empty list.'''
    activities = repository.get_all_activities()

    assert activities == []

def test_get_all_activities_returns_activity(repository):
    '''Repository should be a list with one activity.'''
    activity = Activity(activity_type="run", distance=3, duration=30, notes="Morning", route="Buffalo Creek")
    repository.create_activity(activity)
    activities = repository.get_all_activities()

    assert len(activities) == 1
    loaded = activities[0]

    assert loaded.activity_type == "run"
    assert loaded.distance == 3
    assert loaded.duration == 30
    assert loaded.notes == "Morning"
    assert loaded.route == "Buffalo Creek"
    assert loaded.id == activity.id

def test_get_all_activities_multiple(repository):
    '''Repository should be a list with multiple (2) activities.'''
    repository.create_activity(Activity(activity_type="run", distance=3, duration=30,))
    repository.create_activity(Activity(activity_type="walk", distance=2, duration=40,))

    activities = repository.get_all_activities()

    assert len(activities) == 2

def test_get_activity_by_id(repository):
    '''Repository should retreive activity by id'''
    activity = Activity(activity_type="run", distance=4, duration=32)
    repository.create_activity(activity)

    loaded = repository.get_activity_by_id(activity.id)

    assert loaded is not None
    assert loaded.id == activity.id
    assert loaded.activity_type == activity.activity_type
    assert loaded.distance == activity.distance
    assert loaded.duration == activity.duration

def test_activity_by_id_not_found(repository):
    '''Repository should return None if Id not found'''
    # assert repository.get_activity_by_id(uuid4()) is None
    loaded = repository.get_activity_by_id(uuid4())

    assert loaded is None

def test_update_activity(repository):
    '''Repository should successfully update existing activity'''
    activity = Activity(activity_type="run", distance=3, duration=30, notes="Original run",)
    repository.create_activity(activity)

    updated_activity = Activity(activity_type="run", distance=5, duration=45, notes="Updated run",)
    result = repository.update_activity(activity.id, updated_activity)

    assert result is not None
    assert result.id == activity.id

    loaded = repository.get_activity_by_id(activity.id)

    assert loaded is not None
    assert loaded.distance == 5
    assert loaded.duration == 45
    assert loaded.notes == "Updated run"

def test_update_activity_not_found(repository):
    '''If id not found Repository should return none'''
    activity = Activity(activity_type="run", distance=5, duration=40,)

    result = repository.update_activity(uuid4(), activity)

    assert result is None

def test_delete_activity(repository):
    '''Repository should delete an existing activity.'''
    activity = Activity(activity_type="run", distance=3.0, duration=30.0,)
    repository.create_activity(activity)

    deleted = repository.delete_activity(activity.id)

    assert deleted is True
    assert repository.get_activity_by_id(activity.id) is None

def test_delete_activity_not_found(repository):
    '''Repository should return False when the activity does not exist.'''
    deleted = repository.delete_activity(uuid4())

    assert deleted is False

if __name__ == "__main__":
    pytest.main([__file__])