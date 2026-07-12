from graph.state import ProjectState
from services.llm_service import llm_service


def make_agent_node(context_fn, prompt_fn, schema, state_key: str, node_name: str):
    """
    Builds a LangGraph node function from its four moving parts:
    - context_fn: takes state, returns a dict of kwargs for prompt_fn
    - prompt_fn: takes those kwargs, returns the prompt string
    - schema: the Pydantic schema for structured output
    - state_key: which ProjectState field this agent's result gets stored in
    - node_name: label recorded in state["current_node"]
    """

    def node(state: ProjectState) -> ProjectState:
        try:
            context = context_fn(state)
            prompt = prompt_fn(**context)

            structured_llm = llm_service.get_structured_llm(schema)
            result = structured_llm.invoke(prompt)

            state[state_key] = result
            state["current_node"] = node_name
            state["status"] = "Completed"
            state["error"] = None

        except Exception as e:
            state["error"] = f"{node_name} failed: {e}"
            state["status"] = "Error"

        return state

    return node
