"""Tests for the ActivityService."""
import pytest
from uuid import uuid4
from app.models import Activity
from app.services import ActivityService
from app.database import ActivityRepository
from datetime import datetime

@pytest.fixture
def service():
    repo = ActivityRepository(":memory:") # SQLite creates a temporary in-memory database that disappears after the test.
    service = ActivityService(repo)
    yield service # pause the fixture to run the test
    repo.close()

def test_create_activity(service):
    '''A created activity should be stored.'''
    activity = Activity( activity_type="run", distance=3, duration=25,)
    created = service.create_activity(activity)

    assert created == activity

def test_get_all_activities(service):
    '''Service should return every stored activity.'''
    activity1 = Activity( activity_type="run", distance=3, duration=25,)
    activity2 = Activity( activity_type="walk", distance=2, duration=40,)

    service.create_activity(activity1)
    service.create_activity(activity2)
    activities = service.get_all_activities()

    assert len(activities) == 2

def test_get_activity_by_id(service):
    '''Service should return activity by id.'''
    activity = Activity(activity_type="run", distance=4, duration=32)
    service.repository.create_activity(activity)

    found = service.get_activity_by_id(activity.id)

    assert found is not None
    assert found.id == activity.id

def test_update_activity(service):
    '''Service should update an existing activity'''
    activity = Activity(activity_type="run", distance=3, duration=30, notes="Original",)
    service.create_activity(activity)

    updated_activity = Activity(activity_type="run", distance=5, duration=45, notes="Updated",)
    result = service.update_activity(activity.id, updated_activity)

    assert result is not None
    assert result.id == activity.id
    assert result.distance == 5
    assert result.duration == 45
    assert result.notes == "Updated"

    loaded = service.get_activity_by_id(activity.id)

    assert loaded is not None
    assert loaded.distance == 5
    assert loaded.duration == 45
    assert loaded.notes == "Updated"

def test_update_activity_not_found(service):
    '''Service should return None if id is not found.'''
    activity = Activity(activity_type="run", distance=5, duration=40,)

    result = service.update_activity(uuid4(), activity)

    assert result is None

def test_delete_activity(service):
    '''Service should delete an existing activity.'''
    activity = Activity(activity_type="run", distance=3.0, duration=30.0,)
    service.repository.create_activity(activity)

    deleted = service.delete_activity(activity.id)

    assert deleted is True
    assert service.get_activity_by_id(activity.id) is None
    assert service.repository.get_activity_by_id(activity.id) is None

def test_delete_activity_not_found(service):
    '''Service should return False when the activity does not exist.'''
    deleted = service.delete_activity(uuid4())

    assert deleted is False

def test_export_activities(service, tmp_path):
    '''Service should export stored activities to CSV.'''
    activity = Activity(activity_type="run", distance=3.0, duration=30.0,)

    service.create_activity(activity)

    filepath = tmp_path/"activities.csv"
    service.export_activities(filepath)

    assert filepath.exists()

    content = filepath.read_text(encoding="utf-8")

    assert "activity_type" in content
    assert "run" in content
    assert "3.0" in content
    assert "30.0" in content

def test_sort_activities_by_distance(service):
    '''Activities should be sorted by distance.'''
    activites = [Activity("run", 5, 50), Activity("walk", 2, 40), Activity("run", 8, 80)]
    result = service.sort_activities(activites, "distance")

    assert [activity.distance for activity in result] == [2, 5, 8]

def test_sort_activities_by_distance_descending(service):
    '''Activities should be sorted by distance descending.'''
    activites = [Activity("run", 5, 50), Activity("walk", 2, 40), Activity("run", 8, 80)]
    result = service.sort_activities(activites, "distance", True)

    assert [activity.distance for activity in result] == [8, 5, 2]

def test_sort_activities_by_duration(service):
    '''Activities should be sorted by duration.'''
    activities = [Activity("run", 30, 60), Activity("walk", 2, 20), Activity("run", 5, 45)]
    result = service.sort_activities(activities, "duration")

    assert [activity.duration for activity in result] == [20, 45, 60]

def test_sort_activities_by_pace(service):
    '''Activities should be sorted by pace.'''
    activities = [
        Activity("run", 3, 30), # pace is 10 min/mi
        Activity("walk", 4, 32), # pace is 8 min/mi
        Activity("run", 2, 40),  # pace is 20 min/mi
        ]
    result = service.sort_activities(activities, "pace")

    assert [activity.calculate_pace() for activity in result] == [8, 10, 20]

def test_sort_activities_by_date(service):
    '''Activities should be sorted by date.'''
    older = Activity("run", 3, 30)
    middle = Activity("run", 4, 40)
    newer = Activity("walk", 2, 30)

    # today = datetime.now()
    older.date = datetime(2026, 1, 1)
    middle.date = datetime(2026, 2, 1)
    newer.date = datetime(2026, 3, 1)

    activities = [older, middle, newer]

    result = service.sort_activities(activities, "date")

    assert result == [older, middle, newer]

def test_sort_activities_invalid_field(service):
    '''Invalid sort fields should raise ValueError.'''
    activities = [Activity("run", 3, 30)]

    with pytest.raises(ValueError):
        service.sort_activities(activities, "invalid")

def test_sort_activities_doesnt_modify_original_list(service):
    '''Sorting should return a new list without changing the original.'''
    activity_1 = Activity("run", 5, 50)
    activity_2 = Activity("walk", 2, 40)

    activities = [activity_1, activity_2]

    result = service.sort_activities(activities, "distance")

    assert activities == [activity_1, activity_2]
    assert result == [activity_2, activity_1]

if __name__ == "__main__":
    pytest.main([__file__])
    
# def test_create_activity():
#     """A created activity should be stored."""

#     service = ActivityService()
#     activity = Activity( activity_type="run", distance=3, duration=25,)
#     result = service.create_activity(activity)

#     assert result == activity
#     assert len(service.get_all_activities()) == 1

# def test_get_all_activities():
#     """Service should return every stored activity."""

#     service = ActivityService()
#     activity1 = Activity( activity_type="run", distance=3, duration=25,)
#     activity2 = Activity( activity_type="walk", distance=2, duration=40,)
#     service.create_activity(activity1)
#     service.create_activity(activity2)
#     activities = service.get_all_activities()

#     assert len(activities) == 2
#     assert activity1 in activities
#     assert activity2 in activities

# def test_get_activity_by_id():
#     '''Service should find an activity by its UUID.'''

#     service = ActivityService()
#     activity = Activity( activity_type="run", distance=5, duration=45,)
#     service.create_activity(activity)

#     found = service.get_activity_by_id(activity.id)

#     assert found == activity

# def test_get_activity_by_invalid_id():
#     """Unknown IDs should return None."""

#     service = ActivityService()
#     result = service.get_activity_by_id(uuid4())

#     assert result is None

# def test_update_activity():
#     '''Updating an activity should replace its values.'''
#     service = ActivityService()
#     activity = Activity(activity_type="run", distance=3, duration=30, notes="Morning",)

#     service.create_activity(activity)
#     updated = Activity(activity_type="run", distance=5, duration=45, notes="Evening",)
#     service.update_activity(activity.id, updated)
#     result = service.get_activity_by_id(activity.id)

#     assert result is not None
#     assert result.distance == 5
#     assert result.duration == 45
#     assert result.notes == "Evening"

# def test_update_missing_activity():
#     '''Updating a missing activity should return None.'''

#     service = ActivityService()
#     updated = Activity(activity_type="run", distance=5, duration=45,)
#     result = service.update_activity(uuid4(), updated)

#     assert result is None

# def test_delete_activity():
#     '''Deleting an activity should remove it.'''
#     service = ActivityService()
#     activity = Activity(activity_type="walk", distance=2, duration=35,)

#     service.create_activity(activity)
#     deleted = service.delete_activity(activity.id)

#     assert deleted is True
#     assert len(service.get_all_activities()) == 0

# def test_delete_missing_activity():
#     '''Deleting an unknown activity should return False.'''
#     service = ActivityService()
#     deleted = service.delete_activity(uuid4())

#     assert deleted is False

# def test_create_multiple_activities():
#     '''Service should support storing multiple activities.'''
#     service = ActivityService()

#     for i in range(4):
#         service.create_activity(Activity(activity_type="walk", distance=i + 1, duration=(i + 1) * 10))

#     for i in range(3):
#         service.create_activity(Activity(activity_type="run", distance=i + 1, duration=(i + 1) * 10))    
    
#     assert len(service.get_all_activities()) == 7

# if __name__ == "__main__":
#     pytest.main([__file__])