from pydantic import BaseModel, Field
from typing import List

class ScheduleEntrySchema(BaseModel):
    """Represents a single schedule entry."""
    date: str = Field(..., description="Date in dd.mm.yyyy format")
    hour: str = Field(..., description="Time block, e.g., '1-2'")
    details: str = Field(..., description="Detailed description of the class")

class ScheduleSchema(BaseModel):
    """Represents a complete schedule document."""
    id: str = Field(..., description="Unique identifier for the schedule document")
    entries: List[ScheduleEntrySchema] = Field(..., description="List of schedule entries")
