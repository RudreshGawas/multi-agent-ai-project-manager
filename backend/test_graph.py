from graph.workflow import graph

result = graph.invoke(
    {
        "user_input": """
Build an AI-powered Physiotherapy Platform
where patients perform exercises using pose estimation
and therapists can monitor patient progress remotely.
""",
        "requirements": None,
        "research": None,
        "architecture": None,
        "final_report": None,
        "current_node": None,
        "status": None,
        "error": None,
    }
)

print(result)