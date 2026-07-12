from langgraph.graph import StateGraph, START, END

from graph.state import ProjectState
from graph.router import route_next_agent

from agents.supervisor.node import supervisor_node
from agents.requirement.node import requirement_node
from agents.research.node import research_node
from agents.architect.node import architect_node
from agents.sprint.node import sprint_node
from agents.documentation.node import documentation_node

builder = StateGraph(ProjectState)

# Nodes
builder.add_node("supervisor", supervisor_node)
builder.add_node("requirement", requirement_node)
builder.add_node("research", research_node)
builder.add_node("architect", architect_node)
builder.add_node("sprint", sprint_node)
builder.add_node("documentation", documentation_node)

# Start
builder.add_edge(START, "supervisor")

# Supervisor routing
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

# Return to supervisor
builder.add_edge("requirement", "supervisor")
builder.add_edge("research", "supervisor")
builder.add_edge("architect", "supervisor")
builder.add_edge("sprint", "supervisor")
builder.add_edge("documentation", "supervisor")

graph = builder.compile()