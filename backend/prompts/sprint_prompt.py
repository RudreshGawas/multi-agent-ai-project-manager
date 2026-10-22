from utils.formatters import format_requirements, format_research, format_architecture


def get_sprint_prompt(requirements, research, architecture) -> str:
    return f"""
You are an Agile Project Manager creating a 3-sprint roadmap for this project.

Base every task on the requirements, technology decisions, and architecture below —
do not invent scope that isn't grounded in them.
Treat the requirements as the scope boundary. Do not add optional ideas,
speculative infrastructure, unrequested authentication, AI, notifications,
analytics, deployment work, or load testing. Prefer a usable end-to-end MVP
over production-scale work. Keep each sprint to 3-5 concrete, achievable tasks.
If a capability is marked "Not needed for the MVP", do not schedule it.
Do not claim that unimplemented or untested milestones are already complete.

## Requirements
{format_requirements(requirements)}

## Research Decisions
{format_research(research)}

## Architecture
{format_architecture(architecture)}

Produce:
1. Sprint 1 tasks
2. Sprint 2 tasks
3. Sprint 3 tasks
4. Major milestones

Return ONLY the structured output matching the provided schema.
"""