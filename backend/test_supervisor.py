from agents.supervisor.node import supervisor_node

state = {
    "user_input": """
Build an AI-powered Physiotherapy Platform
where patients perform exercises using pose estimation
and therapists can monitor progress remotely.
""",

    "requirements": None,
    "research": None,
    "architecture": None,
    "final_report": None,

    "supervisor_decision": None,

    "current_node": None,
    "status": None,
    "error": None,
}

updated_state = supervisor_node(state)

print(updated_state["supervisor_decision"])