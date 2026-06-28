from typing import Optional, TypedDict

from schemas.requirement_schema import RequirementAnalysis
from schemas.supervisor_schema import SupervisorDecision


class ProjectState(TypedDict):
    """
    Shared state passed between all LangGraph nodes.
    """

    user_input: str

    requirements: Optional[RequirementAnalysis]

    research: Optional[dict]

    architecture: Optional[dict]

    final_report: Optional[dict]

    supervisor_decision: Optional[SupervisorDecision]

    current_node: Optional[str]

    status: Optional[str]

    error: Optional[str]