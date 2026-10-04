from app.orchestration.graph import (
    CONFIDENCE_THRESHOLD,
    SPECIALISTS,
    route_after_manager,
    route_start,
)
from app.orchestration.state import AgentState


def resolve_entry_node(state: AgentState) -> str:
    """Determine the initial node for a conversation turn."""
    return route_start(state)


def resolve_specialist_node(state: AgentState) -> str:
    """Determine which specialist or escalation node handles the turn after classification."""
    target = route_after_manager(state)
    if target not in SPECIALISTS and target != "escalation":
        return "escalation"
    return target


__all__ = [
    "CONFIDENCE_THRESHOLD",
    "SPECIALISTS",
    "route_start",
    "route_after_manager",
    "resolve_entry_node",
    "resolve_specialist_node",
]
