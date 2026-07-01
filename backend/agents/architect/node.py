from graph.state import ProjectState

from prompts.architect_prompt import get_architect_prompt
from schemas.architect_schema import ArchitectureDesign
from services.llm_service import llm_service


def architect_node(state: ProjectState) -> ProjectState:
    
    prompt = get_architect_prompt(
        state["user_input"]
    )

    structured_llm = llm_service.get_structured_llm(
        ArchitectureDesign
    )

    response = structured_llm.invoke(prompt)

    state["architecture"] = response
    state["current_node"] = "Architect"
    state["status"] = "Completed"

    return state