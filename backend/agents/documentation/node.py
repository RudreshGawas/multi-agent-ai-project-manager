from utils.agent_factory import make_agent_node
from utils.context_builder import ContextBuilder
from prompts.documentation_prompt import get_documentation_prompt
from schemas.documentation_schema import Documentation

documentation_node = make_agent_node(
    context_fn=lambda state: ContextBuilder(state).build_documentation_context(),
    prompt_fn=get_documentation_prompt,
    schema=Documentation,
    state_key="documentation",
    node_name="Documentation Agent",
)