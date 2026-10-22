from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from schemas.architect_schema import ArchitectureDesign
from schemas.clarification_schema import ClarificationAnswer
from schemas.documentation_schema import Documentation
from schemas.requirement_schema import RequirementAnalysis
from schemas.research_schema import ResearchAnalysis
from schemas.sprint_schema import SprintPlan


class ProjectPlanRequest(BaseModel):
    project_idea: str = Field(
        min_length=1,
        max_length=10_000,
        description="A description of the software project to plan.",
    )
    clarifications: list[ClarificationAnswer] = Field(
        default_factory=list,
        max_length=3,
        description="Optional scope decisions confirmed by the user.",
    )

    @field_validator("project_idea")
    @classmethod
    def project_idea_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Project idea must not be blank.")
        return value


class ClarificationRequest(BaseModel):
    project_idea: str = Field(min_length=1, max_length=10_000)

    @field_validator("project_idea")
    @classmethod
    def project_idea_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Project idea must not be blank.")
        return value


class ProjectPlan(BaseModel):
    requirements: RequirementAnalysis
    research: ResearchAnalysis
    architecture: ArchitectureDesign
    sprint: SprintPlan
    documentation: Documentation


class ProjectPlanResponse(ProjectPlan):
    project_id: UUID
    created_at: datetime


class ProjectSummary(BaseModel):
    project_id: UUID
    project_idea: str
    created_at: datetime
