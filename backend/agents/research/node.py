# agents/research/node.py

from graph.state import ProjectState
from prompts.research_prompt import get_research_prompt
from schemas.research_schema import ResearchAnalysis
from services.llm_service import llm_service
from utils.context_builder import ContextBuilder


def research_node(state: ProjectState) -> ProjectState:
    try:
        builder = ContextBuilder(state)
        context = builder.build_research_context()

        prompt = get_research_prompt(**context)
        structured_llm = llm_service.get_structured_llm(ResearchAnalysis)
        research_analysis = structured_llm.invoke(prompt)

        state["research"] = research_analysis
        state["current_node"] = "Research Agent"
        state["status"] = "Completed"

    except Exception as e:
        state["error"] = f"Research Agent failed: {e}"
        state["status"] = "Error"

    return state