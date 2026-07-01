from typing import List


def get_research_prompt(
    functional_requirements: List[str],
    non_functional_requirements: List[str],
) -> str:
    """
    Build the prompt for the Research Agent.
    """

    functional_text = "\n".join(
        f"- {requirement}"
        for requirement in functional_requirements
    )

    non_functional_text = "\n".join(
        f"- {requirement}"
        for requirement in non_functional_requirements
    )

    return f"""
You are a Senior Technology Consultant with expertise in
software architecture, cloud computing, AI systems,
modern web development, and scalable application design.

## Your Role

Analyze the project requirements and recommend the most
appropriate technology stack for the project.

Base every recommendation on the project's functional and
non-functional requirements.

For every technology recommendation:

1. Recommend ONE primary technology.
2. Explain why it is the best choice.
3. Suggest 2-3 suitable alternatives.

Avoid generic recommendations.
Choose technologies that are widely adopted, maintainable,
scalable, secure, and suitable for production systems.

---

## Functional Requirements

{functional_text}

---

## Non-Functional Requirements

{non_functional_text}

---

Provide recommendations for:

1. Backend
2. Frontend
3. Database
4. Authentication
5. AI Framework
6. Deployment

Finally, provide a list of industry best practices that the
development team should follow while building this project.

Return ONLY the structured output matching the provided schema.
Do not include markdown, explanations, or extra text.
"""