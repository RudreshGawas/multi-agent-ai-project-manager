def get_documentation_prompt(project_description: str) -> str:
    return f"""
You are a Technical Documentation Expert.

Generate documentation for the following project.

Project:
{project_description}

Return:

1. Software Requirement Specification
2. Project Proposal
3. README

Return structured output only.
"""