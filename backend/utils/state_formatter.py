from graph.state import ProjectState


def format_project_state(state: ProjectState) -> str:
    """
    Convert ProjectState into a human-readable summary
    for the Supervisor Agent.
    """

    return f"""
==========================
PROJECT STATUS
==========================

Project Idea:
{state["user_input"]}

Current Progress

Requirements:
{"✅ Completed" if state.get("requirements") else "❌ Missing"}

Research:
{"✅ Completed" if state.get("research") else "❌ Missing"}

Architecture:
{"✅ Completed" if state.get("architecture") else "❌ Missing"}

Documentation:
{"✅ Completed" if state.get("documentation") else "❌ Missing"}

Current Node:
{state.get("current_node", "None")}

Status:
{state.get("status", "Not Started")}
"""