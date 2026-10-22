import os
from typing import Any
from uuid import UUID, uuid4

import psycopg
from psycopg.types.json import Jsonb


CREATE_PROJECTS_TABLE = """
CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY,
    project_idea TEXT NOT NULL,
    plan JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
)
"""


def _database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL environment variable is not configured.")
    return database_url


def _connect_timeout() -> int:
    timeout = int(os.getenv("DB_CONNECT_TIMEOUT", "5"))
    if timeout < 1:
        raise ValueError("DB_CONNECT_TIMEOUT must be at least 1 second.")
    return timeout


def check_database_connection() -> None:
    with psycopg.connect(
        _database_url(),
        connect_timeout=_connect_timeout(),
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")


def save_project(project_idea: str, plan: dict[str, Any]) -> dict[str, Any]:
    project_id = uuid4()

    with psycopg.connect(
        _database_url(),
        connect_timeout=_connect_timeout(),
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_PROJECTS_TABLE)
            cursor.execute(
                """
                INSERT INTO projects (id, project_idea, plan)
                VALUES (%s, %s, %s)
                RETURNING created_at
                """,
                (project_id, project_idea, Jsonb(plan)),
            )
            row = cursor.fetchone()

    if row is None:
        raise RuntimeError("PostgreSQL did not return the saved project timestamp.")

    return {
        "project_id": project_id,
        "created_at": row[0],
        **plan,
    }


def get_project(project_id: UUID) -> dict[str, Any] | None:
    with psycopg.connect(
        _database_url(),
        connect_timeout=_connect_timeout(),
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_PROJECTS_TABLE)
            cursor.execute(
                """
                SELECT id, created_at, plan
                FROM projects
                WHERE id = %s
                """,
                (project_id,),
            )
            row = cursor.fetchone()

    if row is None:
        return None

    return {
        "project_id": row[0],
        "created_at": row[1],
        **row[2],
    }


def list_projects(limit: int = 20) -> list[dict[str, Any]]:
    with psycopg.connect(
        _database_url(),
        connect_timeout=_connect_timeout(),
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_PROJECTS_TABLE)
            cursor.execute(
                """
                SELECT id, project_idea, created_at
                FROM projects
                ORDER BY created_at DESC, id DESC
                LIMIT %s
                """,
                (limit,),
            )
            rows = cursor.fetchall()

    return [
        {
            "project_id": row[0],
            "project_idea": row[1],
            "created_at": row[2],
        }
        for row in rows
    ]
