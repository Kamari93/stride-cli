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
if __name__ == "__main__":
    pytest.main([__file__])