from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta, date
from backend.models import AvailabilityResponse, BookingRequest, BookingResponse, Slot
from typing import List, Dict, Any
from backend.tools.availability_tool import generate_daily_slots_for_provider
from backend.db import init_db, get_bookings_for_provider, create_booking
import pytz
import uuid, os

router = APIRouter(prefix="/api/calendly", tags=["calendly"])

PROVIDERS = {
    "provider-1": {
        "name": "Dr. Maya Iyer",
        "specialty": "Cardiology",
        "work_hours": {"mon-fri": {"start": datetime.strptime("09:00","%H:%M").time(), "end": datetime.strptime("17:00","%H:%M").time()}},
        "slot_minutes": 30
    },
    "provider-2": {
        "name": "Dr. Rajesh Kumar",
        "specialty": "Pediatrics",
        "work_hours": {"mon-fri": {"start": datetime.strptime("08:00","%H:%M").time(), "end": datetime.strptime("14:00","%H:%M").time()}},
        "slot_minutes": 20
    }
}

APP_TZ = os.getenv("APP_TZ", "Asia/Kolkata")

init_db()

@router.get("/availability", response_model=AvailabilityResponse)
def availability(provider_id: str, days: int = 7, timezone: str = APP_TZ):
    if provider_id not in PROVIDERS:
        raise HTTPException(status_code=404, detail="Provider not found")
    provider = PROVIDERS[provider_id]
    tz = pytz.timezone(timezone)
    today = datetime.now(tz).date()
    slots = []
    bookings = get_bookings_for_provider(provider_id)
    for i in range(days):
        d = today + timedelta(days=i)
        daily = generate_daily_slots_for_provider(provider, d, timezone)
        for s in daily:
            free = True
            s_start = s["start"]
            s_end = s["end"]
            for b in bookings:
                if not (s_end <= b.start or s_start >= b.end):
                    free = False
                    break
            if free:
                slots.append({"start": s_start, "end": s_end})
    return AvailabilityResponse(provider_id=provider_id, provider_name=provider["name"], timezone=timezone, slots=slots)

@router.post("/book", response_model=BookingResponse)
def book(req: BookingRequest):
    if req.provider_id not in PROVIDERS:
        raise HTTPException(status_code=404, detail="Provider not found")
    booking_obj = {
        "booking_id": str(uuid.uuid4()),
        "provider_id": req.provider_id,
        "patient_name": req.patient_name,
        "patient_phone": req.patient_phone,
        "start": req.start.isoformat(),
        "end": req.end.isoformat(),
        "notes": req.notes,
        "status": "confirmed"
    }
    b = create_booking(booking_obj)
    return BookingResponse(
        booking_id=b.booking_id,
        provider_id=b.provider_id,
        patient_name=b.patient_name,
        start=b.start,
        end=b.end,
        status=b.status,
        message="Booking confirmed"
    )
