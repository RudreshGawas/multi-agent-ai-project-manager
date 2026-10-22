import unittest
from unittest.mock import Mock, patch

from graph.workflow import graph
from schemas.architect_schema import ArchitectureDesign
from schemas.documentation_schema import Documentation
from schemas.requirement_schema import RequirementAnalysis
from schemas.research_schema import ResearchAnalysis, TechnologyRecommendation
from schemas.sprint_schema import SprintPlan


def initial_state() -> dict:
    return {
        "user_input": "Build a project planning application.",
        "requirements": None,
        "research": None,
        "architecture": None,
        "sprint": None,
        "documentation": None,
        "supervisor_decision": None,
        "current_node": None,
        "status": None,
        "error": None,
    }


def structured_outputs() -> dict:
    recommendation = TechnologyRecommendation(
        recommended="Example",
        reason="Fits the project requirements.",
        alternatives=["Alternative A", "Alternative B"],
    )
    return {
        RequirementAnalysis: RequirementAnalysis(
            functional_requirements=["Create a project."],
            non_functional_requirements=["Protect user data."],
            user_stories=["As a user, I can create a project."],
            stakeholders=["User"],
            assumptions=["Users can access the internet."],
        ),
        ResearchAnalysis: ResearchAnalysis(
            backend=recommendation,
            frontend=recommendation,
            database=recommendation,
            authentication=recommendation,
            ai_framework=recommendation,
            deployment=recommendation,
            best_practices=["Validate input."],
        ),
        ArchitectureDesign: ArchitectureDesign(
            system_architecture="A modular web application.",
            tech_stack=["Python"],
            database_design=["Project has many tasks."],
            api_endpoints=["POST /projects"],
        ),
        SprintPlan: SprintPlan(
            sprint_1=["Create project model."],
            sprint_2=["Implement project API."],
            sprint_3=["Add project UI."],
            milestones=["Project creation works."],
        ),
        Documentation: Documentation(
            srs="Project requirements.",
            project_proposal="Project proposal.",
            readme="Project readme.",
        ),
    }


class WorkflowTests(unittest.TestCase):
    def test_workflow_completes_all_agents_without_external_llm_calls(self):
        outputs = structured_outputs()

        def get_structured_llm(schema):
            response = Mock()
            response.invoke.return_value = outputs[schema]
            return response

        with patch(
            "services.llm_service.llm_service.get_structured_llm",
            side_effect=get_structured_llm,
        ):
            result = graph.invoke(initial_state())

        for key in (
            "requirements",
            "research",
            "architecture",
            "sprint",
            "documentation",
        ):
            self.assertIsNotNone(result[key], f"{key} should be generated")
        self.assertIsNone(result["error"])
        self.assertEqual(result["supervisor_decision"].next_agent, "end")

    def test_agent_failure_stops_workflow_with_error(self):
        with patch(
            "services.llm_service.llm_service.get_structured_llm",
            side_effect=RuntimeError("LLM unavailable"),
        ):
            result = graph.invoke(initial_state())

        self.assertEqual(result["status"], "Error")
        self.assertIn("LLM unavailable", result["error"])
        self.assertEqual(result["supervisor_decision"].next_agent, "end")
        self.assertIsNone(result["requirements"])


if __name__ == "__main__":
    unittest.main()
