from datetime import datetime, timedelta
from typing import Any
from google.cloud import firestore
from google.cloud.firestore_v1 import CollectionReference
from google.cloud.firestore_v1.base_document import DocumentSnapshot
from exceptions.schedule_exceptions import FirestoreConnectionError, ScheduleNotFoundError, InvalidDayNameError, \
    ActivityParsingError
from models.schedule import ScheduleWeek, ScheduleDay, ActivityParsed
from parsers.schedule_parser import parse_activity, parse_block
from utils.date_utils import DAYS_INDEX
from os import environ

environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'key.json'
db: firestore.Client = firestore.Client()


async def  get_schedule_week(group: str, month: str, week: str, start_date: str) -> ScheduleWeek:
    """
    Retrieves the full weekly schedule for a given group from Firestore.

    Args:
        group (str): The group identifier (e.g., "WCY24IX1S0").
        month (str): The month document name in Firestore (e.g., "maj").
        week (str): The week document name in Firestore (e.g., "12 V").
        start_date (str): The start date of the week in format "DD.MM.YYYY".

    Returns:
        ScheduleWeek: A structured model containing the weekly schedule.

    Raises:
        HTTPException: If the schedule is not found or a Firestore error occurs.
    """
    try:
        week_collection: CollectionReference = (
            db.collection("groups")
              .document(group)
              .collection(month)
              .document(week)
              .collection("days")
        )

        try:
            documents: Any = week_collection.stream()
        except Exception as e:
            raise FirestoreConnectionError("Could not connect to Firestore") from e

        if not documents:
            raise ScheduleNotFoundError("No days found for the given week")

        start_dt: datetime = datetime.strptime(start_date, "%d.%m.%Y")
        week_data: list[ScheduleDay] = []

        for doc in documents:
            day_name: str = doc.id
            if day_name not in DAYS_INDEX:
                raise InvalidDayNameError(f"Unsupported day name in Firestore: '{day_name}'")

            offset: int = DAYS_INDEX[day_name]
            actual_date: datetime = start_dt + timedelta(days=offset)
            actual_date_str: str = actual_date.strftime("%d.%m.%Y")

            snapshot: DocumentSnapshot = doc
            data: dict[str, Any] = snapshot.to_dict()
            raw_entries: list[dict[str, str]] = data.get("entries", [])
            parsed_entries: list[ActivityParsed] = []

            for entry in raw_entries:
                raw_block: str = entry.get("block", "")
                try:
                    parsed_dict: dict[str, Any] = parse_activity(entry.get("activity", ""))
                    parsed_entry: ActivityParsed = ActivityParsed(
                        **parsed_dict,
                        block_raw=raw_block,
                        block_time=parse_block(raw_block)
                    )
                    parsed_entries.append(parsed_entry)
                except Exception as e:
                    raise ActivityParsingError(f"Failed to parse activity: {entry} ") from e

            schedule_day: ScheduleDay = ScheduleDay(
                date=f"{actual_date_str} ({day_name})",
                entries=parsed_entries
            )
            week_data.append(schedule_day)

        if not week_data:
            raise ScheduleNotFoundError("No schedule data available for this week")

        sorted_data: list[ScheduleDay] = sorted(
            week_data,
            key=lambda x: datetime.strptime(x.date[:10], "%d.%m.%Y")
        )

        return ScheduleWeek.model_validate({start_date : sorted_data})

    except (FirestoreConnectionError, ScheduleNotFoundError, InvalidDayNameError, ActivityParsingError):
        raise

    except Exception as e:
        raise FirestoreConnectionError(f"Unexpected Firestore error: {str(e)}") from e
