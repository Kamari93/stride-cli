"""Tests for the GoalService."""
import pytest
from uuid import uuid4
from app.models import Goal
from app.services import GoalService
from app.database import ActivityRepository

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

if __name__ == "__main__":
    pytest.main([__file__])