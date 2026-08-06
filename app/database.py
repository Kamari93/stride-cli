# Stores and retrieves information. SQLite only.
# External Library needed -> SQLite (belongs here only) 

from app.models import Activity
from uuid import UUID
from datetime import datetime

import sqlite3
from pathlib import Path

class ActivityRepository:
    '''Handles persistence for Activity objects.'''
    '''Stores and retrieves Activity objects using SQLite.'''

    def __init__(self, db_path: str = "stride.db") -> None:
        '''The constructor opens the database and make sure the schema exists.'''
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row

        self.create_tables()

    def create_tables(self) -> None:
        '''Create database tables if they don't already exist.'''
        cursor = self.connection.cursor()

        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS activities (
                id TEXT PRIMARY KEY,
                activity_type TEXT NOT NULL,
                distance REAL NOT NULL,
                duration REAL NOT NULL,
                date TEXT NOT NULL,
                notes TEXT,
                route TEXT
            )

            '''
        )
        self.connection.commit()

    def close(self) -> None:
        '''Close the SQLite connection.'''
        self.connection.close()

    def create_activity(self, activity: Activity) -> Activity:
        '''Stores a new activity to the database.'''
        cursor = self.connection.cursor()

        cursor.execute(
            '''
            INSERT INTO activities (
                id,
                activity_type,
                distance,
                duration,
                date,
                notes,
                route
            )
            VALUES(?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                str(activity.id),
                activity.activity_type,
                activity.distance,
                activity.duration,
                activity.date.isoformat(),
                activity.notes,
                activity.route,
            ),
        )
        self.connection.commit()
        return activity

    def get_all_activities(self) -> list[Activity]:
        '''Return all stored activities.'''
        cursor = self.connection.cursor()
        cursor.execute(
            '''
            SELECT *
            FROM activities
            ORDER BY date DESC
            '''
        )

        rows = cursor.fetchall()

        return [self._row_to_activity(row) for row in rows]

    def get_activity_by_id(self, activity_id: UUID) -> Activity | None:
        '''Return a single activity by its ID.'''
        pass

    def update_activity( self, activity_id: UUID, updated_activity: Activity,) -> Activity | None:
        '''Replace an existing activity.'''
        pass

    def delete_activity(self, activity_id: UUID) -> bool:
        '''Delete an activity.'''
        pass

    def _row_to_activity(self, row: sqlite3.Row) -> Activity:
        '''Convert a SQLite row into an Activity object.'''
        activity = Activity(
            activity_type=row["activity_type"],
            distance=row["distance"],
            duration=row["duration"],
            notes=row["notes"],
            route=row["route"],
            )
        activity.id = UUID(row["id"])
        activity.date = datetime.fromisoformat(row["date"])

        return activity