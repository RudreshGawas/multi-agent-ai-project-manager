from graph.state import ProjectState

from prompts.sprint_prompt import get_sprint_prompt
from schemas.sprint_schema import SprintPlan
from services.llm_service import llm_service


def sprint_node(state: ProjectState) -> ProjectState:
    
    prompt = get_sprint_prompt(
        state["user_input"]
    )

    structured_llm = llm_service.get_structured_llm(
        SprintPlan
    )

    response = structured_llm.invoke(prompt)

    state["sprint"] = response
    state["current_node"] = "Sprint"
    state["status"] = "Completed"

    return state