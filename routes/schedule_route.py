from fastapi import APIRouter, Query
from models.schedule import ScheduleWeek
from services.schedule_service import get_schedule_week

router = APIRouter(prefix="/schedule", tags=["Schedule"])

@router.get("/{group}/{month}/{week}", response_model = ScheduleWeek)
async def schedule_week(
        group: str,
        month: str,
        week: str,
        start_date: str = Query(..., regex=r"^\d{2}\.\d{2}\.\d{4}$")
) -> ScheduleWeek:
    """
    Fetches the full schedule for a given week and group.

    Args:
        group (str): Group identifier (e.g., "WCY24IX1S0").
        month (str): Name of the month in Firestore (e.g., "maj").
        week (str): Week name in Firestore (e.g., "12 V").
        start_date (str): Start date of the week (format "DD.MM.YYYY").

    Returns:
        ScheduleWeek: A Pydantic model of the week's schedule.
    """

    return await get_schedule_week(group, month, week, start_date)
