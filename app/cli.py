# Everything related to menus. No database code. No statistics. Just interacting with the user.
# External Library needed -> Rich (belongs here only) 
# follow single responsibility principle and loose coupling
from rich.console import Console
from rich.panel import Panel 
from rich.prompt import Prompt

from app.models import Activity
from app.services import ActivityService

class CLI:
    '''Handles all user interactions.'''
    def __init__(self, activity_service: ActivityService) -> None:
        self.console = Console()
        self.activity_service = activity_service
        self.running = True
    
    def run(self) -> None:
        '''Main app loop'''
        self.show_welcome()

        while self.running:
            self.show_main_menu()
            choice = self.get_menu_choice()
            self.handle_menu_choice(choice)
    
    def show_welcome(self) -> None:
        '''Display app title.'''
        panel = Panel.fit(
            "[bold cyan]🏁 Welcome to Stride CLI!🏁[/bold cyan]\n"
            "Track your walks and runs from the terminal.",
            title="Stride CLI",
        )
        self.console.print(panel)

    def show_main_menu(self) -> None:
        '''Display the main menu.'''
        self.console.print("\n[bold]Main Menu[/bold]")
        self.console.print("1. Log Activity")
        self.console.print("2. View Activities")
        self.console.print("3. Exit")

    def get_menu_choice(self) -> str:
        '''Prompt the user for a menu selection.'''
        return Prompt.ask(
            "Choose an option",
            choices = ["1", "2", "3"],
        )

    def handle_menu_choice(self, choice) -> None:
        '''Route the user's choice to the appropriate feature.'''
        if choice == "1":
            self.log_activity()
        
        elif choice == "2":
            self.show_activities()

        elif choice == "3":
            self.exit()

    def log_activity(self) -> None:
        '''Display the Log Activity screen.'''
        self.console.print("\n[bold]Log Activity[/bold]")

        activity_type = Prompt.ask(
            "Activity Type",
            choices=["walk", "run"],
        )

        distance = float(Prompt.ask("Distance (miles)"))
        duration = float(Prompt.ask("Duration (minutes)"))

        notes = Prompt.ask(
            "Notes (optional)",
            default = "",
        )

        activity = Activity(
            activity_type = activity_type,
            distance = distance,
            duration = duration,
            notes = notes or None,
        )

        self.activity_service.create_activity(activity)

        self.console.print("[green]✓ Activity logged successfully![/green]")

    def show_activities(self) -> None:
        '''Display all recorded activities.'''
        self.console.print("\n[bold]Activities[/bold]")

        activities = self.activity_service.get_all_activities()

        if not activities:
            self.console.print("[yellow]No activities logged yet.[/yellow]")
            return
        
        for activity in activities:
            self.console.print(activity)

    def show_statistics(self):
        '''Display activity statistics.'''
        pass

    def show_goals(self):
        '''Display goal information.'''
        pass

    def show_error(self, msg):
        '''Display an error message.'''
        pass

    def show_success(self, msg):
        '''Display a success message.'''
        pass

    def exit(self) -> None:
        '''Exit the app.'''
        self.console.print("\nGoodbye!")
        self.running = False