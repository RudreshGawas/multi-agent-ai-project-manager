from langgraph.graph import END
from graph.state import ProjectState


def route_next_agent(state: ProjectState):
    """
    Deterministic router for the current pipeline (Requirement -> Research -> End).
    No LLM call needed here — this logic doesn't require judgment yet.
    """

    decision = state.get("supervisor_decision")

    if decision is None:
        raise ValueError("SupervisorDecision not found in ProjectState.")

    next_agent = decision.next_agent

    if next_agent == "end":
        return END

    if next_agent == "wait":
        # Not an error — the system correctly determined it needs more info.
        # For now, end the run and let the caller check `requires_user_input`.
        return END

    if next_agent in ("requirement", "research", "architect", "sprint", "documentation"):
        return next_agent

    # Supervisor picked a real pipeline stage that isn't wired into the graph yet
    # (architect / sprint / documentation). This is OUR bug, not a user error —
    # fail loudly so we notice it immediately during dev, not silently in prod.
    raise NotImplementedError(
        f"'{next_agent}' was selected by the Supervisor but is not yet "
        f"registered as a graph node."
    )
    