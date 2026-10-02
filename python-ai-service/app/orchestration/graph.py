from langgraph.graph import StateGraph, START, END

from app.orchestration.state import AgentState
from app.agents.manager_agent import manager_agent
from app.agents.faq_agent import faq_agent
from app.agents.complaint_agent import complaint_agent


def complaint_node(state: AgentState):
    result = complaint_agent(state["question"], state.get("company_id", "default"))
    return {
        "answer": result["answer"],
        "escalated": result["escalated"],
        "ticket_id": result["ticket_id"],
    }
CONFIDENCE_THRESHOLD = 0.5
SPECIALISTS = ["faq", "booking", "order", "complaint", "recommendation"]


def manager_node(state: AgentState):
    result = manager_agent(state["question"])
    return {"intent": result["intent"], "confidence": result["confidence"]}


def faq_node(state: AgentState):
    return {"answer": faq_agent(state["question"]), "escalated": False}


def escalation_node(state: AgentState):
    return {
        "answer": "Let me connect you with a human support representative.",
        "escalated": True,
    }


def placeholder_node(name: str):
    """Temporary stand-in until the real agent is built."""
    def node(state: AgentState):
        return {"answer": f"The {name} agent is not built yet.", "escalated": False}
    return node


def route_after_manager(state: AgentState):
    if state["intent"] == "human" or state["confidence"] < CONFIDENCE_THRESHOLD:
        return "escalation"
    return state["intent"]


def build_graph():
    g = StateGraph(AgentState)

    g.add_node("manager", manager_node)
    real_nodes = {"faq": faq_node, "complaint": complaint_node}
    for name in SPECIALISTS:
        g.add_node(name, real_nodes.get(name) or placeholder_node(name))
    g.add_node("escalation", escalation_node)

    g.add_edge(START, "manager")
    g.add_conditional_edges(
        "manager",
        route_after_manager,
        {name: name for name in SPECIALISTS + ["escalation"]},
    )
    for name in SPECIALISTS + ["escalation"]:
        g.add_edge(name, END)

    return g.compile()


graph = build_graph()