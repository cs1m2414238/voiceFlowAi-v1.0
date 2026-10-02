import json

from app.llm.client import get_llm
from app.tools.tickets import create_ticket

CATEGORIES = ["service", "product", "billing", "delivery", "other"]
SEVERITIES = ["low", "medium", "high"]
HIGH_RISK_WORDS = ["legal", "lawyer", "fraud", "unsafe", "police", "sue", "scam"]


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
    except (ValueError, TypeError):
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

    # Safety net: a small model can miss serious cases, so check keywords too.
    if any(word in question.lower() for word in HIGH_RISK_WORDS):
        info["severity"] = "high"

    ticket = create_ticket(
        company_id=company_id,
        category=info["category"],
        description=info["summary"],
        severity=info["severity"],
    )
    print(f"[complaint] {ticket['ticket_id']} {info['category']}/{info['severity']}")

    escalate = info["severity"] == "high"
    if escalate:
        answer = (f"I'm very sorry about this. I've logged it as ticket {ticket['ticket_id']} "
                  "and I'm connecting you with a human representative now.")
    else:
        answer = (f"I'm sorry about that. I've logged your complaint as ticket "
                  f"{ticket['ticket_id']}, and our team will follow up with you.")

    return {"answer": answer, "escalated": escalate, "ticket_id": ticket["ticket_id"]}
