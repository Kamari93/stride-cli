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