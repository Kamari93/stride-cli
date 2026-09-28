"""Tests for the GoalService."""
import pytest
from uuid import uuid4
from app.models import Goal, Activity
from app.services import GoalService
from app.database import ActivityRepository
from datetime import datetime, timedelta

@pytest.fixture
def service():
    """Provide a GoalService using an in-memory SQLite database."""
    repo = ActivityRepository(":memory:")
    service = GoalService(repo)
    yield service # pause the fixture to run the test
    repo.close()


def test_create_goal(service):
    '''A created goal should be stored.'''
    goal = Goal(goal_type="weekly_distance", target=25.0,)
    created = service.create_goal(goal)

    assert created.id == goal.id

def test_get_all_goals(service):
    '''Service should return every stored goal.'''
    goal_one = Goal(goal_type="weekly_distance", target=25.0,)
    goal_two = Goal(goal_type="current_streak", target=7,) 

    service.create_goal(goal_one)
    service.create_goal(goal_two)

    goals = service.get_all_goals()

    assert len(goals) == 2


def test_get_goal_by_id(service):
    '''Service should return a goal by ID.'''
    goal = Goal(goal_type="weekly_distance", target=25.0,)
    service.create_goal(goal)
    found = service.get_goal_by_id(goal.id)

    assert found is not None
    assert found.id == goal.id

def test_get_goal_by_id_not_found(service):
    '''Service should return None when the goal does not exist.'''
    not_found = service.get_goal_by_id(uuid4())

    assert not_found is None

def test_update_goal(service):
    '''Service should update an existing goal.'''
    goal = Goal(goal_type="weekly_distance", target=25.0,)
    service.create_goal(goal)

    updated_goal = Goal(goal_type="weekly_distance", target=40.0,)
    
    result = service.update_goal(goal.id, updated_goal)

    assert result is not None
    assert result.id == goal.id
    assert result.target == 40.0

    loaded = service.get_goal_by_id(goal.id)

    assert loaded is not None
    assert loaded.goal_type == "weekly_distance"
    assert loaded.target == 40.0

def test_update_goal_not_found(service):
    '''Service should return None when updating a nonexistent goal.'''
    goal = Goal(goal_type="monthly_distance", target=50.0,)
    result = service.update_goal(uuid4(), goal)

    assert result is None

def test_delete_goal(service):
    '''Service should delete an existing goal.'''
    goal = Goal(goal_type="weekly_distance",target=25.0,)
    service.create_goal(goal)
    deleted = service.delete_goal(goal.id)

    assert deleted is True
    assert service.get_goal_by_id(goal.id) is None

def test_delete_goal_not_found(service):
    '''Service should return False when the goal does not exist.'''
    deleted = service.delete_goal(uuid4())

    assert deleted is False

def test_get_goal_progress_weekly_distance(service):
    '''Service should calculate progress for a weekly distance goal.'''
    goal = Goal(goal_type="weekly_distance", target=30.0)

    activities = [Activity("run", 10.0, 100), Activity("walk", 5.0, 60)]
    progress = service.get_goal_progress(goal, activities)

    assert progress == 15.0

def test_get_goal_progress_monthly_distance(service):
    '''Service should calculate progress for a monthly distance goal.'''
    goal = Goal(goal_type="monthly_distance", target=50.0)

    activities = [Activity("run", 10.0, 100), Activity("walk", 5.0, 60)]
    progress = service.get_goal_progress(goal, activities)

    assert progress == 15.0

def test_get_goal_progress_current_streak(service):
    """Service should calculate progress for a current streak goal."""
    goal = Goal(goal_type="current_streak", target=15.0)
    # today = datetime(2026, 9, 1)
    today = datetime.now()

    activities = [Activity("run", 3.0, 30.0,), Activity("run", 10.0, 100), Activity("walk", 5.0, 60)]
    activities[0].date = today
    activities[1].date = today - timedelta(days=1)
    activities[2].date = today - timedelta(days=2)

    progress = service.get_goal_progress(goal, activities)

    assert progress == 3

def test_goal_progress_current_streak_no_activity_today(service):
    '''Current streak should continue from yesterday if there is no activity today.'''
    goal = Goal(goal_type="current_streak", target=5,)
    today = datetime(2026, 8, 27)

    activities = [Activity("run", 3.0, 30.0), Activity("run", 3.0, 30.0), Activity("run", 3.0, 30.0)]

    activities[0].date = today - timedelta(days=1)
    activities[1].date = today - timedelta(days=2)
    activities[2].date = today - timedelta(days=3)

    progress = service.get_goal_progress(goal, activities, today)

    assert progress == 3

def test_goal_progress_current_streak_broken(service):
    '''Current streak should stop when there is a missing day.'''
    goal = Goal(goal_type="current_streak", target=5,)
    today = datetime(2026, 9, 1)
    # today = datetime.now()

    activities = [Activity("run", 3.0, 30.0), Activity("run", 3.0, 30.0), Activity("run", 3.0, 30.0)]

    activities[0].date = today
    activities[1].date = today - timedelta(days=1)
    activities[2].date = today - timedelta(days=3)

    progress = service.get_goal_progress(goal, activities, today)

    assert progress == 2

def test_get_goal_progress_longest_streak(service):
    """Service should calculate progress for a longest streak goal."""
    goal = Goal(goal_type="longest_streak", target=10.0)
    today = datetime(2026, 8, 27)

    a1 = Activity("run", 3.0, 30.0)
    a2 = Activity("walk", 3.0, 30.0)
    a3 = Activity("run", 3.0, 30.0)
    a4 = Activity("walk", 3.0, 30.0)
    a5 = Activity("run", 3.0, 30.0)
    a6 = Activity("walk", 3.0, 30.0)

    a1.date = today

    a2.date = today - timedelta(days=1)
    a3.date = today - timedelta(days=2)
    a4.date = today - timedelta(days=5)
    a5.date = today - timedelta(days=6)
    a6.date = today - timedelta(days=8)

    activities = [a1, a2, a3, a4, a5, a6]

    progress = service.get_goal_progress(goal, activities)

    assert progress == 3

def test_get_goal_percentage(service):
    '''Service should calculate goal completion percentage.'''
    goal = Goal(goal_type="weekly_distance", target=20.0)
    activites = [Activity(activity_type="walk", distance=10, duration=120), Activity(activity_type="run", distance=5, duration=50)]

    percentage = service.get_goal_percentage(goal, activites)

    assert percentage == 75

def test_is_goal_complete(service):
    '''Service should identify a completed goal.'''
    goal = Goal(goal_type="monthly_distance", target=20.0)
    activites = [Activity(activity_type="walk", distance=10, duration=120), Activity(activity_type="run", distance=5, duration=50), Activity(activity_type="walk", distance=5, duration=60)]

    complete = service.is_goal_complete(goal, activites)

    assert complete is True

def test_is_goal_complete_streak(service):
    '''Service should identify a completed streak goal.'''
    goal = Goal(goal_type="current_streak", target=3)
    # today = datetime(2026, 9, 1)
    today = datetime.now()

    activites = [Activity(activity_type="walk", distance=10, duration=120), Activity(activity_type="run", distance=5, duration=50), Activity(activity_type="walk", distance=5, duration=60)]
    activites[0].date = today
    activites[1].date = today - timedelta(days=1)
    activites[2].date = today - timedelta(days=2)
    

    complete = service.is_goal_complete(goal, activites)

    assert complete is True

def test_is_goal_complete_longest_streak(service):
    '''Service should identify a completed longest streak goal.'''
    goal = Goal(goal_type="longest_streak", target=3.0)
    today = datetime(2026, 8, 27)

    a1 = Activity("run", 3.0, 30.0)
    a2 = Activity("walk", 3.0, 30.0)
    a3 = Activity("run", 3.0, 30.0)
    a4 = Activity("walk", 3.0, 30.0)
    a5 = Activity("run", 3.0, 30.0)
    a6 = Activity("walk", 3.0, 30.0)

    a1.date = today

    a2.date = today - timedelta(days=1)
    a3.date = today - timedelta(days=2)
    a4.date = today - timedelta(days=5)
    a5.date = today - timedelta(days=6)
    a6.date = today - timedelta(days=8)

    activities = [a1, a2, a3, a4, a5, a6]

    complete = service.is_goal_complete(goal, activities)
    
    assert complete is True

def test_is_goal_complete_returns_false(service):
    '''Service should identify an incomplete goal.'''
    goal = Goal(goal_type="weekly_distance", target=20.0)
    activities = [Activity(activity_type="run", distance=10, duration=90)]

    complete = service.is_goal_complete(goal, activities)

    assert complete is False

if __name__ == "__main__":
    pytest.main([__file__])