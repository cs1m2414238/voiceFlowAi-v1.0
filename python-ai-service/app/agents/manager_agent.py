import json

from app.llm.client import get_llm

VALID_INTENTS = [
    "faq", "booking", "order",
    "complaint", "recommendation", "human",
]


def create_intent_prompt(question: str) -> str:
    return f"""
You are the manager of a customer support system.
Classify the customer's message into exactly ONE intent.

Intents:
- faq: the customer asks for FACTS or INFORMATION about the company,
  its products, services, technology, policies, prices or hours.
- booking: wants to make, change or cancel a reservation or appointment.
- order: asks about an existing order, delivery, refund status or service request.
- complaint: is unhappy or reports a problem or bad experience.
- recommendation: asks you to CHOOSE or SUGGEST something for them
  (e.g. "which one should I buy", "what do you suggest").
- human: asks for a human agent, or the message is unclear or meaningless.

Rule: if the customer is only asking for information, the intent is faq,
NOT recommendation.

Examples:
"What technologies does the project use?" -> {{"intent": "faq", "confidence": 0.9}}
"What are your opening hours?" -> {{"intent": "faq", "confidence": 0.9}}
"Book a table for two on Friday" -> {{"intent": "booking", "confidence": 0.9}}
"Where is my order?" -> {{"intent": "order", "confidence": 0.9}}
"This service is terrible" -> {{"intent": "complaint", "confidence": 0.9}}
"Which plan do you suggest for me?" -> {{"intent": "recommendation", "confidence": 0.9}}
"Let me talk to a real person" -> {{"intent": "human", "confidence": 0.9}}
"asdf qwerty" -> {{"intent": "human", "confidence": 0.2}}

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
    print(f"[manager] {question!r} -> {intent} ({confidence})")
    return {"intent": intent, "confidence": confidence}