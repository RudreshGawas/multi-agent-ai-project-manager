from graph.workflow import graph

initial_state = {
    "user_input": """
Build an AI-powered Physiotherapy Platform
where patients perform exercises using pose estimation
and therapists can monitor patient progress remotely.
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

result = graph.invoke(initial_state)

print("\n========== FINAL STATE ==========\n")

for key, value in result.items():
    print(f"{key}:\n{value}\n")