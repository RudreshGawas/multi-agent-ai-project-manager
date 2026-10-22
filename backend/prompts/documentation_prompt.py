from utils.formatters import (
    format_requirements,
    format_research,
    format_architecture,
    format_sprint,
)


def get_documentation_prompt(requirements, research, architecture, sprint) -> str:
    return f"""
You are a Technical Documentation Expert producing final documentation for this project,
based entirely on the decisions already made in previous phases below.

Stay faithful to the requested MVP and the supplied decisions. Do not add
features, technologies, integrations, numeric targets, budgets, staffing,
security certifications, uptime/performance guarantees, or implementation
details that the earlier phases did not establish. Do not claim code, tests,
deployments, or milestones exist or have passed when they have not.
Keep each document concise and useful for the actual project: an SRS summary,
a short project proposal, and a practical README. For a small MVP, each should
be a few sections, not an enterprise-length specification. Do not add fake
status badges, fictional repository URLs, or setup instructions for
unselected technologies.

## Requirements
{format_requirements(requirements)}

## Research Decisions
{format_research(research)}

## Architecture
{format_architecture(architecture)}

## Sprint Plan
{format_sprint(sprint)}

Produce:
1. A concise Software Requirement Specification (SRS) covering the confirmed
   MVP scope and any clearly labeled assumptions
2. A short project proposal that explains the requested problem and solution
3. A practical README with only the selected stack and verified setup steps

Return ONLY the structured output matching the provided schema.
"""