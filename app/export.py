# Handles exporting app data
# CSV only
import csv
from pathlib import Path
from app.models import Activity

def export_activities_to_csv(activities: list[Activity], filepath: str | Path) -> None:
    '''Export activities to a CSV file'''
    filepath = Path(filepath) # create a file path object from the inputted string

    with filepath.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file) # convert the data to str and write them into the file

        writer.writerow([
            "id",
            "activity_type",
            "distance",
            "duration",
            "notes",
            "route",
            "date",
        ])

        for activity in activities:
            writer.writerow([
                activity.id,
                activity.activity_type,
                activity.distance,
                activity.duration,
                activity.notes,
                activity.route,
                activity.date,
            ])