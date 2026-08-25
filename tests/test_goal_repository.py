import pytest
from app.database import ActivityRepository
from app.models import Goal
from uuid import uuid4

@pytest.fixture
def repo():
    repo = ActivityRepository(":memory:") # SQLite creates a temporary in-memory database that disappears after the test.
    yield repo # pause the fixture to run the test
    repo.close()

def test_create_goal(repo):
    '''Test Create Goal'''
    goal = Goal(goal_type="weekly_distance", target=25.0,)
    saved = repo.create_goal(goal)

    assert saved.id == goal.id

def test_get_all_goals(repo):
    ''''''
    goal1 = Goal(goal_type="weekly_distance", target=25.0,)
    goal2 = Goal(goal_type="current_streak", target=30,)

    repo.create_goal(goal1)
    repo.create_goal(goal2)
    result = repo.get_all_goals()

    assert len(result) == 2

def test_get_goal_by_id(repo):
    '''Test Get Goal By ID'''
    goal = Goal(goal_type="weekly_distance", target=25.0,)
    repo.create_goal(goal)
    result = repo.get_goal_by_id(goal.id)

    assert result is not None
    assert result.id == goal.id

def test_get_goal_by_id_not_found(repo):
    '''Test Goal Not Found'''
    result = repo.get_goal_by_id(uuid4())

    assert result is None

def test_update_goal(repo):
    '''Repository should successfully update existing goal'''
    goal = Goal(goal_type="weekly_distance", target=25.0,)
    repo.create_goal(goal)

    updated_goal = Goal(goal_type="weekly_distance", target=40.0,)
    
    result = repo.update_goal(goal.id, updated_goal)

    assert result is not None
    assert result.id == goal.id
    assert result.target == 40.0

    loaded = repo.get_goal_by_id(goal.id)

    assert loaded is not None
    assert loaded.goal_type == "weekly_distance"
    assert loaded.target == 40.0

def test_update_goal_not_found(repo):
    '''Updating a nonexistent goal should return None.'''
    goal = Goal(goal_type="monthly_distance", target=50.0,)
    result = repo.update_goal(uuid4(), goal)

    assert result is None

def test_delete_goal(repo):
    '''An existing goal should be deleted.'''
    goal = Goal(goal_type="weekly_distance",target=25.0,)
    repo.create_goal(goal)
    deleted = repo.delete_goal(goal.id)

    assert deleted is True
    assert repo.get_goal_by_id(goal.id) is None

def test_delete_goal_not_found(repo):
    '''Deleting a nonexistent goal should return False.'''
    deleted = repo.delete_goal(uuid4())

    assert deleted is False

if __name__ == "__main__":
    pytest.main([__file__])