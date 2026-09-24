# Starts the application.
from app.cli import CLI 
from app.weather import Weather_Service, OpenMeteoProvider
from app.services import ActivityService, GoalService
from app.database import ActivityRepository

def main() -> None:
    repository = ActivityRepository()
    # activity_service = ActivityService()
    activity_service = ActivityService(repository)
    goal_service = GoalService(repository)
    weather_provider = OpenMeteoProvider()
    weather_service = Weather_Service(weather_provider)
    cli = CLI(activity_service, goal_service, weather_service)
    cli.run()


if __name__ == "__main__":
    main()