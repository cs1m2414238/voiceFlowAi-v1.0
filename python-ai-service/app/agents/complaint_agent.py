import json
import logging
import re

from app.llm.client import get_llm
from app.tools.tickets import create_ticket

logger = logging.getLogger(__name__)

CATEGORIES = ["service", "product", "billing", "delivery", "other"]
SEVERITIES = ["low", "medium", "high"]

HIGH_RISK_PATTERN = re.compile(
    r"\b(legal|lawyer|attorney|fraud|fraudulent|unsafe|police|sue|sued|scam|scammed)\b"
)
NEGATIONS = {"not", "no", "never", "without"}


def _has_high_risk(text: str) -> bool:
    """Whole-word match, skipping a keyword if a negation is just before it."""
    text = text.lower().replace("’", "'")
    for match in HIGH_RISK_PATTERN.finditer(text):
        previous = re.findall(r"[\w']+", text[:match.start()])[-3:]
        negated = any(w in NEGATIONS or w.endswith("n't") for w in previous)
        if not negated:
            return True
    return False


def _analysis_prompt(question: str) -> str:
    return f"""
You handle customer complaints. Read the message and reply with ONLY a JSON object:
{{"category": "<service|product|billing|delivery|other>",
  "severity": "<low|medium|high>",
  "summary": "<one short sentence describing the problem>"}}

Use severity "high" only for serious issues (safety, money lost, legal threats).

Customer message: {question}
"""


def _analyse(question: str) -> dict:
    defaults = {"category": "other", "severity": "medium", "summary": question[:200]}
    try:
        raw = get_llm().invoke(_analysis_prompt(question)).content
        data = json.loads(raw[raw.find("{"): raw.rfind("}") + 1])
        if not isinstance(data, dict):
            raise ValueError("Model reply is not a JSON object")
    except Exception:
        # Ollama down, timeout, bad JSON... the complaint must still be logged.
        logger.exception("Complaint analysis failed, using default values")
        return defaults

    category = data.get("category", "other")
    severity = data.get("severity", "medium")
    return {
        "category": category if category in CATEGORIES else "other",
        "severity": severity if severity in SEVERITIES else "medium",
        "summary": str(data.get("summary") or defaults["summary"]),
    }


def complaint_agent(question: str, company_id: str = "default") -> dict:
    info = _analyse(question)

    if _has_high_risk(question):
        info["severity"] = "high"

    try:
        ticket = create_ticket(
            company_id=company_id,
            category=info["category"],
            description=info["summary"],
            severity=info["severity"],
        )
    except Exception:
        logger.exception("Ticket creation failed for company %s", company_id)
        return {
            "answer": ("I'm sorry, I couldn't log your complaint just now. "
                       "I'm connecting you with a human representative so it isn't lost."),
            "escalated": True,
            "ticket_id": None,
        }

    print(f"[complaint] {ticket['ticket_id']} {info['category']}/{info['severity']}")

    escalate = info["severity"] == "high"
    if escalate:
        answer = (f"I'm very sorry about this. I've logged it as ticket {ticket['ticket_id']} "
                  "and I'm connecting you with a human representative now.")
    else:
        answer = (f"I'm sorry about that. I've logged your complaint as ticket "
                  f"{ticket['ticket_id']}, and our team will follow up with you.")

    return {"answer": answer, "escalated": escalate, "ticket_id": ticket["ticket_id"]}