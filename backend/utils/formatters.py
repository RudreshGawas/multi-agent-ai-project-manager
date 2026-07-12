def format_requirements(requirements) -> str:
    fr = "\n".join(f"- {r}" for r in requirements.functional_requirements)
    nfr = "\n".join(f"- {r}" for r in requirements.non_functional_requirements)
    return f"""Functional Requirements:
{fr}

Non-Functional Requirements:
{nfr}"""


def format_research(research) -> str:
    def line(label, rec):
        return f"{label}: {rec.recommended} — {rec.reason}"

    best_practices = "\n".join(f"- {b}" for b in research.best_practices)

    return f"""{line("Backend", research.backend)}
{line("Frontend", research.frontend)}
{line("Database", research.database)}
{line("Authentication", research.authentication)}
{line("AI Framework", research.ai_framework)}
{line("Deployment", research.deployment)}

Best Practices:
{best_practices}"""


def format_architecture(architecture) -> str:
    tech = "\n".join(f"- {t}" for t in architecture.tech_stack)
    db = "\n".join(f"- {d}" for d in architecture.database_design)
    api = "\n".join(f"- {a}" for a in architecture.api_endpoints)

    return f"""System Architecture:
{architecture.system_architecture}

Tech Stack:
{tech}

Database Design:
{db}

API Endpoints:
{api}"""


def format_sprint(sprint) -> str:
    s1 = "\n".join(f"- {t}" for t in sprint.sprint_1)
    s2 = "\n".join(f"- {t}" for t in sprint.sprint_2)
    s3 = "\n".join(f"- {t}" for t in sprint.sprint_3)
    milestones = "\n".join(f"- {m}" for m in sprint.milestones)

    return f"""Sprint 1:
{s1}

Sprint 2:
{s2}

Sprint 3:
{s3}

Milestones:
{milestones}"""
