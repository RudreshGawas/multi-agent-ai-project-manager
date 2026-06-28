from graph.state import ProjectState

from prompts.supervisor_prompt import get_supervisor_prompt
from schemas.supervisor_schema import SupervisorDecision
from services.llm_service import llm_service
from utils.state_formatter import format_project_state


def supervisor_node(state: ProjectState) -> ProjectState:
    """
    Supervisor Agent

    Responsible for deciding which agent
    should execute next.
    """

    # Format state for the LLM
    formatted_state = format_project_state(state)

    # Build prompt
    prompt = get_supervisor_prompt(formatted_state)

    # Structured LLM
    structured_llm = llm_service.get_structured_llm(
        SupervisorDecision
    )

    # Make decision
    decision = structured_llm.invoke(prompt)

    # Update shared state
    state["supervisor_decision"] = decision
    state["current_node"] = "Supervisor"
    state["status"] = "Decision Completed"

    return state