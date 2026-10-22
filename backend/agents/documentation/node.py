from graph.state import ProjectState

from utils.context_builder import ContextBuilder
from prompts.documentation_prompt import get_documentation_prompt
from schemas.documentation_schema import Documentation
from services.llm_service import llm_service


def documentation_node(state: ProjectState) -> ProjectState:
    try:
        context = ContextBuilder(state).build_documentation_context()
        prompt = get_documentation_prompt(**context)
        structured_llm = llm_service.get_structured_llm(Documentation)
        response = structured_llm.invoke(prompt)

        state["documentation"] = response
        state["current_node"] = "Documentation"
        state["status"] = "Completed"
        state["error"] = None
    except Exception as e:
        state["error"] = f"Documentation Agent failed: {e}"
        state["status"] = "Error"

    return state
