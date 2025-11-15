from datetime import datetime, timedelta, time, date
import pytz
from typing import List, Dict, Any

def generate_daily_slots_for_provider(provider: Dict[str,Any], day: date, app_tz: str):
    weekday = day.weekday()
    if weekday >= 5:
        return []
    work = provider["work_hours"]["mon-fri"]
    slot_mins = provider["slot_minutes"]
    start_dt = datetime.combine(day, work["start"])
    end_dt = datetime.combine(day, work["end"])
    tz = pytz.timezone(app_tz)
    cur = tz.localize(start_dt)
    end_local = tz.localize(end_dt)
    slots = []
    while cur + timedelta(minutes=slot_mins) <= end_local:
        slots.append({"start": cur.isoformat(), "end": (cur + timedelta(minutes=slot_mins)).isoformat(), "timezone": app_tz})
        cur += timedelta(minutes=slot_mins)
    return slots
