from typing import List
from pydantic import BaseModel


class SprintPlan(BaseModel):
    sprint_1: List[str]
    sprint_2: List[str]
    sprint_3: List[str]
    milestones: List[str]