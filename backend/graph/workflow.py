from collections.abc import Callable

from langgraph.graph import StateGraph, START, END
from langgraph.config import get_stream_writer

from graph.state import ProjectState
from graph.router import route_next_agent

from agents.supervisor.node import supervisor_node
from agents.requirement.node import requirement_node
from agents.research.node import research_node
from agents.architect.node import architect_node
from agents.sprint.node import sprint_node
from agents.documentation.node import documentation_node


def _with_progress(
    agent_name: str,
    node: Callable[[ProjectState], ProjectState],
) -> Callable[[ProjectState], ProjectState]:
    def run(state: ProjectState) -> ProjectState:
        writer = get_stream_writer()
        writer({"agent": agent_name, "status": "working"})
        result = node(state)
        writer(
            {
                "agent": agent_name,
                "status": "error" if result.get("error") is not None else "completed",
            }
        )
        return result

    return run


def _build_graph(with_progress: bool = False):
    builder = StateGraph(ProjectState)

    agents = {
        "requirement": ("requirements", requirement_node),
        "research": ("research", research_node),
        "architect": ("architecture", architect_node),
        "sprint": ("sprint", sprint_node),
        "documentation": ("documentation", documentation_node),
    }
    builder.add_node("supervisor", supervisor_node)
    for node_name, (agent_name, node) in agents.items():
        builder.add_node(
            node_name,
            _with_progress(agent_name, node) if with_progress else node,
        )

    builder.add_edge(START, "supervisor")
    builder.add_conditional_edges(
        "supervisor",
        route_next_agent,
        {
            "requirement": "requirement",
            "research": "research",
            "architect": "architect",
            "sprint": "sprint",
            "documentation": "documentation",
            END: END,
        },
    )
    for node_name in agents:
        builder.add_edge(node_name, "supervisor")

    return builder.compile()


graph = _build_graph()
progress_graph = _build_graph(with_progress=True)