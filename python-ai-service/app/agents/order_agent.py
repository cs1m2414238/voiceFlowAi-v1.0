import re

from app.tools.orders import PENDING, create_service_request, get_order

ID_PATTERN = re.compile(r"\b(?:ord[-\s]?)?(\d{4,8})\b", re.IGNORECASE)
REQUEST_WORDS = ("refund", "return", "cancel", "exchange")
DROP_WORDS = ("never mind", "nevermind", "forget it", "stop")
MAX_TRIES = 2


def _reply(answer, escalated=False):
    return {"answer": answer, "escalated": escalated}


def _handoff():
    return _reply("I'm having trouble finding that order. "
                  "Let me connect you with a team member.", True)


def _describe(order_id, order):
    if order["status"] == "Delivered":
        return (f"Order {order_id} ({order['item']}) was delivered on {order['date']}.")
    return (f"Order {order_id} ({order['item']}) is {order['status'].lower()} "
            f"and expected by {order['date']}.")


def order_agent(message: str, session_id: str, company_id: str = "default") -> dict:
    text = message.lower()

    if session_id in PENDING and any(w in text for w in DROP_WORDS):
        PENDING.pop(session_id, None)
        return _reply("No problem, I've dropped that request.")

    pending = PENDING.get(session_id, {})
    tries = pending.get("tries", 0)
    wants_request = any(w in text for w in REQUEST_WORDS)
    kind = pending.get("kind") or ("request" if wants_request else "status")
    if wants_request:
        kind = "request"

    match = ID_PATTERN.search(message)
    if not match:
        if tries >= MAX_TRIES:
            PENDING.pop(session_id, None)
            return _handoff()
        PENDING[session_id] = {"kind": kind, "tries": tries + 1}
        return _reply("Sure, I can help with that. What is your order number?")

    order_id = match.group(1)
    order = get_order(order_id)
    if order is None:
        if tries >= MAX_TRIES:
            PENDING.pop(session_id, None)
            return _handoff()
        PENDING[session_id] = {"kind": kind, "tries": tries + 1}
        return _reply(f"I couldn't find order {order_id}. "
                      "Please check the number and send it again.")

    PENDING.pop(session_id, None)
    print(f"[order] {session_id} order={order_id} kind={kind}")

    if kind == "status":
        return _reply(_describe(order_id, order))

    status = order["status"]
    if status == "Processing":
        req = create_service_request(order_id, "cancellation")
        return _reply(f"Done. I've requested cancellation of order {order_id}. "
                      f"Your request number is {req['request_id']}.")
    if status == "Shipped":
        return _reply(f"Order {order_id} has already shipped, so it can't be cancelled. "
                      "Once it arrives, ask me for a return and I'll start it.")
    req = create_service_request(order_id, "return")
    return _reply(f"I've started a return for order {order_id}. "
                  f"Your request number is {req['request_id']}.")