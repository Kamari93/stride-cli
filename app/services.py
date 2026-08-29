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
from app.models import Activity, Goal
from app.database import ActivityRepository
from uuid import UUID
from datetime import datetime

from app.stats import weekly_distance, monthly_distance, current_streak, longest_streak

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

class GoalService:
    '''Coordinates business logic for Goal objects.'''
    def __init__(self, repository: ActivityRepository) -> None:
        '''Initialize the service with an ActivityRepository.'''
        self.repository = repository

    def create_goal(self, goal: Goal) -> Goal:
        '''Save a new goal.'''
        return self.repository.create_goal(goal)

    def get_all_goals(self):
        '''Return every goal.'''
        return self.repository.get_all_goals()

    def get_goal_by_id(self, goal_id: UUID) -> Goal:
        '''Return a single goal by its ID.'''
        return self.repository.get_goal_by_id(goal_id)

    def update_goal(self, goal_id: UUID, updated_goal: Goal) -> Goal | None:
        '''Update an existing goal.'''
        return self.repository.update_goal(goal_id, updated_goal)

    def delete_goal(self, goal_id: UUID) -> bool:
        '''Delete an existing goal.'''
        return self.repository.delete_goal(goal_id)

    def get_goal_progress(self, goal: Goal, activities: list[Activity], today: datetime | None = None) -> float:
        '''Return the current progress toward a goal.'''
        if goal.goal_type == "weekly_distance":
            return weekly_distance(activities)
        if goal.goal_type == "monthly_distance":
            return monthly_distance(activities)
        if goal.goal_type == "current_streak":
            return current_streak(activities, today)
        if goal.goal_type == "longest_streak":
            return longest_streak(activities)

        raise ValueError(f"Unsupported goal type: {goal.goal_type}")

    def get_goal_percentage(self, goal: Goal, activities: list[Activity]) -> float:
        '''Return percentage of the goal completed.'''
        progress = self.get_goal_progress(goal, activities)

        return min((progress / goal.target) * 100, 100)

    def is_goal_complete(self, goal: Goal, activities: list[Activity]) ->bool:
        '''Return True if the goal has been completed.'''
        return self.get_goal_progress(goal, activities) >= goal.target