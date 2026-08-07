"""Tests for the ActivityService."""
import pytest
from uuid import uuid4
from app.models import Activity
from app.services import ActivityService
from app.database import ActivityRepository

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

if __name__ == "__main__":
    pytest.main([__file__])