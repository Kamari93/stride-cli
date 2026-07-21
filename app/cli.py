# Everything related to menus. No database code. No statistics. Just interacting with the user.
# External Library needed -> Rich (belongs here only) 
# follow single responsibility principle and loose coupling
from rich.console import Console
from rich.panel import Panel 
from rich.prompt import Prompt
from rich.table import Table
from rich import box

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

    def handle_menu_choice(self, choice: str) -> None:
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

        # distance = float(Prompt.ask("Distance (miles)"))
        # duration = float(Prompt.ask("Duration (minutes)"))

        distance = self.prompt_for_float("Distance (miles)")
        duration = self.prompt_for_float("Duration (minutes)")

        notes = Prompt.ask(
            "Notes (optional)",
            default = "",
        )
        try:
            activity = Activity(
                activity_type = activity_type,
                distance = distance,
                duration = duration,
                notes = notes or None,
            )

            self.activity_service.create_activity(activity)
        except ValueError as e:
            self.show_error(str(e))
            return
        
        # self.console.print("[green]✓ Activity logged successfully![/green]")
        self.show_success("Activity logged successfully!")
        self.pause()
        

    def show_activities(self) -> None:
        '''Display all recorded activities.'''
        # self.console.print("\n[bold]Activities[/bold]")

        activities = self.activity_service.get_all_activities()

        if not activities:
            self.console.print("[yellow]No activities logged yet.[/yellow]")
            return
        
        table = Table(show_header=True, title="Activities", header_style="bold green", box=box.ROUNDED)
        table.add_column("Type")
        table.add_column("Distance")
        table.add_column("Duration")
        table.add_column("Pace")
        table.add_column("Notes")
        table.add_column("Date")
        

        # for activity in activities:
        #     self.console.print(str(activity))

        for activity in activities:
            table.add_row(
                f"{activity.activity_type.title()}",
                f"{activity.distance:.1f} mi",
                f"{activity.duration:.0f} min",
                f"{activity.calculate_pace():.1f} min/mi",
                f"{activity.notes or "-"}",
                f"{activity.date}",
            )
        self.console.print("\n")
        self.console.print(table)
        self.pause()

    def show_statistics(self) -> None:
        '''Display activity statistics.'''
        pass

    def show_goals(self) -> None:
        '''Display goal information.'''
        pass

    def show_error(self, msg: str) -> None:
        '''Display an error message.'''
        self.console.print(f"[bold red]x {msg}[/bold red]")

    def show_success(self, msg: str) -> None:
        '''Display a success message.'''
        self.console.print(f"[bold green]✓ {msg}[/bold green]")

    def prompt_for_float(self, prompt: str) -> float:
        '''Prompt until the user enters a valid number.'''
        while True:
            try:
                return float(Prompt.ask(prompt))
            except:
                self.show_error("Please enter a valid number.")
    
    def prompt_for_int(self, prompt: str) -> int:
        '''Prompt until the user enters a valid integer.'''
        while True:
            try:
                return int(Prompt.ask(prompt))
            except:
                self.show_error("Please enter a valid integer.")

    def prompt_for_optional_text(self, prompt: str) -> str | None:
        '''Prompt the user for text. Returns None if the user leaves it blank.'''
        while True:
            try:
                input = Prompt.ask(prompt).strip()
                return input if input else None

            except:
                self.show_error("Please enter a valid text input.")
    
    def pause(self) -> None:
        Prompt.ask("\nPress Enter to continue")

    def exit(self) -> None:
        '''Exit the app.'''
        self.console.print("\nGoodbye!")
        self.running = False