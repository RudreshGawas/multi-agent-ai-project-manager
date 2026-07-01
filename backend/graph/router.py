from langgraph.graph import END

from graph.state import ProjectState


def route_next_agent(state: ProjectState):
    """
    Route the workflow based on the Supervisor Agent's decision.
    """

    decision = state.get("supervisor_decision")

    if decision is None:
        raise ValueError(
            "SupervisorDecision not found in ProjectState."
        )

    if decision.next_agent == "end":
        return END

    if decision.next_agent in ("requirement", "research"):
        return decision.next_agent

    raise ValueError(
        f"Unsupported next agent: {decision.next_agent}"
    )