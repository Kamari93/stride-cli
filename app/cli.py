# Everything related to menus. No database code. No statistics. Just interacting with the user.
# External Library needed -> Rich (belongs here only) 
# follow single responsibility principle and loose coupling
from rich.console import Console
from rich.panel import Panel 
from rich.prompt import Prompt
from rich.table import Table
from rich import box

from app.models import Activity, Goal
from app.services import ActivityService, GoalService
from app.stats import (
    total_activities,
    total_distance,
    total_duration,
    average_pace,
    activity_counts,
    longest_activity,
    longest_run,
    longest_walk,
    fastest_pace,
    weekly_distance,
    monthly_distance,
    current_streak,
    longest_streak,
    average_walk_pace,
    average_run_pace,
    fastest_walk_pace,
    fastest_run_pace,
)

class CLI:
    '''Handles all user interactions.'''
    def __init__(self, activity_service: ActivityService, goal_service: GoalService) -> None:
        self.console = Console()
        self.activity_service = activity_service
        self.goal_service = goal_service
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
        self.console.print("5. Statistics")
        self.console.print("6. Goals")
        self.console.print("7. Export Activities")
        self.console.print("8. Exit")

    def get_menu_choice(self) -> str:
        '''Prompt the user for a menu selection.'''
        return Prompt.ask(
            "Choose an option",
            choices = ["1", "2", "3", "4", "5", "6", "7", "8"],
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
            self.show_statistics()

        elif choice == "6":
            self.show_goals_menu()

        elif choice == "":
            self.export_activities()

        elif choice == "7":
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
        route = self.prompt_for_optional_text("Route (optional)")
        try:
            activity = Activity(
                activity_type = activity_type,
                distance = distance,
                duration = duration,
                notes = notes or None,
                route = route,
            )

            self.activity_service.create_activity(activity)
        except ValueError as e:
            self.show_error(str(e))
            return
        
        # self.console.print("[green]✓ Activity logged successfully![/green]")
        self.show_success("Activity logged successfully!")
        self.pause()

    def display_activities(self) -> None:
        '''Display all recorded activities in a table'''
        activities = self.activity_service.get_all_activities()

        if not activities:
            self.console.print("[yellow]No activities logged yet.[/yellow]")
            return
        
        table = Table(show_header=True, title="Activities", header_style="bold green", box=box.ROUNDED, show_lines=True,)
        table.add_column("#")
        table.add_column("Type")
        table.add_column("Distance")
        table.add_column("Duration")
        table.add_column("Pace")
        table.add_column("Notes")
        table.add_column("Route")
        table.add_column("Date")
        
        for idx, activity in enumerate(activities, start=1):
            table.add_row(
                str(idx),
                activity.activity_type.title(),
                f"{activity.distance:.1f} mi",
                f"{activity.duration:.0f} min",
                # f"{activity.calculate_pace():.1f} min/mi",
                activity.formatted_pace(),
                activity.notes or "-",
                activity.route or "-",
                # str(activity.date),
                activity.formatted_date(),
            )
        self.console.print("\n")
        self.console.print(table)

    def show_activities(self) -> None:
        '''Display activities and wait for the user.'''
        # self.console.print("\n[bold]Activities[/bold]")
        self.display_activities()
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
        route = Prompt.ask(f"Route [{activity.route or ""}]", default=activity.route or "",)

        try:
            updated_activity = Activity(
                activity_type = activity.activity_type,
                distance = distance if distance is not None else activity.distance,
                duration = duration if duration is not None else activity.duration,
                notes = notes or None,
                route = route or None,
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
        self.console.print("\n[bold red]You are about to delete:[/bold red]\n")
        self.console.print(str(activity)) # utilize __str__ method from Activity model to display

        confirm = Prompt.ask("\nAre you sure you want to delete this activity?", choices=["y", "n"], default="n")

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
        activities = self.activity_service.get_all_activities()

        if not activities:
            self.show_error("No activities found.")
            return

        counts = activity_counts(activities)
        table = Table(
            title = "Statistics",
            box = box.ROUNDED,
            show_header = True,
            header_style = "bold cyan",
            show_lines=True,
        )

        table.add_column("Metric")
        table.add_column("Value")

        table.add_row("Total Activities", str(total_activities(activities)))
        table.add_row("Total Distance", f"{total_distance(activities):.1f} mi")
        table.add_row("Total Duration", f"{total_duration(activities):.0f} min")

        pace = average_pace(activities)
        minutes = int(pace)
        seconds = round((pace - minutes) * 60)

        walk_pace = average_walk_pace(activities)
        walk_minutes = int(walk_pace)
        walk_seconds = round((walk_pace - walk_minutes) * 60)

        run_pace = average_run_pace(activities)
        run_minutes = int(run_pace)
        run_seconds = round((run_pace - run_minutes) * 60)

        # table.add_row("Average Pace", f"{pace:.1f} min/mi" if pace is not None else "-")
        table.add_row("Average Pace", f"{minutes}:{seconds:02d} min/mi" if pace is not None else "-")
        table.add_row("Average Walk Pace", f"{walk_minutes}:{walk_seconds:02d} min/mi" if walk_pace is not None else "-")
        table.add_row("Average Run Pace", f"{run_minutes}:{run_seconds:02d} min/mi" if run_pace is not None else "-")
        table.add_row("Total Walks", str(counts["walk"]))
        table.add_row("Total Runs", str(counts["run"]))

        longest = longest_activity(activities)
        if longest:
            table.add_row("Longest Activity", f"{longest.distance:.1f} mi")

        fastest = fastest_pace(activities)
        if fastest:
            table.add_row("Fastest Pace", fastest.formatted_pace())

        fastest_walk = fastest_walk_pace(activities)
        if fastest_walk:
            table.add_row("Fastest Walk Pace", fastest_walk.formatted_pace())

        fastest_run = fastest_run_pace(activities)
        if fastest_run:
            table.add_row("Fastest Run Pace", fastest_run.formatted_pace())

        longest_walk_activity = longest_walk(activities)
        if longest_walk_activity:
            table.add_row("Longest Walk", f"{longest_walk_activity.distance:.1f} mi")

        longest_run_activity = longest_run(activities)
        if longest_run_activity:
            table.add_row("Longest Run", f"{longest_run_activity.distance:.1f} mi")

        weekly = weekly_distance(activities)
        if weekly:
            table.add_row("Weekly Distance", f"{weekly:.1f} mi")

        monthly = monthly_distance(activities)
        if monthly:
            table.add_row("Monthly Distance", f"{monthly:.1f} mi")

        table.add_row("Current Streak", f"{current_streak(activities)} days")
        table.add_row("Longest Streak", f"{longest_streak(activities)} days")
        self.console.print()
        self.console.print(Panel.fit("Activity Summary", title="Statistics", border_style="cyan",))
        self.console.print(table)

        self.pause()

    def show_goals_menu(self) -> None:
        '''Display the goals menu.'''
        while True:
            self.console.print("\n[bold]Goals Menu[/bold]")
            self.console.print("1. View Goals")
            self.console.print("2. Create Goal")
            self.console.print("3. Edit Goal")
            self.console.print("4. Delete Goal")
            self.console.print("5. Back To Main")

            choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5"])

            if choice == "1":
                self.show_goals()
            if choice == "2":
                self.create_goal()
            if choice == "3":
                self.edit_goal()
            if choice == "4":
                self.delete_goal()
            if choice == "5":
                return

    def show_goals(self) -> None:
        '''Display all goals and their progress.'''
        goals = self.goal_service.get_all_goals()
        activities = self.activity_service.get_all_activities()

        if not goals:
            self.show_error("No goals found.")
            self.pause()
            return

        table = Table(
            title = "Goals",
            box = box.ROUNDED,
            show_header = True,
            header_style = "bold cyan",
            show_lines=True,
        )

        table.add_column("Goal")
        table.add_column("Target")
        table.add_column("Progress")
        table.add_column("Completion")
        table.add_column("Progress Bar")
        table.add_column("Status")

        for goal in goals:
            progress = self.goal_service.get_goal_progress(goal, activities)
            percentage = self.goal_service.get_goal_percentage(goal, activities)
            complete = self.goal_service.is_goal_complete(goal, activities)

            goal_name = goal.goal_type.replace("_", " ").title()

            if goal.goal_type in ("weekly_distance", "monthly_distance"):
                target_text = f"{goal.target:.1f} mi"
                progress_text = f"{progress:.1f} mi"

            if goal.goal_type in ("current_streak", "longest_streak"):
                target_text = f"{goal.target:.0f} days"
                progress_text = f"{progress:.0f} days"

            else:
                target_text = str(goal.target)
                progress_text = str(progress)

            status = ("[green]✓ Complete[/green]" if complete else "[yellow]In Progress[/yellow]")
            progress_bar = self.create_goal_progress_bar(percentage)

            table.add_row(
                goal_name,
                target_text,
                progress_text,
                f"{percentage:.0f}%",
                f"{progress_bar}",
                status,
            )

        self.console.print()
        self.console.print(
            Panel.fit("Track your progress toward your goals.", title="Goals", border_style="cyan",)
        )
        self.console.print(table)
        self.pause()

    def create_goal_progress_bar(self, percentage: float) -> str:
        '''Return a simple visual progress bar.'''
        width = 20
        percentage = min(percentage, 100)

        completed = round(width * percentage / 100)
        remaining = width - completed

        return completed * "█" + remaining * "░"

    def create_goal(self,) -> None:
        '''Create a new goal through the CLI.'''
        self.console.print("\n[bold]Create Goal Menu[/bold]")
        self.console.print("1. Weekly Distance Goal")
        self.console.print("2. Monthly Distance Goal")
        self.console.print("3. Current Streak Goal")
        self.console.print("4. Longest Streak Goal")
        self.console.print("5. Cancel")

        choice = Prompt.ask("Goal Type", choices = ["1", "2", "3", "4", "5"],)

        if choice == "1":
            goal_type = "weekly_distance"
        if choice == "2":
            goal_type = "monthly_distance"
        if choice == "3":
            goal_type = "current_streak"
        if choice == "4":
            goal_type = "longest_streak"
        if choice == "5":
            return


        target = self.prompt_for_float("Target")

        try:
            goal = Goal(goal_type, target)
            self.goal_service.create_goal(goal)
        except ValueError as e:
            self.show_error(str(e))
            self.pause()
            return

        self.show_success("Goal created successfully!")
        self.pause()

    def edit_goal(self) -> None:
        '''Edit an existing goal.'''
        goals = self.goal_service.get_all_goals()

        if not goals:
            self.show_error("No goals found.")
            self.pause()
            return

        self.display_goals()

        choice = self.prompt_for_int("Select activity number (0 to cancel)")
        
        if choice == 0:
            return None

        if not 1 <= choice <= len(goals):
            self.show_error("Invalid goal number.")
            self.pause()
            return

        goal = goals[choice - 1]

        self.console.print("\n[bold]Edit Goal[/bold]")

        target = self.prompt_for_optional_float(f"Target: {goal.target}")

        updated_goal = Goal(goal.goal_type, (target if target is not None else goal.target))

        try:
            result = self.goal_service.update_goal(goal.id, updated_goal)
        except ValueError as e:
            self.show_error(str(e))
            self.pause
            return

        if result is None:
            self.show_error("Goal could not be updated.")
            self.pause()
            return
        
        self.show_success("Goal updated successfully!")
        self.pause()

    def delete_goal(self) -> None:
        '''Delete an existing goal.'''
        goals = self.goal_service.get_all_goals()
        
        if not goals:
            self.show_error("No goals found.")
            self.pause()
            return

        self.display_goals()

        choice = self.prompt_for_int("Select activity number (0 to cancel)")
        
        if choice == 0:
            return None

        if not 1 <= choice <= len(goals):
            self.show_error("Invalid goal number.")
            self.pause()
            return

        goal = goals[choice - 1]
        goal_name = goal.goal_type.replace("_", " ").title()

        self.console.print(
            f"\n[bold red]You are about to delete:[/bold red]\n"
            f"Goal: {goal_name} - {goal.target}"
        )

        confirm = Prompt.ask("\nAre you sure you want to delete this goal?", choices=["y", "n"], default="n")
        
        if confirm == "n":
            self.console.print("[yellow]Deletion cancelled[/yellow]")
            self.pause()
            return

        deleted = self.goal_service.delete_goal(goal.id)

        if deleted:
            self.show_success("Goal deleted successfully!")
        else:
            self.show_error("Goal could not be deleted.")

        self.pause()

    def display_goals(self) -> None:
        '''Display goals in a simple selection table.'''
        goals = self.goal_service.get_all_goals()

        if not goals:
            self.console.print("[yellow]No goals found.[/yellow]")
            return

        table = Table(
            title = "Goals",
            box = box.ROUNDED,
            show_header = True,
            header_style = "bold cyan",
            show_lines=True,
        )

        table.add_column("#")
        table.add_column("Goal")
        table.add_column("Target")

        for idx, goal in enumerate(goals, start=1):
            goal_name = goal.goal_type.replace("_", " ").title()

            if goal.goal_type in ("weekly_distance", "monthly_distance"):
                target_text = f"{goal.target:.1f} mi"
            else:
                target_text = f"{goal.target:.0f} days"

            table.add_row(
                str(idx),
                goal_name,
                target_text,
                )
        self.console.print()
        self.console.print(table)

    def export_activities(self) -> None:
        '''Export activities to a CSV file.'''
        activities = self.activity_service.get_all_activities()

        if not activities:
            self.show_error("No activities found to export.")
            self.pause()
            return

        filepath = Prompt.ask("Enter CSV File", default="activities.csv").strip()

        if not filepath:
            filepath = "activities.csv"

        try:
            self.activity_service.export_activities(filepath)
        except OSError as e:
            self.show_error(f"Could not export activities: {e}")
            self.pause()
            return

        self.show_success(f"Activities exported successfully to {filepath}")
        self.pause()

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
            text = Prompt.ask(prompt).strip()
            return text if text else None
            # try:
            #     text = Prompt.ask(prompt).strip()
            #     return text if text else None

            # except Exception:
            #     self.show_error("Please enter a valid text input.")
    
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

        # self.show_activities()
        self.display_activities()

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