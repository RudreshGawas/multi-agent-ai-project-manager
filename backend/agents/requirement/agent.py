from prompts.requirement_prompt import get_requirement_prompt
from schemas.requirement_schema import RequirementAnalysis
from services.llm_service import llm_service


class RequirementAgent:
    """
    AI agent responsible for analyzing project requirements.
    """

    def __init__(self):
        self.llm = llm_service.get_structured_llm(
            RequirementAnalysis
        )

    def analyze(self, project_idea: str) -> RequirementAnalysis:
        """
        Analyze the project idea and return
        structured requirements.
        """

        prompt = get_requirement_prompt(project_idea)

        response = self.llm.invoke(prompt)

        return response