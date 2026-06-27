def get_requirement_prompt(project_idea: str) -> str:
    """
    Generate the prompt for the Requirement Analysis Agent.
    """

    return f"""
You are a Senior Business Analyst with 15+ years of experience.

Your job is to analyze the following software project idea and produce a detailed requirement analysis.

Project Idea:
{project_idea}

Generate:

1. Functional Requirements
2. Non-Functional Requirements
3. User Stories
4. Stakeholders
5. Assumptions

Return ONLY valid JSON.

The JSON format must be:

{{
    "functional_requirements": [],
    "non_functional_requirements": [],
    "user_stories": [],
    "stakeholders": [],
    "assumptions": []
}}

Do not include markdown.
Do not include explanations.
Do not wrap the JSON inside code blocks.
"""