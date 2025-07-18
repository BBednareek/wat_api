from pydantic import BaseModel, RootModel
from typing import Optional


class ActivityParsed(BaseModel):
    raw: str
    subject: Optional[str]
    type: Optional[str]
    room: Optional[str]
    building: Optional[str]
    block_raw: str
    block_time: str


class ScheduleDay(BaseModel):
    date: str  # e.g., "03.03.2025 (pon.)"
    entries: list[ActivityParsed]


class ScheduleWeek(RootModel[dict[str, list[ScheduleDay]]]):
    """Root-level dictionary: start_date => list of days"""
    pass
