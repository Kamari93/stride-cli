import csv 
import pytest

from app.models import Activity
from app.export import export_activities_to_csv

def test_export_activities_to_csv(tmp_path):
    """Activities should be exported to a CSV file."""
    activities = [
        Activity(activity_type="run", distance=3.0, duration=30.0, notes="Morning run", route="Park"),
        Activity(activity_type="walk", distance=2.0, duration=40.0,),
    ]

    filepath = tmp_path/"activities.csv"

    export_activities_to_csv(activities, filepath)

    assert filepath.exists()

    with filepath.open("r", newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file)) # make each row a dict

    assert len(rows) == 2

    assert rows[0]["activity_type"] == "run"
    assert rows[0]["distance"] == "3.0"
    assert rows[0]["duration"] == "30.0"
    assert rows[0]["notes"] == "Morning run"
    assert rows[0]["route"] == "Park"

    assert rows[1]["activity_type"] == "walk"
    assert rows[1]["distance"] == "2.0"
    assert rows[1]["duration"] == "40.0"

def test_export_empty_activites(tmp_path):
    '''Exporting no activities should create a CSV with headers only.'''
    filepath = tmp_path/"activities.csv"
    activities = []

    export_activities_to_csv(activities, filepath)

    assert filepath.exists()

    with filepath.open("r", newline="", encoding="utf-8") as file:
        rows = list(csv.reader(file)) # read spreadsheet line by line

    assert rows == [[
        "id",
        "activity_type",
        "distance",
        "duration",
        "notes",
        "route",
        "date",
    ]]

if __name__ == "__main__":
    pytest.main([__file__])