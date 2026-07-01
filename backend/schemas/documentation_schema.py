from pydantic import BaseModel


class Documentation(BaseModel):
    srs: str
    project_proposal: str
    readme: str