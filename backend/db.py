from sqlmodel import SQLModel, Field, create_engine, Session, select
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./backend/bookings.db")
engine = create_engine(DATABASE_URL, echo=False)

class Booking(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    booking_id: str
    provider_id: str
    patient_name: str
    patient_phone: str | None = None
    start: str
    end: str
    notes: str | None = None
    status: str

def init_db():
    SQLModel.metadata.create_all(engine)

def create_booking(obj: dict):
    with Session(engine) as s:
        b = Booking(**obj)
        s.add(b)
        s.commit()
        s.refresh(b)
        return b

def get_bookings_for_provider(provider_id: str):
    with Session(engine) as s:
        q = select(Booking).where(Booking.provider_id == provider_id)
        return s.exec(q).all()
