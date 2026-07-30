import pytest
from app.models import Activity

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

if __name__ == "__main__":
    pytest.main([__file__])