# agents/requirement/node.py

from graph.state import ProjectState
from prompts.requirement_prompt import get_requirement_prompt
from schemas.requirement_schema import RequirementAnalysis
from services.llm_service import llm_service


def requirement_node(state: ProjectState) -> ProjectState:
    try:
        structured_llm = llm_service.get_structured_llm(RequirementAnalysis)
        prompt = get_requirement_prompt(state["user_input"])
        result = structured_llm.invoke(prompt)

        state["requirements"] = result
        state["current_node"] = "Requirement Node"
        state["status"] = "Completed"

    except Exception as e:
        state["error"] = f"Requirement Agent failed: {e}"
        state["status"] = "Error"

    return state
