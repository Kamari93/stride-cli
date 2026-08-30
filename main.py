# Starts the application.
from app.cli import CLI 
from app.services import ActivityService, GoalService
from app.database import ActivityRepository

def main() -> None:
    repository = ActivityRepository()
    # activity_service = ActivityService()
    activity_service = ActivityService(repository)
    goal_service = GoalService(repository)
    cli = CLI(activity_service, goal_service)
    cli.run()


if __name__ == "__main__":
    main()