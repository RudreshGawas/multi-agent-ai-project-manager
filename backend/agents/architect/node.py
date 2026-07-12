from utils.agent_factory import make_agent_node
from utils.context_builder import ContextBuilder
from prompts.architect_prompt import get_architect_prompt
from schemas.architect_schema import ArchitectureDesign

architect_node = make_agent_node(
    context_fn=lambda state: ContextBuilder(state).build_architect_context(),
    prompt_fn=get_architect_prompt,
    schema=ArchitectureDesign,
    state_key="architecture",
    node_name="Architect Agent",
)