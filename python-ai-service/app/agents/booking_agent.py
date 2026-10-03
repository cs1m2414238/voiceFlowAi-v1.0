import json

from app.llm.client import get_llm
from app.tools.bookings import ACTIVE, create_booking

REQUIRED = ["date", "time", "party_size"]
QUESTIONS = {
    "date": "Sure, I can help with that. What date would you like to book for?",
    "time": "What time works for you?",
    "party_size": "How many people will be coming?",
}
CANCEL_WORDS = ["cancel", "never mind", "nevermind", "forget it"]
MAX_PARTY = 10


def _extract_prompt(message: str, known: dict) -> str:
    return f"""
You collect details for a booking.
Details known so far: {json.dumps(known)}
Customer message: {message}

Extract any of these fields that the message mentions: date, time, party_size.
Reply with ONLY a JSON object with those three keys. Use null for anything not mentioned.
party_size must be a number.
Example: {{"date": "Friday", "time": "7 pm", "party_size": 4}}
"""


def _extract(message: str, known: dict) -> dict:
    try:
        raw = get_llm().invoke(_extract_prompt(message, known)).content
        data = json.loads(raw[raw.find("{"): raw.rfind("}") + 1])
    except (ValueError, TypeError):
        return {}

    result = {}
    for key in REQUIRED:
        value = data.get(key)
        if value in (None, "", "null"):
            continue
        if key == "party_size":
            try:
                value = int(value)
            except (ValueError, TypeError):
                continue
        result[key] = value
    return result


def booking_agent(message: str, session_id: str, company_id: str = "default") -> dict:
    text = message.lower()

    if session_id in ACTIVE and any(w in text for w in CANCEL_WORDS):
        ACTIVE.pop(session_id, None)
        return {"answer": "No problem, I've cancelled that booking request.",
                "escalated": False, "booking_id": None}

    slots = ACTIVE.setdefault(session_id, {})
    slots.update(_extract(message, slots))
    print(f"[booking] {session_id} slots={slots}")

    missing = [k for k in REQUIRED if k not in slots]
    if missing:
        return {"answer": QUESTIONS[missing[0]], "escalated": False, "booking_id": None}

    if slots["party_size"] > MAX_PARTY:
        ACTIVE.pop(session_id, None)
        return {"answer": "For a group that large, let me connect you with a team member.",
                "escalated": True, "booking_id": None}

    booking = create_booking(company_id, slots["date"], slots["time"], slots["party_size"])
    ACTIVE.pop(session_id, None)
    return {
        "answer": (f"You're all set! Booking {booking['booking_id']} is confirmed for "
                   f"{slots['party_size']} people on {slots['date']} at {slots['time']}."),
        "escalated": False,
        "booking_id": booking["booking_id"],
    }