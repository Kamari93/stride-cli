import pytest
from app.models import Activity
from datetime import datetime, timedelta
from app.stats import (
    total_activities,
    total_distance,
    total_duration,
    average_pace,
    activity_counts,
    longest_activity,
    longest_run,
    longest_walk,
    fastest_pace,
    weekly_distance,
    monthly_distance,
    current_streak,
    longest_streak,
    average_walk_pace,
    average_run_pace,
    fastest_walk_pace,
    fastest_run_pace,
    weekly_distance_history,
    monthly_distance_history,
    activity_distance_history,
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

def test_average_walk_pace():
    '''The average_walk_pace function should succsessfully calculate the average pace of all walk activities'''
    activities = [Activity("run", 3.0, 30.0), Activity("walk", 2.0, 40.0), Activity("walk", 3.0, 30.0)]

    # 10 min/mile and 20 min/mile
    # Average = 15 min/mile
    assert average_walk_pace(activities) == 15.0

def test_average_walk_pace_with_no_activities():
    '''The average_walk_pace function should return None if activities array is empty'''
    activities = []

    assert average_walk_pace(activities) is None

def test_average_run_pace():
    '''The average_run_pace function should succsessfully calculate the average pace of all walk activities'''
    activities = [Activity("run", 3.0, 30.0), Activity("run", 2.0, 40.0), Activity("walk", 3.0, 30.0)]

    # 10 min/mile and 20 min/mile
    # Average = 15 min/mile
    assert average_run_pace(activities) == 15.0

def test_average_run_pace_with_no_activities():
    '''The average_run_pace function should return None if activities array is empty'''
    activities = []

    assert average_run_pace(activities) is None

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

def test_longest_activity():
    '''The longest_activity should return the stored activity with the longest recorded distance'''
    activities = [Activity("run", 3.0, 30.0), Activity("walk", 5.0, 80.0), Activity("run", 2.0, 20.0),]
    result = longest_activity(activities)

    assert result is not None
    assert result.distance == 5.0

def test_longest_empty():
    '''The longest_activity should return None if activities is empty'''
    result = longest_activity([])

    assert result is None

def test_longest_run():
    '''The longest_run should return the run activity with longest distance'''
    activities = activities = [Activity("run", 3.0, 30.0), Activity("run", 6.0, 60.0), Activity("walk", 8.0, 120.0),]
    result = longest_run(activities)

    assert result is not None
    assert result.distance == 6.0

def test_longest_run_none():
    '''The longest_run should return None if there are no run activities in the activities list'''
    activities = [Activity("walk", 2.0, 40.0), Activity("walk", 3.0, 50.0),]
    result = longest_run(activities)

    assert result is None

def test_longest_walk():
    '''The longest_walk should return the walk activity with longest distance'''
    activities = [Activity("walk", 2.0, 40.0), Activity("walk", 5.0, 90.0), Activity("run", 8.0, 80.0),]
    result = longest_walk(activities)

    assert result is not None
    assert result.distance == 5.0

def test_longest_run_none():
    '''The longest_walk should return None if there are no walk activities in the activities list'''
    activities = [Activity("run", 3.0, 30.0), Activity("run", 4.0, 40.0),]
    result = longest_walk(activities)

    assert result is None

def test_fastest_pace():
    '''The fastest_pace should return the activity with the fastest pace'''
    activities = [
        Activity("run", 3.0, 30.0),  # 10 min/mi
        Activity("run", 4.0, 32.0),  # 8 min/mi
        Activity("walk", 2.0, 40.0), # 20 min/mi
        ]
    result = fastest_pace(activities)

    assert result is not None
    assert result.calculate_pace() == 8.0

def test_fastest_pace_empty():
    '''The fastest_pace should return None if the activity list is empty'''
    assert fastest_pace([]) is None

def test_fastest_walk_pace():
    '''The fastest_walk_pace should return the walk activity with the fastest pace'''
    activities = [
        Activity("run", 3.0, 30.0),  # 10 min/mi
        Activity("run", 4.0, 32.0),  # 8 min/mi
        Activity("walk", 2.0, 40.0), # 20 min/mi
        Activity("walk", 2.0, 30.0), # 15 min/mi
        ]
    result = fastest_walk_pace(activities)

    assert result is not None
    assert result.calculate_pace() == 15.0

def test_fastest_walk_pace_empty():
    '''The fastest_walk_pace should return None if the activity list is empty'''
    assert fastest_walk_pace([]) is None

def test_fastest_run_pace():
    '''The fastest_run_pace should return the run activity with the fastest pace'''
    activities = [
        Activity("run", 3.0, 21.0),  # 7 min/mi
        Activity("run", 4.0, 32.0),  # 8 min/mi
        Activity("walk", 2.0, 40.0), # 20 min/mi
        Activity("walk", 2.0, 30.0), # 15 min/mi
        ]
    result = fastest_run_pace(activities)

    assert result is not None
    assert result.calculate_pace() == 7.0

def test_fastest_run_pace_empty():
    '''The fastest_run_pace should return None if the activity list is empty'''
    assert fastest_run_pace([]) is None

def test_weekly_distance():
    '''The weekly_distance should sum up the activity distance for the last 7 days'''
    recent = Activity(activity_type="run", distance=3.0, duration=30,)
    older = Activity(activity_type="walk", distance=5.0, duration=60,)
    older.date = datetime.now() - timedelta(days=10)

    result = weekly_distance([recent, older])

    assert result == 3.0

def test_weekly_distance_uses_calendar_week():
    '''The weekly_distance should sum up the activity distance for the current week'''
    today = datetime(2026, 9, 9) # Wednesday

    monday = Activity("run", 5.0, 50)
    tuesday = Activity("walk", 3.0, 40)
    wednesday = Activity("run", 4.0, 40)
    sunday_before = Activity("walk", 10.0, 100)

    activities = [monday, tuesday, wednesday, sunday_before]

    activities[0].date = datetime(2026, 9, 7)
    activities[1].date = datetime(2026, 9, 8)
    activities[2].date = datetime(2026, 9, 9)
    activities[3].date = datetime(2026, 9, 6)

    assert weekly_distance(activities, today) == 12.0

def test_weekly_distance_empty():
    '''The weekly_distance should return 0 if there were no activities recorded for the last 7 days'''
    most_recent = Activity(activity_type="run", distance=3.0, duration=30,)
    older = Activity(activity_type="walk", distance=5.0, duration=60,)
    most_recent.date = datetime.now() - timedelta(days=9)
    older.date = datetime.now() - timedelta(days=10)

    result = weekly_distance([most_recent, older])

    assert result == 0

def test_weekly_distance_empty_no_data():
    '''The weekly_distance should return 0 if the activities list is empty'''
    assert weekly_distance([]) == 0.0


def test_monthly_distance():
    '''The monthly_distance should sum up the activity distance for the last 30 days'''
    recent = Activity(activity_type="run", distance=4.0, duration=40,)
    older = Activity(activity_type="walk", distance=10.0, duration=100,)
    older.date = datetime.now() - timedelta(days=45)

    result = monthly_distance([recent, older])

    assert result == 4.0

def test_monthly_distance_uses_calendar_month():
    '''The monthly_distance should sum up the activity distance for the current calendar month'''
    today = datetime(2026, 9, 8)

    activities = [
        Activity("run", 5.0, 50, datetime(2026, 8, 31)),
        Activity("walk", 3.0, 40, datetime(2026, 9, 1)),
        Activity("run", 4.0, 40, datetime(2026, 9, 8)),
        Activity("walk", 10.0, 100, datetime(2026, 10, 1)),
    ]

    # activities[0].date = datetime(2026, 8, 31)
    # activities[1].date = datetime(2026, 9, 1)
    # activities[2].date = datetime(2026, 9, 8)
    # activities[3].date = datetime(2026, 10, 1)

    result = monthly_distance(activities, today)

    assert result == 7.0

def test_monthly_distance_empty():
    '''The monthly_distance should return 0 if there were no activities recorded for the last 30 days'''
    most_recent = Activity(activity_type="run", distance=4.0, duration=40,)
    older = Activity(activity_type="walk", distance=10.0, duration=100,)
    most_recent.date = datetime.now() - timedelta(days=31)
    older.date = datetime.now() - timedelta(days=45)

    result = monthly_distance([most_recent, older])

    assert result == 0

def test_monthly_distance_empty_no_data():
    '''The monthly_distance should return 0 if the activities list is empty'''
    assert monthly_distance([]) == 0.0

def test_current_streak():
    '''The current_streak should return the current streak if activities are consecutive'''
    today = datetime.now()

    a1 = Activity("run", 3.0, 30.0)
    a2 = Activity("walk", 2.0, 40.0)
    a3 = Activity("run", 4.0, 32.0)

    a1.date = today
    a2.date = today - timedelta(days=1)
    a3.date = today - timedelta(days=2)

    result = current_streak([a1, a2, a3])

    assert result == 3

def test_current_streak_II():
    '''The current_streak should return the current streak for activities that are consecutive'''
    today = datetime.now()

    a1 = Activity("run", 3.0, 30.0)
    a2 = Activity("run", 3.0, 30.0)
    a3 = Activity("run", 3.0, 30.0)
    a4 = Activity("run", 3.0, 30.0)
    a5 = Activity("run", 3.0, 30.0)

    a1.date = today

    a2.date = today - timedelta(days=1)
    a3.date = today - timedelta(days=2)
    a4.date = today - timedelta(days=5)
    a5.date = today - timedelta(days=6)

    assert current_streak([a1, a2, a3, a4, a5]) == 3

def test_current_streak_broken():
    '''If the streak is broken due to activities not be consecutive current_streak should return 0'''
    today = datetime.now()

    activity = Activity("run", 3.0, 30.0)
    activity.date = today - timedelta(days=3)

    assert current_streak([activity]) == 0

def test_current_streak_from_yesterday():
    '''If the user hasn't logged in activity yet but has a streak going from previous day streak should stay active'''
    today = datetime.now()

    a1 = Activity("run", 3.0, 30.0)
    a2 = Activity("walk", 2.0, 40.0)
    a3 = Activity("run", 4.0, 32.0)

    a1.date = today - timedelta(days=1)
    a2.date = today - timedelta(days=2)
    a3.date = today - timedelta(days=3)

    result = current_streak([a1, a2, a3])

    assert result == 3

def test_longest_streak():
    '''The longest_streak should check the entire activities list and return the longest streak for all activities'''
    today = datetime.now()
    
    a1 = Activity("run", 3.0, 30.0)
    a2 = Activity("run", 3.0, 30.0)
    a3 = Activity("run", 3.0, 30.0)
    a4 = Activity("run", 3.0, 30.0)
    a5 = Activity("run", 3.0, 30.0)
    a6 = Activity("run", 3.0, 30.0)

    a1.date = today

    a2.date = today - timedelta(days=1)
    a3.date = today - timedelta(days=2)
    a4.date = today - timedelta(days=5)
    a5.date = today - timedelta(days=6)
    a6.date = today - timedelta(days=8)

    assert longest_streak([a1, a2, a3, a4, a5, a6]) == 3

def test_longest_streak_empty():
    '''longest_streak should return 0 if activities list is empty'''
    assert longest_streak([]) == 0

def test_weekly_distance_history():
    '''weekly_distance_history should return list of tuples for total distance for each week based on weeks param'''
    today = datetime(2026, 9, 9)

    activities = [
        Activity("run", 5.0, 50, datetime(2026, 8, 24)), 
        Activity("walk", 3.0, 40, datetime(2026, 9, 1)), 
        Activity("run", 4.0, 40, datetime(2026, 9, 8))
        ]
    result = weekly_distance_history(activities, weeks=3, today=today)

    assert result == [
        ("Aug 24", 5.0),
        ("Aug 31", 3.0),
        ("Sep 07", 4.0),
    ]

def test_monthly_distance_history():
    '''monthly_distance_history should return list of tuples for total distance for each month based on weeks param'''
    today = datetime(2026, 9, 9)

    activities = [
        Activity("run", 5.0, 50, datetime(2026, 7, 15)),
        Activity("walk", 3.0, 40, datetime(2026, 8, 10)),
        Activity("run", 4.0, 40, datetime(2026, 9, 8)),
    ]

    result = monthly_distance_history(activities, months=3, today=today)

    assert result == [
        ("Jul 2026", 5.0),
        ("Aug 2026", 3.0),
        ("Sep 2026", 4.0),
    ]

def test_activity_distance_history():
    '''test_activity_distance_history should return activity dates and distances in chronological order'''
    activities = [
        Activity("run", 4.0, 40, datetime(2026, 9, 5)),
        Activity("walk", 2.5, 30, datetime(2026, 9, 1)),
        Activity("run", 3.2, 35, datetime(2026, 9, 3))
    ]

    result = activity_distance_history(activities)

    assert result == [
        ("Sep 01", 2.5),
        ("Sep 03", 3.2),
        ("Sep 05", 4.0),
    ]


if __name__ == "main":
    pytest.main([__file__])