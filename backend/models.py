from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

class Slot(BaseModel):
    start: datetime
    end: datetime

class AvailabilityResponse(BaseModel):
    provider_id: str
    provider_name: str
    timezone: str
    slots: List[Slot]

class BookingRequest(BaseModel):
    provider_id: str
    patient_name: str
    patient_phone: Optional[str] = None
    start: datetime
    end: datetime
    notes: Optional[str] = None
    timezone: Optional[str] = Field(None)

class BookingResponse(BaseModel):
    booking_id: str
    provider_id: str
    patient_name: str
    start: datetime
    end: datetime
    status: str
    message: Optional[str] = None

class AgentQueryRequest(BaseModel):
    user_query: str
    provider_id: Optional[str] = None
    timezone: Optional[str] = None

class RetrievedPassage(BaseModel):
    id: str
    title: str
    text: str
    score: float

class AgentQueryResponse(BaseModel):
    answer: str
    passages: List[RetrievedPassage]
    suggested_booking: Optional[Dict[str, Any]] = None
