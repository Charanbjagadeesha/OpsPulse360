from fastapi import APIRouter
import json
from pathlib import Path

router = APIRouter(
    prefix="/api/stream",
    tags=["Streaming"]
)

EVENT_FILE = Path("/mnt/c/OpsPulse360/processed_events.jsonl")


@router.get("/events")
def get_stream_events():
    events = []

    if not EVENT_FILE.exists():
        return events

    with EVENT_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    return events[-100:]
