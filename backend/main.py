from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from backend.api import calendly_integration, chat
from backend.db import init_db
from datetime import datetime
import os

app = FastAPI(title="Appointment Scheduling Agent", version="1.0")
app.include_router(calendly_integration.router)
app.include_router(chat.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()
    print("App startup. DB initialized. APP_TZ=", os.getenv("APP_TZ", "Asia/Kolkata"))


@app.get("/")
def root():
    """Redirect root to the interactive docs for convenience."""
    return RedirectResponse(url="/docs")


@app.get("/health")
def health():
    """Return a small health JSON including time and whether RAG / DB artifacts exist.

    This endpoint must be very cheap and never import heavy RAG dependencies.
    """
    now = datetime.utcnow().isoformat() + "Z"
    rag_path = os.path.join("backend", "rag", "faiss.index")
    db_path = os.path.join("backend", "bookings.db")
    return {
        "status": "ok",
        "time": now,
        "rag_loaded": os.path.exists(rag_path),
        "db_exists": os.path.exists(db_path),
    }
