# Starts the application.
from app.cli import CLI 
from app.services import ActivityService
from app.database import ActivityRepository

def main() -> None:
    repository = ActivityRepository()
    # activity_service = ActivityService()
    activity_service = ActivityService(repository)
    cli = CLI(activity_service)
    cli.run()


if __name__ == "__main__":
    main()