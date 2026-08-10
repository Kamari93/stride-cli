# The orchestrator of the application.
# The service layer is the glue that keeps the CLI and database from becoming tightly coupled.
# Services are usually verbs.

# Responsibilities
#
# - Create activities
# - Retrieve activities
# - Update activities
# - Delete activities
# - Validate business rules
# - Coordinate communication between the CLI and the database
#
# Does NOT:
# - Display menus
# - Execute SQL
# - Store application state

# Keep the service from having to know every field individually.
from app.models import Activity
from app.database import ActivityRepository
from uuid import UUID

class ActivityService:
    """Coordinates business logic for Activity objects."""

    # def __init__(self) -> None:
    #     """Initialize the service with temporary in-memory storage."""
    #     self.activities: list[Activity] = []
    
    def __init__(self, repository: ActivityRepository) -> None:
        '''Initialize the service with an ActivityRepository.'''
        self.repository = repository

    # ---------- Create ----------

    def create_activity(self, activity: Activity) -> Activity:
        """Validate and save a new activity."""
        self.validate_activity(activity)
        return self.repository.create_activity(activity)
        # self.activities.append(activity)
        # return activity

    # ---------- Read ----------

    def get_all_activities(self) -> list[Activity]:
        """Return every activity."""
        # return self.activities
        return self.repository.get_all_activities()
    
    def get_activity_by_id(self, activity_id: UUID) -> Activity | None:
        """Return a single activity by its ID."""
        return self.repository.get_activity_by_id(activity_id)
    
        # for activity in self.activities:
        #     if activity.id == activity_id:
        #         return activity
        # return None

        # result = self._find_activity(activity_id)

        # if result is None:
        #     return None

        # _, activity = result # decouple and extract activity ignore id as we don't need for this fn

        # return activity
        

    # ---------- Update ----------

    # def update_activity( self, activity_id: UUID, **changes) -> Activity | None:
    #     """Update an existing activity."""
    #     activity = self.get_activity_by_id(activity_id)

    #     # activity not found
    #     if not activity:
    #         return None 
        
    #     for key, val in changes.items():
    #         if hasattr(activity, key):
    #             setattr(activity, key, val)
        
    #     return activity
    
    def update_activity(self, activity_id: UUID, updated_activity: Activity) -> Activity | None:
        """Replace an existing activity."""
        existing = self.repository.get_activity_by_id(activity_id)

        if existing is None:
            return None

        updated_activity.id = existing.id
        updated_activity.date = existing.date

        self.validate_activity(updated_activity)
        
        return self.repository.update_activity(activity_id, updated_activity)
        # result = self._find_activity(activity_id)

        # if result is None:
        #     return None

        # idx, old_activity = result

        # updated_activity.id = old_activity.id
        # updated_activity.date = old_activity.date

        # self.activities[idx] = updated_activity

        # return updated_activity

    # ---------- Delete ----------

    def delete_activity(self, activity_id: UUID) -> bool:
        """Delete an activity."""
        return self.repository.delete_activity(activity_id)
        # for index, activity in enumerate(self.activities):
        #     if activity.id == activity_id:
        #         self.activities.pop(index)
        #         return True
        # return False

        # result = self._find_activity(activity_id)

        # if result is None:
        #     return False

        # idx, _ = result

        # self.activities.pop(idx)

        # return True

    # ---------- Find Activity Private Helper ----------
    # def _find_activity(self, activity_id: UUID) -> tuple[int, Activity] | None:
    #     '''Return the index and Activity for the given ID. Returns None if the activity is not found.'''
    #     for idx, activity in enumerate(self.activities):
    #         if activity.id == activity_id:
    #             return idx, activity
        
    #     return None

    # ---------- Validation ----------

    def validate_activity(self, activity: Activity) -> bool:
        """Validate business rules. Returns True if the activity is valid.
        Raises ValueError if validation fails."""
        return True