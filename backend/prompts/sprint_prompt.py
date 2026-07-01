def get_sprint_prompt(project_description: str) -> str:
    return f"""
You are an Agile Project Manager.

Create a 3 Sprint roadmap.

Project:
{project_description}

Return:

1. Sprint 1 Tasks
2. Sprint 2 Tasks
3. Sprint 3 Tasks
4. Major Milestones

Return structured output only.
"""