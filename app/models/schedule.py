from typing import TypedDict, List

class ScheduleEntry(TypedDict):
    """TypedDict for an individual schedule entry."""
    date: str
    hour: str
    details: str

class ScheduleDocument(TypedDict):
    """TypedDict for a schedule document."""
    id: str
    entries: List[ScheduleEntry]