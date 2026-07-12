from utils.formatters import format_research


def get_architect_prompt(
    functional_requirements: list[str],
    non_functional_requirements: list[str],
    research,
) -> str:
    fr_text = "\n".join(f"- {r}" for r in functional_requirements)
    nfr_text = "\n".join(f"- {r}" for r in non_functional_requirements)
    research_text = format_research(research)

    return f"""
You are a Senior Software Architect designing the system architecture for this project.

IMPORTANT: The technology choices below were already decided by the Research phase.
Your architecture MUST be consistent with them. Do not introduce or substitute different
technologies — design around what has already been chosen.

## Functional Requirements
{fr_text}

## Non-Functional Requirements
{nfr_text}

## Research Recommendations (fixed constraints — do not contradict)
{research_text}

Produce:
1. A high-level system architecture description
2. The confirmed tech stack (must match the research recommendations above)
3. Database design — key entities and relationships
4. Core API endpoints required

Return ONLY the structured output matching the provided schema.
"""