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

## Requirements
{format_requirements(requirements)}

## Research Decisions
{format_research(research)}

## Architecture
{format_architecture(architecture)}

## Sprint Plan
{format_sprint(sprint)}

Produce:
1. Software Requirement Specification (SRS)
2. Project Proposal
3. README

Return ONLY the structured output matching the provided schema.
"""