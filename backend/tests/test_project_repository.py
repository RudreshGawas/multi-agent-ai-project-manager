import os
import unittest
from datetime import datetime, timezone
from unittest.mock import Mock, patch
from uuid import UUID

from services import project_repository


PROJECT_ID = UUID("12345678-1234-5678-1234-567812345678")
CREATED_AT = datetime(2026, 10, 21, 12, 0, tzinfo=timezone.utc)


class ProjectRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.connection = Mock()
        self.connection.__enter__ = Mock(return_value=self.connection)
        self.connection.__exit__ = Mock(return_value=False)
        self.cursor = Mock()
        self.cursor.__enter__ = Mock(return_value=self.cursor)
        self.cursor.__exit__ = Mock(return_value=False)
        self.connection.cursor.return_value = self.cursor

    @patch.dict(os.environ, {"DATABASE_URL": "postgresql://user:pass@localhost/db"})
    @patch("services.project_repository.uuid4", return_value=PROJECT_ID)
    @patch("services.project_repository.psycopg.connect")
    def test_save_project_inserts_json_plan_and_returns_id(self, connect, uuid4):
        self.cursor.fetchone.return_value = (CREATED_AT,)
        connect.return_value = self.connection

        result = project_repository.save_project(
            "Project idea",
            {"requirements": {"functional_requirements": ["Create a project."]}},
        )

        self.assertEqual(result["project_id"], PROJECT_ID)
        self.assertEqual(result["created_at"], CREATED_AT)
        insert_sql, insert_params = self.cursor.execute.call_args_list[1].args
        self.assertIn("INSERT INTO projects", insert_sql)
        self.assertEqual(insert_params[0], PROJECT_ID)
        self.assertEqual(insert_params[1], "Project idea")
        self.assertEqual(
            insert_params[2].obj,
            {"requirements": {"functional_requirements": ["Create a project."]}},
        )
        uuid4.assert_called_once_with()

    @patch.dict(os.environ, {"DATABASE_URL": "postgresql://user:pass@localhost/db"})
    @patch("services.project_repository.psycopg.connect")
    def test_get_project_returns_none_for_missing_id(self, connect):
        self.cursor.fetchone.return_value = None
        connect.return_value = self.connection

        result = project_repository.get_project(PROJECT_ID)

        self.assertIsNone(result)
        query, params = self.cursor.execute.call_args_list[1].args
        self.assertIn("WHERE id = %s", query)
        self.assertEqual(params, (PROJECT_ID,))

    @patch.dict(os.environ, {"DATABASE_URL": "postgresql://user:pass@localhost/db"})
    @patch("services.project_repository.psycopg.connect")
    def test_list_projects_returns_recent_project_summaries(self, connect):
        row = (PROJECT_ID, "Project idea", CREATED_AT)
        self.cursor.fetchall.return_value = [row]
        connect.return_value = self.connection

        result = project_repository.list_projects(limit=7)

        self.assertEqual(
            result,
            [
                {
                    "project_id": PROJECT_ID,
                    "project_idea": "Project idea",
                    "created_at": CREATED_AT,
                }
            ],
        )
        query, params = self.cursor.execute.call_args_list[1].args
        self.assertIn("ORDER BY created_at DESC", query)
        self.assertIn("LIMIT %s", query)
        self.assertEqual(params, (7,))

    @patch.dict(
        os.environ,
        {
            "DATABASE_URL": "postgresql://user:pass@localhost/db",
            "DB_CONNECT_TIMEOUT": "3",
        },
    )
    @patch("services.project_repository.psycopg.connect")
    def test_connection_check_uses_configured_timeout(self, connect):
        connect.return_value = self.connection

        project_repository.check_database_connection()

        connect.assert_called_once_with(
            "postgresql://user:pass@localhost/db",
            connect_timeout=3,
        )
        self.cursor.execute.assert_called_once_with("SELECT 1")

    @patch.dict(
        os.environ,
        {
            "DATABASE_URL": "postgresql://user:pass@localhost/db",
            "DB_CONNECT_TIMEOUT": "0",
        },
    )
    def test_connection_timeout_must_be_positive(self):
        with self.assertRaisesRegex(ValueError, "at least 1 second"):
            project_repository.check_database_connection()

    @patch.dict(os.environ, {}, clear=True)
    def test_database_url_is_required(self):
        with self.assertRaisesRegex(RuntimeError, "DATABASE_URL"):
            project_repository.get_project(PROJECT_ID)


if __name__ == "__main__":
    unittest.main()
