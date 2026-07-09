# Everything related to menus. No database code. No statistics. Just interacting with the user.
# External Library needed -> Rich (belongs here only) 
# follow single responsibility principle and loose coupling
from rich.console import Console

class CLI:
    '''Handles all user interactions.'''
    def __init__(self):
        self.console = Console()
    
    def run(self):
        '''Main app loop'''
        pass
    
    def show_welcome(self):
        '''Display app title.'''
        pass

    def show_main_menu(self):
        '''Display the main menu.'''
        pass

    def get_menu_choice(self):
        '''Prompt the user for a menu selection.'''
        pass

    def handle_menu_choice(self, choice):
        '''Route the user's choice to the appropriate feature.'''
        pass

    def show_log_activity(self):
        '''Display the Log Activity screen.'''
        pass

    def show_activities(self):
        '''Display all recorded activities.'''
        pass

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

    def exit(self):
        '''Exit the app.'''
        pass