from typing import TypedDict

from schemas.requirement_schema import RequirementAnalysis
from schemas.research_schema import ResearchAnalysis
from schemas.architect_schema import ArchitectureDesign
from schemas.sprint_schema import SprintPlan
from schemas.documentation_schema import Documentation
from schemas.supervisor_schema import SupervisorDecision


class ProjectState(TypedDict):
    """
    Shared state passed between all LangGraph nodes.
    """

    # User Input
    user_input: str

    # Agent Outputs
    requirements: RequirementAnalysis | None
    research: ResearchAnalysis | None
    architecture: ArchitectureDesign | None
    sprint: SprintPlan | None
    documentation: Documentation | None

    # Supervisor
    supervisor_decision: SupervisorDecision | None

    # Workflow Metadata
    current_node: str | None
    status: str | None
    error: str | None