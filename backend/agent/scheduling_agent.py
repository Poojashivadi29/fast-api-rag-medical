from typing import List, Dict, Any
from backend.models import AgentQueryRequest
from backend.agent.prompts import BASE_PROMPT

def decide_intent(user_text: str) -> str:
    ut = user_text.lower()
    if any(w in ut for w in ["book", "appointment", "schedule", "see dr", "see doctor"]):
        return "book"
    if any(w in ut for w in ["cancel", "reschedule", "change"]):
        return "cancel"
    return "faq"

def build_suggested_booking(provider_id: str, slot_start: str, slot_end: str, timezone: str):
    return {
        "intent": "book_appointment",
        "provider_id": provider_id,
        "preferred_start": slot_start,
        "preferred_end": slot_end,
        "timezone": timezone
    }

def generate_answer(user_text: str, passages: List[Dict[str,Any]], intent: str, provider_id: str | None = None, first_slot: Dict | None = None):
    lines = []
    if intent == "book" and provider_id and first_slot:
        sb = build_suggested_booking(provider_id, first_slot["start"], first_slot["end"], first_slot.get("timezone","Asia/Kolkata"))
        lines.append(f"I can suggest {sb['preferred_start']} for provider {provider_id}. Would you like me to book that?")
        return " ".join(lines), sb
    if passages:
        for p in passages:
            lines.append(f"{p['title']}: {p['text']}")
        return " ".join(lines), None
    return "I'm sorry — I don't have that information. Can you clarify?", None
