from typing import List
from pydantic import BaseModel


class ArchitectureDesign(BaseModel):
    system_architecture: str
    tech_stack: List[str]
    database_design: List[str]
    api_endpoints: List[str]