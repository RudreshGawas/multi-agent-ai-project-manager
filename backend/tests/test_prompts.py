from types import SimpleNamespace
import unittest

from prompts.architect_prompt import get_architect_prompt
from prompts.clarification_prompt import get_clarification_prompt
from prompts.documentation_prompt import get_documentation_prompt
from prompts.requirement_prompt import get_requirement_prompt
from prompts.research_prompt import get_research_prompt
from prompts.sprint_prompt import get_sprint_prompt


def sample_inputs():
    requirements = SimpleNamespace(
        functional_requirements=["Create and complete tasks."],
        non_functional_requirements=["Keep the interface easy to use."],
    )
    recommendation = SimpleNamespace(
        recommended="Not needed for the MVP",
        reason="The confirmed MVP does not need this capability.",
        alternatives=[],
    )
    research = SimpleNamespace(
        backend=recommendation,
        frontend=recommendation,
        database=recommendation,
        authentication=recommendation,
        ai_framework=recommendation,
        deployment=recommendation,
        best_practices=["Validate task input."],
    )
    architecture = SimpleNamespace(
        system_architecture="A simple application.",
        tech_stack=["Existing application stack"],
        database_design=["Task"],
        api_endpoints=["POST /tasks"],
    )
    sprint = SimpleNamespace(
        sprint_1=["Create tasks."],
        sprint_2=["Complete tasks."],
        sprint_3=["Polish the task list."],
        milestones=["A usable MVP."],
    )
    return requirements, research, architecture, sprint


class PromptScopeTests(unittest.TestCase):
    def test_clarification_prompt_is_specific_optional_and_capped(self):
        prompt = get_clarification_prompt("Make a to-do app.")

        self.assertIn("at most 3 short, useful questions", prompt)
        self.assertIn("return no questions", prompt)
        self.assertIn('For "make a to-do app"', prompt)
        self.assertIn("simplest sensible MVP default", prompt)

    def test_requirement_prompt_keeps_simple_ideas_at_mvp_scope(self):
        prompt = get_requirement_prompt("Make a simple to-do list app.")

        self.assertIn("A short or simple idea", prompt)
        self.assertIn("Do not add features", prompt)
        self.assertIn("Never invent numeric targets", prompt)
        self.assertIn("Put genuinely necessary but unstated assumptions", prompt)

    def test_research_prompt_allows_unused_categories(self):
        prompt = get_research_prompt(
            ["Create and complete tasks."],
            ["Keep the interface easy to use."],
        )

        self.assertIn("Not needed for the MVP", prompt)
        self.assertIn("Do not add AI to a non-AI product", prompt)
        self.assertIn("Do not over-engineer", prompt)

    def test_downstream_prompts_preserve_mvp_scope(self):
        requirements, research, architecture, sprint = sample_inputs()

        architecture_prompt = get_architect_prompt(
            requirements.functional_requirements,
            requirements.non_functional_requirements,
            research,
        )
        sprint_prompt = get_sprint_prompt(requirements, research, architecture)
        documentation_prompt = get_documentation_prompt(
            requirements,
            research,
            architecture,
            sprint,
        )

        self.assertIn("Keep the architecture proportional", architecture_prompt)
        self.assertIn("do not schedule it", sprint_prompt)
        self.assertIn("Do not claim code, tests,", documentation_prompt)
        self.assertIn("or milestones exist or have passed", documentation_prompt)
        self.assertIn("not an enterprise-length specification", documentation_prompt)


if __name__ == "__main__":
    unittest.main()
