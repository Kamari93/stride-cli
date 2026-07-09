# Defines the data. Activity, Goal. Nothing else.
# Models are usually nouns.
from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4

@dataclass
class Activity:
    id: UUID = field(default_factory=uuid4)
    date: date = field(default_factory=date.today)
    activity_type: str 
    distance: float # miles
    duration: float # minutes
    notes: str | None = None
    route: str | None = None

    def __post_init__(self) -> None:
        if self.distance <= 0:
            raise ValueError("Distance cannot be negative.")
        if self.duration <= 0:
            raise ValueError("Duration cannot be negative.")
        if self.activity_type not in ("walk", "run"):
            raise ValueError("Activity type must be 'walk' or 'run'.")
    
    # TODO: calculate_pace(self) -> float
    # Return minutes per mile.

    # TODO: __str__(self) -> str
    # Return a user-friendly representation of the activity.

    # TODO: to_dict(self) -> dict
    # Convert the Activity object into a dictionary.