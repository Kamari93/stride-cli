# Defines the data. Activity, Goal. Nothing else.
# Models are usually nouns.
from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4

@dataclass
class Activity:
    # required params cannot come after params with defaults
    activity_type: str 
    distance: float # miles
    duration: float # minutes
    date: date = field(default_factory=date.today)
    id: UUID = field(default_factory=uuid4, init=False) # generate its own id automatically w/o CLI
    notes: str | None = None
    route: str | None = None

    def __post_init__(self) -> None:
        if self.distance <= 0:
            raise ValueError("Distance must be greater than 0.")
        if self.duration <= 0:
            raise ValueError("Duration must be greater than 0.")
        if self.activity_type not in ("walk", "run"):
            raise ValueError("Activity type must be 'walk' or 'run'.")
    
    # TODO: calculate_pace(self) -> float
    def calculate_pace(self) -> float:
        # Return minutes per mile.
        "Return pace in minutes per mile"
        return self.duration / self.distance

    # TODO: __str__(self) -> str
    def __str__(self) -> str:
        # Return a user-friendly representation of the activity.
        notes = self.notes if self.notes else "None"
        return (
            f"{self.activity_type.title()} | "
            f"{self.distance:.1f} mi | "
            f"{self.duration:.0f} min | "
            f"Pace: {self.calculate_pace():.1f} min/mi | "
            f"Notes: {notes} | "
            f"Date: {self.date}"
        )

    # TODO: to_dict(self) -> dict
    def to_dict(self) -> dict:
        # Convert the Activity object into a dictionary.
        return {
            "id": str(self.id),
            "date": self.date.isoformat(),
            "activity_type": self.activity_type,
            "distance": self.distance,
            "duration": self.duration,
            "notes": self.notes,
            "route": self.route,
        }