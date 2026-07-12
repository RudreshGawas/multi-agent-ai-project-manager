from utils.agent_factory import make_agent_node
from utils.context_builder import ContextBuilder
from prompts.sprint_prompt import get_sprint_prompt
from schemas.sprint_schema import SprintPlan

sprint_node = make_agent_node(
    context_fn=lambda state: ContextBuilder(state).build_sprint_context(),
    prompt_fn=get_sprint_prompt,
    schema=SprintPlan,
    state_key="sprint",
    node_name="Sprint Agent",
)