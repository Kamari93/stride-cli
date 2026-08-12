# Calculations only. Average pace, Weekly miles, Longest run, Streaks.
# External Library needed -> Plotext (belongs here only) 
from app.models import Activity

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

def activity_counts(activities: list[Activity]) -> dict[str, int]:
    '''Return the number of walks and runs.'''
    return {
        "walk": sum(1 for activity in activities if activity.activity_type == "walk"),
        "run": sum(1 for activity in activities if activity.activity_type == "run"), 
    }