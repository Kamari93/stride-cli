# Calculations only. Average pace, Weekly miles, Longest run, Streaks.
# External Library needed -> Plotext (belongs here only) 
from app.models import Activity
from datetime import datetime, timedelta

def total_activities(activities: list[Activity]) -> int:
    '''Return the total number of activities.'''
    return len(activities)

def total_distance(activities: list[Activity]) -> float:
    '''Return the total distance across all activities.'''
    return sum(activity.distance for activity in activities)

def total_duration(activities: list[Activity]) -> float:
    '''Return the total duration across all activities.'''
    return sum(activity.duration for activity in activities)

def average_pace(activities: list[Activity]) -> float | None:
    '''Return the average pace across all activities.'''
    if not activities:
        return None

    return sum(activity.calculate_pace() for activity in activities) / len(activities)

def average_walk_pace(activities: list[Activity]) -> float | None:
    '''Return the average pace for all walk activities.'''
    walks = [activity for activity in activities if activity.activity_type == "walk"]

    if not walks:
        return None

    return sum(activity.calculate_pace() for activity in walks) / len(walks)

def average_run_pace(activities: list[Activity]) -> float | None:
    '''Return the average pace for all run activities.'''
    runs = [activity for activity in activities if activity.activity_type == "run"]

    if not runs:
        return None

    return sum(activity.calculate_pace() for activity in runs) / len(runs)

def activity_counts(activities: list[Activity]) -> dict[str, int]:
    '''Return the number of walks and runs.'''
    return {
        "walk": sum(1 for activity in activities if activity.activity_type == "walk"),
        "run": sum(1 for activity in activities if activity.activity_type == "run"), 
    }

def longest_activity(activities: list[Activity]) -> Activity | None:
    '''Return the activity with the greatest distance.'''
    if not activities:
        return None

    return max(activities, key=lambda activity: activity.distance,)

def longest_run(activities: list[Activity]) -> Activity | None:
    '''Return the longest run.'''
    runs = [activity for activity in activities if activity.activity_type == "run"]
    if not runs:
        return None

    return max(runs, key=lambda activity: activity.distance)

def longest_walk(activities: list[Activity]) -> Activity | None:
    '''Return the longest walk.'''
    walks = [activity for activity in activities if activity.activity_type == "walk"]
    if not walks:
        return None

    return max(walks, key=lambda activity: activity.distance)

def fastest_pace(activities: list[Activity],) -> Activity | None:
    '''Return the activity with the fastest pace.'''
    if not activities:
        return None

    return min(activities, key=lambda activity: activity.calculate_pace())

def fastest_walk_pace(activities: list[Activity],) -> Activity | None:
    '''Return the walk activity with the fastest pace'''
    walks = [activity for activity in activities if activity.activity_type == "walk"]

    if not walks:
        return None

    return min(walks, key=lambda activity: activity.calculate_pace())

def fastest_run_pace(activities: list[Activity],) -> Activity | None:
    '''Return the run activity with the fastest pace'''
    runs = [activity for activity in activities if activity.activity_type == "run"]
    if not runs:
        return None

    return min(runs, key=lambda activity: activity.calculate_pace())

def weekly_distance(activities: list[Activity], today: datetime | None = None,) -> float:
    '''Return distance logged during the current week.'''
    if not activities:
        return 0.0

    # date from one week ago
    cutoff = datetime.now() - timedelta(days=7)

    # add up the distance for every activity that happened on or after cutoff date.
    return sum(activity.distance for activity in activities if activity.date >= cutoff)

def monthly_distance(activities: list[Activity], today: datetime | None = None,) -> float:
    '''Return distance logged during the current month.'''
    if not activities:
        return 0.0

    # date from one month ago
    cutoff = datetime.now() - timedelta(days=30)
    
    # add up the distance for every activity that happened on or after cutoff date.
    return sum(activity.distance for activity in activities if activity.date >= cutoff)

def current_streak(activities: list[Activity], today: datetime | None = None,) -> int:
    '''Return the current activity streak in days.'''
    if not activities:
        return 0.0

    today = today or datetime.now()
    activity_dates = {activity.date.date() for activity in activities}

    current_day = today.date()

     # If no activity today, check if they had one yesterday
    if current_day not in activity_dates:
        current_day -= timedelta(days=1)
        if current_day not in activity_dates:
            return 0

    # Count the streak backwards from the valid starting day
    streak = 0
    while current_day in activity_dates:
        streak += 1
        current_day -= timedelta(days=1)

    return streak

def longest_streak(activities: list[Activity]) -> int:
    '''Return the longest activity streak.'''
    if not activities:
        return 0.0

    dates = sorted({activity.date.date() for activity in activities})

    current = 1
    longest = 1

    for i in range(len(dates)):
        difference = (dates[i] - dates[i - 1]).days

        if difference == 1:
            current += 1
            longest = max(current, longest)
        else:
            current = 1

    return longest