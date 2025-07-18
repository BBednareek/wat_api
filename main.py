from fastapi import FastAPI, HTTPException, Query
from google.cloud import firestore
from os import environ
from typing import Any
from google.cloud.firestore_v1 import Client
from parser import parse_activity, parse_block
from datetime import datetime, timedelta

environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

app: FastAPI = FastAPI()
db: Client = firestore.Client()

# Mapowanie nazw dni na indeksy
DAYS_INDEX = {
    "pon.": 0,
    "wt.": 1,
    "śr.": 2,
    "czw.": 3,
    "pt.": 4,
    "sob.": 5,
    "niedz.": 6
}

@app.get("/schedule/{group}/{month}/{week}")
async def get_week_schedule(
    group: str,
    month: str,
    week: str,
    start_date: str = Query(..., regex=r"^\d{2}\.\d{2}\.\d{4}$")
):
    """
    Zwraca cały tydzień planu zajęć.
    start_date: np. 03.03.2025 (poniedziałek danego tygodnia)
    """
    try:
        week_collection = (
            db.collection("groups")
            .document(group)
            .collection(month)
            .document(week)
            .collection("days")
        )

        documents = week_collection.stream()
        start_dt = datetime.strptime(start_date, "%d.%m.%Y")
        week_data = []

        for doc in documents:
            day_name = doc.id  # np. "śr.", "pon."
            if day_name not in DAYS_INDEX:
                continue

            offset = DAYS_INDEX[day_name]
            actual_date = start_dt + timedelta(days=offset)
            actual_date_str = actual_date.strftime("%d.%m.%Y")

            data: dict[str, Any] = doc.to_dict()
            raw_entries: list = data.get("entries", [])

            parsed_entries: list = []
            for entry in raw_entries:
                raw_block = entry.get("block", "")
                parsed = parse_activity(entry.get("activity", ""))
                parsed["block_raw"] = raw_block
                parsed["block_time"] = parse_block(raw_block)
                parsed_entries.append(parsed)

            week_data.append({
                "date": f"{actual_date_str} ({day_name})",
                "entries": parsed_entries
            })

        if not week_data:
            raise HTTPException(status_code=404, detail="Week not found")

        return {
            start_date: sorted(week_data, key=lambda x: datetime.strptime(x["date"][:10], "%d.%m.%Y"))
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
