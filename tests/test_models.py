import pytest
from uuid import UUID
from app.models import Activity, Goal

'''The model is responsible for validation and behavior'''

def test_create_valid_activity():
    '''A valid Activity should be created successfully.'''
    activity = Activity(activity_type="run", distance=3.2, duration=30, notes="Morning run")
    assert activity.activity_type == "run"
    assert activity.distance == 3.2
    assert activity.duration == 30
    assert activity.notes == "Morning run"

def test_negative_distance_raises_value_error():
    '''Distance must be greater than zero.'''
    with pytest.raises(ValueError):
        Activity(activity_type="walk", distance=-1, duration=30)

def test_zero_distance_raises_value_error():
    '''Distance cannot be zero.'''
    with pytest.raises(ValueError):
        Activity(activity_type="walk", distance=0, duration=30)

def test_negative_duration_raises_value_error():
    '''Duration must be greater than zero.'''
    with pytest.raises(ValueError):
        Activity(activity_type="walk", distance=1.5, duration=-10)

def test_zero_duration_raises_value_error():
    '''Duration cannot be zero.'''
    with pytest.raises(ValueError):
        Activity(activity_type="walk", distance=1.5, duration=0)

def test_invalid_activity_type():
    '''Only walk and run are valid activity types.'''
    with pytest.raises(ValueError):
        Activity(activity_type="bike", distance=5,duration=35)

def test_calculate_pace():
    '''Pace should be minutes per mile.'''
    activity = Activity(activity_type="run", distance=4, duration=32, notes="pace test")
    assert activity.calculate_pace() == 8.0

def test_to_dict():
    '''Activity should convert itself to a dictionary.'''
    activity = Activity(activity_type="walk", distance=2.5, duration=40, notes="Evening walk")

    data = activity.to_dict()

    assert data['activity_type'] == "walk"
    assert data['distance'] == 2.5
    assert data["duration"] == 40
    assert data["notes"] == "Evening walk"
    assert "id" in data
    assert "date" in data

def test_str_returns_readable_string():
    '''__str__ should return a friendly string.'''
    activity = Activity(activity_type="run", distance=3, duration=30, notes="Tempo")

    # result = activity.__str__()
    result = str(activity)

    assert "Run" in result
    assert "3.0 mi" in result
    assert "30 min" in result
    assert "Tempo" in result


'''Tests for Goals'''
def test_create_goal():
    '''test goal creation'''
    goal = Goal(goal_type="weekly_distance", target=25.0,)

    assert goal.goal_type == "weekly_distance"
    assert goal.target == 25.0

def test_goal_invalid_type():
    '''Test Invalid Goal Type'''
    with pytest.raises(ValueError):
        Goal(goal_type="speed_distance", target=25.0,)
        
def test_goal_invalid_target():
    '''Test Invalid Target'''
    with pytest.raises(ValueError):
        Goal(goal_type="speed_distance", target=0,)

def test_goal_generate_id():
    '''Test Goal Generates UUID'''
    goal = Goal(goal_type="weekly_distance", target=25.0)

    assert isinstance(goal.id, UUID)

def test_goal_str():
    '''Test Goal String Representation'''
    goal = Goal(goal_type="weekly_distance", target=25.0)

    assert str(goal) == "Weekly Distance Goal: 25.0"

def test_goal_to_dict():
    '''Test Goal to_dict'''
    goal = Goal(goal_type="monthly_distance", target=100.0)

    data = goal.to_dict()

    assert data["goal_type"] == "monthly_distance"
    assert data["target"] == 100.0
    assert "id" in data
    
if __name__ == "__main__":
    pytest.main([__file__])