import pytest
from app.models import Activity
from app.stats import (
    total_activities,
    total_distance,
    total_duration,
    average_pace,
    activity_counts
)

def test_total_activities():
    '''The total_activities function should successfuly return total number of activites'''
    activities = [Activity("run", 3.0, 30.0), Activity("walk", 2.0, 40.0),]
    activities_count = total_activities(activities)

    assert activities_count == 2

def test_total_distance():
    '''The total_distance function should successfuly return total distance for all activities'''
    activities = [Activity("run", 3.0, 30.0), Activity("walk", 2.0, 40.0),]

    assert total_distance(activities) == 5.0

def test_total_duration():
    '''The total_duration function should successfuly return total duration for all activities'''
    activities = [Activity("run", 3.0, 30.0), Activity("walk", 2.0, 40.0),]

    assert total_duration(activities) == 70.0

def test_average_pace():
    '''The average_pace function should succsessfully calculate the average pace of all activities'''
    activities = [Activity("run", 3.0, 30.0), Activity("walk", 2.0, 40.0),]

    # 10 min/mile and 20 min/mile
    # Average = 15 min/mile
    assert average_pace(activities) == 15.0

def test_average_pace_with_no_activities():
    '''The average_pace function should return None if activities array is empty'''
    activities = []

    assert average_pace(activities) == None 

def test_activity_counts():
    '''The activity_count function should accurately count the total number for each activity_type and return a dictionary with proper calculations'''
    activities = [Activity("run", 3.0, 30.0), Activity("run", 2.0, 20.0), Activity("walk", 2.0, 40.0),]

    # results = activity_counts(activities)
    # assert results["run"] == 2
    # assert results["walk"] == 1

    assert activity_counts(activities) == {
        "run": 2,
        "walk": 1,
    }

def test_activity_counts_with_no_activities():
    '''The activity_count function should accurately count the total number for each activity_type and return a dictionary with proper calculations even with empty arr'''
    assert activity_counts([]) == {
        "run": 0,
        "walk": 0,
    }
    
if __name__ == "main":
    pytest.main([__file__])