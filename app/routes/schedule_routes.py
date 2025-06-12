from fastapi import APIRouter, HTTPException
from app.schemas.schedule import ScheduleSchema
from app.services.error_handler import handle_errors
from app.services.firestore_service import get_schedule

router = APIRouter(prefix="/schedules", tags=["schedules"])

@handle_errors
@router.get("/{doc_id}", response_model=ScheduleSchema)
def get_one_schedule(doc_id: str) -> ScheduleSchema:
    """Fetch a specific schedule by ID."""
    doc = get_schedule(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return ScheduleSchema(id=doc_id, **doc)



