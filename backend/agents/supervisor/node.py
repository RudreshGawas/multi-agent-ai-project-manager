# agents/supervisor/node.py

from graph.state import ProjectState
from prompts.supervisor_prompt import get_supervisor_prompt
from schemas.supervisor_schema import SupervisorDecision
from services.llm_service import llm_service
from utils.state_formatter import format_project_state


def _deterministic_decision(state: ProjectState) -> SupervisorDecision | None:
    """
    Handles the unambiguous cases without spending an LLM call.
    Returns None if the situation is ambiguous and needs real judgment.
    """
    if state.get("requirements") is None:
        return SupervisorDecision(
            next_agent="requirement",
            reason="Requirements have not been generated yet.",
            confidence=1.0,
            requires_user_input=False,
            missing_information=[],
            workflow_stage="Requirement Analysis",
        )

    if state.get("research") is None:
        return SupervisorDecision(
            next_agent="research",
            reason="Requirements exist but research is missing.",
            confidence=1.0,
            requires_user_input=False,
            missing_information=[],
            workflow_stage="Research",
        )

    if state.get("architecture") is None:
        return SupervisorDecision(
            next_agent="architect",
            reason="Research exists but architecture design is missing.",
            confidence=1.0,
            requires_user_input=False,
            missing_information=[],
            workflow_stage="Architecture Design",
        )

    if state.get("sprint") is None:
        return SupervisorDecision(
            next_agent="sprint",
            reason="Architecture design exists but sprint plan is missing.",
            confidence=1.0,
            requires_user_input=False,
            missing_information=[],
            workflow_stage="Sprint Planning",
        )

    if state.get("documentation") is None:
        return SupervisorDecision(
            next_agent="documentation",
            reason="Sprint plan exists but documentation is missing.",
            confidence=1.0,
            requires_user_input=False,
            missing_information=[],
            workflow_stage="Documentation",
        )

    return SupervisorDecision(
        next_agent="end",
        reason="All workflow stages (requirements, research, architecture, sprint, and documentation) are complete.",
        confidence=1.0,
        requires_user_input=False,
        missing_information=[],
        workflow_stage="Complete",
    )


def supervisor_node(state: ProjectState) -> ProjectState:
    try:
        decision = _deterministic_decision(state)

        state["supervisor_decision"] = decision
        state["current_node"] = "Supervisor"
        state["status"] = "Decision Completed"

    except Exception as e:
        state["error"] = f"Supervisor failed: {e}"
        state["status"] = "Error"

    return state