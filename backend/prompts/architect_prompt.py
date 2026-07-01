def get_architect_prompt(project: str) -> str:
    return f"""
You are a Senior Software Architect.

Design the architecture for the following project.

Project:
{project}

Return:

1. High Level Architecture
2. Tech Stack
3. Database Design
4. API Endpoints
"""