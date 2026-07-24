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
from uuid import UUID

class ActivityService:
    """Coordinates business logic for Activity objects."""

    def __init__(self) -> None:
        """Initialize the service with temporary in-memory storage."""
        self.activities: list[Activity] = []
    

    # ---------- Create ----------

    def create_activity(self, activity: Activity) -> Activity:
        """Validate and save a new activity."""
        self.validate_activity(activity)
        self.activities.append(activity)
        return activity

    # ---------- Read ----------

    def get_all_activities(self) -> list[Activity]:
        """Return every activity."""
        return self.activities

    def get_activity_by_id(self, activity_id: UUID) -> Activity | None:
        """Return a single activity by its ID."""
        # for activity in self.activities:
        #     if activity.id == activity_id:
        #         return activity
        # return None

        result = self._find_activity(activity_id)

        if result is None:
            return None

        _, activity = result # decouple and extract activity ignore id as we don't need for this fn

        return activity
        

    # ---------- Update ----------

    def update_activity( self, activity_id: UUID, **changes) -> Activity | None:
        """Update an existing activity."""
        activity = self.get_activity_by_id(activity_id)

        # activity not found
        if not activity:
            return None 
        
        for key, val in changes.items():
            if hasattr(activity, key):
                setattr(activity, key, val)
        
        return activity

    # ---------- Delete ----------

    def delete_activity(self, activity_id: UUID) -> bool:
        """Delete an activity."""
        for index, activity in enumerate(self.activities):
            if activity.id == activity_id:
                self.activities.pop(index)
                return True
        
        return False

    # ---------- Find Activity Private Helper ----------
    def _find_activity(self, activity_id: UUID) -> tuple[int, Activity] | None:
        '''Return the index and Activity for the given ID. Returns None if the activity is not found.'''
        for idx, activity in enumerate(self.activities):
            if activity.id == activity_id:
                return idx, activity
        
        return None

    # ---------- Validation ----------

    def validate_activity(self, activity: Activity) -> bool:
        """Validate business rules. Returns True if the activity is valid.
        Raises ValueError if validation fails."""
        return True