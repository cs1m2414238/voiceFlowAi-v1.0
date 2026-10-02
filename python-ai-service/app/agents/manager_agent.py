import json

from app.llm.client import get_llm

VALID_INTENTS = [
    "faq", "booking", "order",
    "complaint", "recommendation", "human",
]


def create_intent_prompt(question: str) -> str:
    return f"""
You are the manager of a customer support system.
Classify the customer's message into exactly ONE intent:

- faq: general questions about the company, policies, products, hours
- booking: wants to make, change or cancel a reservation or appointment
- order: asks about an order, delivery, refund or service request
- complaint: unhappy, reporting a problem or a bad experience
- recommendation: asks for suggestions or help choosing
- human: asks for a human agent, or the message is unclear

Reply with ONLY a JSON object and nothing else:
{{"intent": "<one intent from the list>", "confidence": <number from 0 to 1>}}

Customer message: {question}
"""


def manager_agent(question: str) -> dict:
    """Detect the customer's intent. Falls back to 'human' if unsure."""
    llm = get_llm()
    raw = llm.invoke(create_intent_prompt(question)).content

    try:
        start, end = raw.find("{"), raw.rfind("}") + 1
        data = json.loads(raw[start:end])
        intent = data.get("intent", "human")
        confidence = float(data.get("confidence", 0.0))
    except (ValueError, TypeError):
        return {"intent": "human", "confidence": 0.0}

    if intent not in VALID_INTENTS:
        return {"intent": "human", "confidence": 0.0}

    return {"intent": intent, "confidence": confidence}