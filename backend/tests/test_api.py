from datetime import datetime, timezone
import unittest
from unittest.mock import patch
from uuid import UUID

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)
PROJECT_ID = UUID("12345678-1234-5678-1234-567812345678")
CREATED_AT = datetime(2026, 10, 21, 12, 0, tzinfo=timezone.utc)


def successful_workflow_result() -> dict:
    recommendation = {
        "recommended": "Example",
        "reason": "Fits the project requirements.",
        "alternatives": ["Alternative A", "Alternative B"],
    }
    return {
        "requirements": {
            "functional_requirements": ["Create a project."],
            "non_functional_requirements": ["Protect user data."],
            "user_stories": ["As a user, I can create a project."],
            "stakeholders": ["User"],
            "assumptions": ["Users can access the internet."],
        },
        "research": {
            "backend": recommendation,
            "frontend": recommendation,
            "database": recommendation,
            "authentication": recommendation,
            "ai_framework": recommendation,
            "deployment": recommendation,
            "best_practices": ["Validate input."],
        },
        "architecture": {
            "system_architecture": "A modular web application.",
            "tech_stack": ["Python"],
            "database_design": ["Project has many tasks."],
            "api_endpoints": ["POST /projects"],
        },
        "sprint": {
            "sprint_1": ["Create project model."],
            "sprint_2": ["Implement project API."],
            "sprint_3": ["Add project UI."],
            "milestones": ["Project creation works."],
        },
        "documentation": {
            "srs": "Project requirements.",
            "project_proposal": "Project proposal.",
            "readme": "Project readme.",
        },
        "error": None,
    }


def saved_project() -> dict:
    result = successful_workflow_result()
    result.pop("error")
    return {
        "project_id": PROJECT_ID,
        "created_at": CREATED_AT,
        **result,
    }


class ApiTests(unittest.TestCase):
    def test_health_check(self):
        response = client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_api_allows_local_frontend_preflight(self):
        response = client.options(
            "/api/v1/projects/plan",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["access-control-allow-origin"],
            "http://localhost:3000",
        )

    def test_clarification_endpoint_returns_questions_for_the_project_idea(self):
        questions = {
            "questions": [
                {
                    "question": "Should tasks sync across devices?",
                    "options": ["No, save locally", "Yes, use accounts"],
                    "suggested_answer": "No, save locally",
                }
            ]
        }
        with patch(
            "main.llm_service.get_structured_llm"
        ) as get_structured_llm:
            get_structured_llm.return_value.invoke.return_value = questions
            response = client.post(
                "/api/v1/projects/clarify",
                json={"project_idea": "Make a to-do list app."},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), questions)
        get_structured_llm.assert_called_once()
        prompt = get_structured_llm.return_value.invoke.call_args.args[0]
        self.assertIn("Make a to-do list app.", prompt)

    def test_plan_endpoint_returns_and_persists_structured_plan(self):
        with (
            patch(
                "main.graph.invoke",
                return_value=successful_workflow_result(),
            ) as invoke,
            patch(
                "main.project_repository.save_project",
                return_value=saved_project(),
            ) as save_project,
            patch("main.project_repository.check_database_connection") as check_db,
        ):
            response = client.post(
                "/api/v1/projects/plan",
                json={"project_idea": " Build a project planning application. "},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            set(response.json()),
            {
                "project_id",
                "created_at",
                "requirements",
                "research",
                "architecture",
                "sprint",
                "documentation",
            },
        )
        self.assertEqual(
            invoke.call_args.args[0]["user_input"],
            "Build a project planning application.",
        )
        self.assertEqual(
            save_project.call_args.kwargs["project_idea"],
            "Build a project planning application.",
        )
        self.assertEqual(
            save_project.call_args.kwargs["plan"]["requirements"]["functional_requirements"],
            ["Create a project."],
        )
        self.assertEqual(response.json()["project_id"], str(PROJECT_ID))
        check_db.assert_called_once_with()

    def test_streaming_plan_endpoint_sends_agent_progress_and_plan(self):
        progress_events = [
            ("custom", {"agent": "research", "status": "working"}),
            ("custom", {"agent": "research", "status": "completed"}),
            ("values", successful_workflow_result()),
        ]
        with (
            patch(
                "main.progress_graph.stream",
                return_value=iter(progress_events),
            ),
            patch(
                "main.project_repository.save_project",
                return_value=saved_project(),
            ),
            patch("main.project_repository.check_database_connection"),
        ):
            response = client.post(
                "/api/v1/projects/plan/stream",
                json={"project_idea": "Build a project planning application."},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "text/event-stream; charset=utf-8")
        self.assertIn(
            '"type": "progress", "agent": "research", "status": "working"',
            response.text,
        )
        self.assertIn(
            '"type": "progress", "agent": "research", "status": "completed"',
            response.text,
        )
        self.assertIn('"type": "complete"', response.text)
        self.assertIn('"project_id": "12345678-1234-5678-1234-567812345678"', response.text)

    def test_streaming_plan_endpoint_passes_user_confirmed_scope_to_agents(self):
        with (
            patch(
                "main.progress_graph.stream",
                return_value=iter([("values", successful_workflow_result())]),
            ) as stream,
            patch(
                "main.project_repository.save_project",
                return_value=saved_project(),
            ),
            patch("main.project_repository.check_database_connection"),
        ):
            response = client.post(
                "/api/v1/projects/plan/stream",
                json={
                    "project_idea": "Make a to-do list app.",
                    "clarifications": [
                        {
                            "question": "Should tasks sync across devices?",
                            "answer": "No, save locally",
                        }
                    ],
                },
            )

        self.assertEqual(response.status_code, 200)
        workflow_input = stream.call_args.args[0]
        self.assertIn("Make a to-do list app.", workflow_input["user_input"])
        self.assertIn(
            "User-confirmed scope choices (treat these as requirements):",
            workflow_input["user_input"],
        )
        self.assertIn("No, save locally", workflow_input["user_input"])

    def test_get_project_endpoint_returns_saved_plan(self):
        with patch(
            "main.project_repository.get_project",
            return_value=saved_project(),
        ) as get_project:
            response = client.get(f"/api/v1/projects/{PROJECT_ID}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["project_id"], str(PROJECT_ID))
        get_project.assert_called_once_with(PROJECT_ID)

    def test_list_projects_returns_recent_project_summaries(self):
        projects = [
            {
                "project_id": PROJECT_ID,
                "project_idea": "Build a project planning application.",
                "created_at": CREATED_AT,
            }
        ]
        with patch(
            "main.project_repository.list_projects",
            return_value=projects,
        ) as list_projects:
            response = client.get("/api/v1/projects?limit=5")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["project_id"], str(PROJECT_ID))
        self.assertEqual(
            response.json()[0]["project_idea"],
            "Build a project planning application.",
        )
        list_projects.assert_called_once_with(limit=5)

    def test_list_projects_rejects_invalid_limit(self):
        response = client.get("/api/v1/projects?limit=101")

        self.assertEqual(response.status_code, 422)

    def test_get_project_endpoint_returns_not_found(self):
        with patch("main.project_repository.get_project", return_value=None):
            response = client.get(f"/api/v1/projects/{PROJECT_ID}")

        self.assertEqual(response.status_code, 404)

    def test_plan_endpoint_returns_service_unavailable_when_storage_fails(self):
        with (
            patch(
                "main.project_repository.save_project",
                side_effect=RuntimeError("Database unavailable"),
            ),
            patch("main.project_repository.check_database_connection"),
            patch(
                "main.graph.invoke",
                return_value=successful_workflow_result(),
            ),
            self.assertLogs("main", level="ERROR"),
        ):
            response = client.post(
                "/api/v1/projects/plan",
                json={"project_idea": "Build a project planning application."},
            )

        self.assertEqual(response.status_code, 503)
        self.assertIn("could not be saved", response.json()["detail"])

    def test_plan_endpoint_checks_database_before_running_workflow(self):
        with (
            patch(
                "main.project_repository.check_database_connection",
                side_effect=OSError("Database host not found"),
            ),
            patch("main.graph.invoke") as invoke,
            self.assertLogs("main", level="ERROR"),
        ):
            response = client.post(
                "/api/v1/projects/plan",
                json={"project_idea": "Build a project planning application."},
            )

        self.assertEqual(response.status_code, 503)
        self.assertIn("Check DATABASE_URL", response.json()["detail"])
        invoke.assert_not_called()

    def test_plan_endpoint_rejects_blank_ideas(self):
        response = client.post(
            "/api/v1/projects/plan",
            json={"project_idea": "   "},
        )

        self.assertEqual(response.status_code, 422)

    @patch(
        "main.graph.invoke",
        return_value={"error": "LLM unavailable", "current_node": "Requirement Node"},
    )
    def test_plan_endpoint_returns_gateway_error_on_workflow_failure(self, _invoke):
        with patch("main.project_repository.check_database_connection"):
            response = client.post(
                "/api/v1/projects/plan",
                json={"project_idea": "Build a project planning application."},
            )

        self.assertEqual(response.status_code, 502)
        self.assertIn("Please retry", response.json()["detail"])
        _invoke.assert_called_once()


if __name__ == "__main__":
    unittest.main()
