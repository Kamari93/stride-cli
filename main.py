# Starts the application.
from app.cli import CLI 
from app.services import ActivityService

def main() -> None:
    activity_service = ActivityService()
    cli = CLI(activity_service)
    cli.run()


if __name__ == "__main__":
    main()