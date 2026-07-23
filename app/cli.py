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
        self.console.print("3. Edit Activity")
        self.console.print("4. Delete Activity")
        self.console.print("5. Exit")

    def get_menu_choice(self) -> str:
        '''Prompt the user for a menu selection.'''
        return Prompt.ask(
            "Choose an option",
            choices = ["1", "2", "3", "4", "5"],
        )

    def handle_menu_choice(self, choice: str) -> None:
        '''Route the user's choice to the appropriate feature.'''
        if choice == "1":
            self.log_activity()
        
        elif choice == "2":
            self.show_activities()

        elif choice == "3":
            self.edit_activity()
        
        elif choice == "4":
            self.delete_activity()

        elif choice == "5":
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

        # notes = Prompt.ask(
        #     "Notes (optional)",
        #     default = "",
        # )
        notes = self.prompt_for_optional_text("Notes (optional)")
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
        table.add_column("#")
        table.add_column("Type")
        table.add_column("Distance")
        table.add_column("Duration")
        table.add_column("Pace")
        table.add_column("Notes")
        table.add_column("Date")
        

        # for activity in activities:
        #     self.console.print(str(activity))

        for idx, activity in enumerate(activities, start=1):
            table.add_row(
                str(idx),
                activity.activity_type.title(),
                f"{activity.distance:.1f} mi",
                f"{activity.duration:.0f} min",
                f"{activity.calculate_pace():.1f} min/mi",
                activity.notes or "-",
                str(activity.date),
            )
        self.console.print("\n")
        self.console.print(table)
        self.pause()

    def edit_activity(self) -> None:
        '''Edit an existing activity.'''
        # self.console.print("coming soon")
        activity = self.select_activity()

        if activity is None:
            return

        self.console.print("\n[bold]Edit Activity[/bold]")

        distance = self.prompt_for_optional_float(f"Distance [{activity.distance}]")
        duration = self.prompt_for_optional_float(f"Duration [{activity.duration}]")
        notes = Prompt.ask(f"Notes [{activity.notes or ""}]", default=activity.notes or "",)

        try:
            updated_activity = Activity(
                activity_type = activity.activity_type,
                distance = distance if distance is not None else activity.distance,
                duration = duration if duration is not None else activity.duration,
                notes = notes or None,
                # route = activity.route 
            )

            self.activity_service.update_activity(activity.id, updated_activity)
        
        except ValueError as e:
            self.show_error(e)
            return 
        
        self.show_success("Activity updated successfully!")
        self.pause()


    def delete_activity(self) -> None:
        '''Delete an existing activity'''
        # self.console.print("coming soon")

        activity = self.select_activity()

        if activity is None:
            return 
        
        # self.console.print("\n[bold red]Delete Activity[/bold red]")
        # self.console.print(activity)
        self.console.print("\n[bold red]You are about to delete:[/bold red]")
        self.console.print(str(activity)) # utilize __str__ method from Activity model to display

        confirm = Prompt.ask("Are you sure you want to delete this activity? (y/n)", choices=["y", "n"], default="n")

        if confirm == "n":
            self.console.print("[yellow]Deletion cancelled[/yellow]")
            self.pause()
            return
        
        deleted = self.activity_service.delete_activity(activity.id)
        
        if deleted:
            self.show_success("Activity deleted successfully!")
        
        else:
            self.show_error("Activity could not be deleted")
        
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
            except ValueError:
                self.show_error("Please enter a valid number.")
    
    def prompt_for_int(self, prompt: str) -> int:
        '''Prompt until the user enters a valid integer.'''
        while True:
            try:
                return int(Prompt.ask(prompt))
            except ValueError:
                self.show_error("Please enter a valid integer.")

    def prompt_for_optional_text(self, prompt: str) -> str | None:
        '''Prompt the user for text. Returns None if the user leaves it blank.'''
        while True:
            try:
                input = Prompt.ask(prompt).strip()
                return input if input else None

            except:
                self.show_error("Please enter a valid text input.")
    
    def prompt_for_optional_float(self, prompt: str) -> float | None:
        '''Prompt for a number. Press Enter to keep the current value.'''
        while True:
            value = Prompt.ask(prompt, default="").strip()

            if value == "":
                return None
            
            try:
                return float(value)
            except ValueError:
                self.show_error("Please enter a valid number.")
            
    def select_activity(self) -> Activity | None:
        '''Display activities and return the selected one.'''
        activities = self.activity_service.get_all_activities()

        if not activities:
            self.show_error("No activities found.")
            return None

        self.show_activities()

        while True:
            choice = self.prompt_for_int("Select activity number (0 to cancel)")

            if choice == 0:
                return None

            if 1 <= choice <= len(activities):
                return activities[choice - 1]
            
            self.show_error("Invalid activity number.")

    def pause(self) -> None:
        Prompt.ask("\nPress Enter to continue")

    def exit(self) -> None:
        '''Exit the app.'''
        self.console.print("\nGoodbye!")
        self.running = False