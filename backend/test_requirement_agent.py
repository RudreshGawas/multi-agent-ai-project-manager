from agents.requirement.node import requirement_node

state = {
    "user_input": """
Build an AI-powered Physiotherapy Platform
where patients perform exercises using pose estimation
and therapists monitor patient progress remotely.
""",
    "requirements": None,
    "research": None,
    "architecture": None,
    "sprint": None,
    "documentation": None,
    "supervisor_decision": None,
    "current_node": None,
    "status": None,
    "error": None,
}

result = requirement_node(state)

print(type(result["requirements"]))
print()
print(result["requirements"].functional_requirements)
print()
print(result["requirements"].user_stories)