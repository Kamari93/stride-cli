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
from .models import Activity
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
        for activity in self.activities:
            if activity.id == activity_id:
                return activity
        
        return None

    # ---------- Update ----------

    def update_activity( self, activity_id: UUID, **changes) -> Activity | None:
        """Update an existing activity."""
        pass

    # ---------- Delete ----------

    def delete_activity(self, activity_id: UUID) -> bool:
        """Delete an activity."""
        pass


    # ---------- Validation ----------

    def validate_activity(self, activity: Activity) -> bool:
        """Validate business rules.Returns True if the activity is valid.
        Raises ValueError if validation fails."""
        return True