from typing import TypedDict, Optional


class ProjectState(TypedDict):
    """
    Shared state passed between all LangGraph agents.

    Every agent receives this state,
    updates it,
    and returns the updated version.
    """

    # User Input
    user_input: str

    # Requirement Agent Output
    requirements: Optional[dict]

    # Research Agent Output
    research: Optional[dict]

    # Architect Agent Output
    architecture: Optional[dict]

    # Final Supervisor Output
    final_report: Optional[dict]

    # Workflow Status
    current_agent: Optional[str]

    status: Optional[str]

    error: Optional[str]