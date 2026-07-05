## Core models (version 1)
- Activity
- Goal

## Application Layers 
- CLI (Presentation) - Responsible for interacting with the user. The CLI displays menus.
- Statistics (Business Logic) - Responsible for calculating statitstics. Calculates statistics.
- Services (Business Logic) - Responsible for coordinating application logic and validating data. Validates data.
- Data (SQLite) - Responsible for storing and retrieving data. Stores and retrieves data.

## Data Flow
- The user selects “Log Activity” from the menu. The CLI gathers input, passes it to the service layer, which validates and stores the activity in the database. Later, the statistics module reads those stored activities to calculate summaries.

## Open Questions 
- Should distance be stored in miles only?
- How should pace be displayed?
- How should goals be represented?

## Activity Model
- id
- date
- activity_type (run/walk)
- distance (miles)
- duration (minutes)
- notes
- route 
- weather (future)