try:
    from langgraph.graph import StateGraph, START, END
except ImportError:
    START = "__start__"
    END = "__end__"

    class _CompiledStateGraph:
        def __init__(self, nodes, edges, conditional_edges):
            self._nodes = dict(nodes)
            self._edges = dict(edges)
            self._conditional_edges = dict(conditional_edges)

        def invoke(self, state: dict) -> dict:
            current_state = dict(state)
            current_node = START
            while current_node != END:
                if current_node != START:
                    node_fn = self._nodes[current_node]
                    updates = node_fn(current_state)
                    if isinstance(updates, dict):
                        current_state.update(updates)
                if current_node in self._conditional_edges:
                    router_fn, mapping = self._conditional_edges[current_node]
                    route_key = router_fn(current_state)
                    current_node = mapping[route_key] if mapping else route_key
                elif current_node in self._edges:
                    current_node = self._edges[current_node]
                else:
                    break
            return current_state

    class StateGraph:
        def __init__(self, state_schema):
            self.state_schema = state_schema
            self._nodes = {}
            self._edges = {}
            self._conditional_edges = {}

        def add_node(self, name: str, action):
            if name in self._nodes:
                raise ValueError(f"Node `{name}` already present.")
            self._nodes[name] = action

        def add_edge(self, start_key: str, end_key: str):
            self._edges[start_key] = end_key

        def add_conditional_edges(self, source: str, path, path_map=None):
            self._conditional_edges[source] = (path, path_map)

        def compile(self):
            return _CompiledStateGraph(self._nodes, self._edges, self._conditional_edges)


from app.agents.order_agent import order_agent
from app.tools.orders import PENDING
from app.orchestration.state import AgentState
from app.agents.manager_agent import manager_agent
from app.agents.faq_agent import faq_agent
from app.agents.complaint_agent import complaint_agent
from app.agents.booking_agent import booking_agent
from app.agents.recommendation_agent import recommendation_agent
from app.agents.escalation_agent import escalation_agent
from app.tools.bookings import ACTIVE

CONFIDENCE_THRESHOLD = 0.5
SPECIALISTS = ["faq", "booking", "order", "complaint", "recommendation"]


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


def recommendation_node(state: AgentState):
    r = recommendation_agent(
        state["question"],
        state.get("company_id", "default"),
    )
    return {
        "answer": r["answer"],
        "escalated": r.get("escalated", False),
    }


def escalation_node(state: AgentState):
    r = escalation_agent(
        state["question"],
        company_id=state.get("company_id", "default"),
        session_id=state.get("session_id", "default"),
    )
    return {
        "answer": r["answer"],
        "escalated": r["escalated"],
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
    real_nodes = {
        "faq": faq_node,
        "complaint": complaint_node,
        "booking": booking_node,
        "order": order_node,
        "recommendation": recommendation_node,
    }
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