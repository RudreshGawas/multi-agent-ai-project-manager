from langgraph.graph import END
from graph.state import ProjectState


def route_next_agent(state: ProjectState):
    """
    Route to the next stage selected by the supervisor.
    """

    if state.get("error") is not None:
        return END

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

    if next_agent in (
        "requirement",
        "research",
        "architect",
        "sprint",
        "documentation",
    ):
        return next_agent

    raise NotImplementedError(
        f"'{next_agent}' was selected by the Supervisor but is not registered "
        "as a graph node."
    )
    