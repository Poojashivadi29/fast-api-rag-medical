import uuid
from backend.db import create_booking

def make_booking(payload: dict):
    booking_id = str(uuid.uuid4())
    db_obj = {
        "booking_id": booking_id,
        "provider_id": payload["provider_id"],
        "patient_name": payload["patient_name"],
        "patient_phone": payload.get("patient_phone"),
        "start": payload["start"],
        "end": payload["end"],
        "notes": payload.get("notes"),
        "status": "confirmed"
    }
    b = create_booking(db_obj)
    return b
