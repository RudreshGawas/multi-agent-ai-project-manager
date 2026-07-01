from typing import List
from pydantic import BaseModel


class TechnologyRecommendation(BaseModel):
    recommended: str
    reason: str
    alternatives: List[str]


class ResearchAnalysis(BaseModel):
    backend: TechnologyRecommendation
    frontend: TechnologyRecommendation
    database: TechnologyRecommendation
    authentication: TechnologyRecommendation
    ai_framework: TechnologyRecommendation
    deployment: TechnologyRecommendation
    best_practices: List[str]