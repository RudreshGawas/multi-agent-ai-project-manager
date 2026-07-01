from langgraph.graph import StateGraph, START, END

from graph.state import ProjectState
from graph.router import route_next_agent

from agents.supervisor.node import supervisor_node
from agents.requirement.node import requirement_node
from agents.research.node import research_node


builder = StateGraph(ProjectState)

# -------------------------
# Add Nodes
# -------------------------

builder.add_node("supervisor", supervisor_node)
builder.add_node("requirement", requirement_node)
builder.add_node("research", research_node)

# -------------------------
# Start
# -------------------------

builder.add_edge(
    START,
    "supervisor"
)

# -------------------------
# Conditional Routing
# -------------------------

builder.add_conditional_edges(
    "supervisor",
    route_next_agent,
    {
        "requirement": "requirement",
        "research": "research",
        END: END,
    },
)

# -------------------------
# Return to Supervisor
# -------------------------

builder.add_edge("requirement", "supervisor")
builder.add_edge("research", "supervisor")

graph = builder.compile()