# Stores and retrieves information. SQLite only.
# External Library needed -> SQLite (belongs here only) 

from app.models import Activity
from uuid import UUID

class ActivityRepository:
    '''Handles persistence for Activity objects.'''
    def create_activity(self, activity: Activity) -> Activity:
        '''Save a new activity.'''
        pass

    def get_all_activities(self) -> list[Activity]:
        '''Return all stored activities.'''
        pass

    def get_activity_by_id(self, activity_id: UUID) -> Activity | None:
        '''Return a single activity by its ID.'''
        pass

    def update_activity( self, activity_id: UUID, updated_activity: Activity,) -> Activity | None:
        '''Replace an existing activity.'''
        pass

    def delete_activity(self, activity_id: UUID) -> bool:
        '''Delete an activity.'''
        pass