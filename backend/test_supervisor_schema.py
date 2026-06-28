from schemas.supervisor_schema import SupervisorDecision

decision = SupervisorDecision(
    next_agent="requirement",
    reason="Requirements have not been generated yet.",
    confidence=0.98,
    requires_user_input=False,
    missing_information=[],
    workflow_stage="Requirement Analysis",
)

print(decision)