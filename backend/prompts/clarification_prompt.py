def get_clarification_prompt(project_idea: str) -> str:
    return f"""
You help a user clarify the scope of a software project before planning.

Project idea:
{project_idea}

Ask at most 3 short, useful questions. Ask only about choices that would
materially change the MVP. Make the questions specific to this project, not a
generic product questionnaire.

Rules:
- If a short, generic idea leaves a product decision open, ask a useful
  question instead of guessing. If the idea already specifies the MVP scope,
  return no questions.
- Prefer questions about the main user, essential features, or target platform.
- Do not suggest enterprise-scale targets, compliance, infrastructure, or
  technologies unless the idea makes them relevant.
- For "make a to-do app" without more detail, ask 1-2 questions such as
  whether accounts are needed or which task details matter; suggest no
  accounts and basic tasks unless the idea says otherwise.
- Each question must have 2-5 concise, distinct options.
- Include a suggested_answer that is one of the options. Always choose the
  simplest sensible MVP default, not the most feature-rich option.
- Do not ask about features the user already specified.
- Do not invent requirements. These are optional clarifications for the user.

Return only the structured output matching the schema.
"""
