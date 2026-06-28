from langgraph.graph import StateGraph, START, END

from graph.state import ProjectState
from agents.requirement.node import requirement_node

builder = StateGraph(ProjectState)

builder.add_node(
    "requirement",
    requirement_node
)

builder.add_edge(
    START,
    "requirement"
)

builder.add_edge(
    "requirement",
    END
)

graph = builder.compile()