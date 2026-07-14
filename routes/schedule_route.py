from fastapi import APIRouter, Query
from models.schedule import ScheduleWeek
from services.schedule_service import get_schedule_week

router = APIRouter(prefix="/schedule", tags=["Schedule"])

@router.get("/{group}/{month}/{week}", response_model=ScheduleWeek)
async def schedule_week(
        group: str,
        month: str,
        week: str,
        start_date: str = Query(..., pattern=r"^\d{2}\.\d{2}\.\d{4}$")
) -> ScheduleWeek:
    return await get_schedule_week(group, month, week, start_date)
