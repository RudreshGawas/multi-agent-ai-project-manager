print("\n========== RESEARCH ==========")
from graph.state import ProjectState

from prompts.research_prompt import get_research_prompt
from schemas.research_schema import ResearchAnalysis
from services.llm_service import llm_service
from utils.context_builder import ContextBuilder


def research_node(state: ProjectState) -> ProjectState:
    """
    Research Agent

    Input:
        RequirementAnalysis

    Output:
        ResearchAnalysis

    Responsibilities:
        1. Extract the required context.
        2. Build the research prompt.
        3. Invoke the LLM with structured output.
        4. Store the research analysis in ProjectState.
    """
    
    # Build Context
    builder = ContextBuilder(state)
    context = builder.build_research_context()

    # Build Prompt
    prompt = get_research_prompt(**context)

    # Configure Structured LLM
    structured_llm = llm_service.get_structured_llm(
        ResearchAnalysis
    )

    # Generate Research Analysis
    research_analysis = structured_llm.invoke(prompt)

    # Update State
    state["research"] = research_analysis
    state["current_node"] = "Research Agent"
    state["status"] = "Completed"

    return state
    print("Research Agent Finished")