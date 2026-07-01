from graph.state import ProjectState

from prompts.documentation_prompt import get_documentation_prompt
from schemas.documentation_schema import Documentation
from services.llm_service import llm_service

print("\n===== DOCUMENTATION =====")
def documentation_node(state: ProjectState) -> ProjectState:
    print("\n===== DOCUMENTATION =====")
    prompt = get_documentation_prompt(
        state["user_input"]
    )

    structured_llm = llm_service.get_structured_llm(
        Documentation
    )

    response = structured_llm.invoke(prompt)

    state["documentation"] = response
    state["current_node"] = "Documentation"
    state["status"] = "Completed"

    return state