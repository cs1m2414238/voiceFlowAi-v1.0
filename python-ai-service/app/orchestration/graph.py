from langgraph.graph import StateGraph, START, END
from app.agents.order_agent import order_agent
from app.tools.orders import PENDING
from app.orchestration.state import AgentState
from app.agents.manager_agent import manager_agent
from app.agents.faq_agent import faq_agent
from app.agents.complaint_agent import complaint_agent
from app.agents.booking_agent import booking_agent
from app.tools.bookings import ACTIVE
from app.agents.recommendation_agent import recommendation_agent

CONFIDENCE_THRESHOLD = 0.5
SPECIALISTS = ["faq", "booking", "order", "complaint", "recommendation"]

def recommendation_node(state: AgentState):
    r = recommendation_agent(state["question"], state.get("company_id", "default"))
    return {"answer": r["answer"], "escalated": r["escalated"]}

def manager_node(state: AgentState):
    result = manager_agent(state["question"])
    return {"intent": result["intent"], "confidence": result["confidence"]}


def faq_node(state: AgentState):
    return {"answer": faq_agent(state["question"]), "escalated": False}


def complaint_node(state: AgentState):
    r = complaint_agent(state["question"], state.get("company_id", "default"))
    return {
        "answer": r["answer"],
        "escalated": r["escalated"],
        "ticket_id": r["ticket_id"],
    }


def booking_node(state: AgentState):
    r = booking_agent(
        state["question"],
        state.get("session_id", "default"),
        state.get("company_id", "default"),
    )
    return {
        "intent": "booking",
        "confidence": state.get("confidence", 1.0),
        "answer": r["answer"],
        "escalated": r["escalated"],
        "booking_id": r["booking_id"],
    }


def escalation_node(state: AgentState):
    return {
        "answer": "Let me connect you with a human support representative.",
        "escalated": True,
    }


def placeholder_node(name: str):
    def node(state: AgentState):
        return {"answer": f"The {name} agent is not built yet.", "escalated": False}
    return node

def order_node(state: AgentState):
    r = order_agent(
        state["question"],
        state.get("session_id", "default"),
        state.get("company_id", "default"),
    )
    return {
        "intent": "order",
        "confidence": state.get("confidence", 1.0),
        "answer": r["answer"],
        "escalated": r["escalated"],
    }

def route_start(state: AgentState):
    """Skip the Manager when this session is mid-booking or mid-order."""
    session = state.get("session_id")
    if session in ACTIVE:
        return "booking"
    if session in PENDING:
        return "order"
    return "manager"


def route_after_manager(state: AgentState):
    if state["intent"] == "human" or state["confidence"] < CONFIDENCE_THRESHOLD:
        return "escalation"
    return state["intent"]


def build_graph():
    g = StateGraph(AgentState)

    g.add_node("manager", manager_node)
    real_nodes = {"faq": faq_node, "complaint": complaint_node,
                  "booking": booking_node, "order": order_node,
                  "recommendation": recommendation_node}
    for name in SPECIALISTS:
        g.add_node(name, real_nodes.get(name) or placeholder_node(name))
    g.add_node("escalation", escalation_node)

    g.add_conditional_edges(
        START, route_start,
        {"manager": "manager", "booking": "booking", "order": "order"},
    )
    g.add_conditional_edges(
        "manager",
        route_after_manager,
        {name: name for name in SPECIALISTS + ["escalation"]},
    )
    for name in SPECIALISTS + ["escalation"]:
        g.add_edge(name, END)

    return g.compile()


graph = build_graph()