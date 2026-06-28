from typing import List, Literal

from pydantic import BaseModel, Field


class SupervisorDecision(BaseModel):
    """
    Decision made by the Supervisor Agent.
    """

    next_agent: Literal[
        "requirement",
        "research",
        "architect",
        "documentation",
        "sprint",
        "end",
        "wait"
    ] = Field(
        ...,
        description="Next agent that should execute."
    )

    reason: str = Field(
        ...,
        description="Why this decision was made."
    )

    confidence: float = Field(
        ...,
        ge=0,
        le=1,
        description="Supervisor confidence score."
    )

    requires_user_input: bool = Field(
        ...,
        description="Whether additional information is required."
    )

    missing_information: List[str] = Field(
        default_factory=list,
        description="Missing information required from the user."
    )

    workflow_stage: str = Field(
        ...,
        description="Current stage of the workflow."
    )