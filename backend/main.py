import json
import logging
import os
from uuid import UUID

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from graph.workflow import graph, progress_graph
from prompts.clarification_prompt import get_clarification_prompt
from schemas.api_schema import (
    ClarificationRequest,
    ProjectPlan,
    ProjectPlanRequest,
    ProjectPlanResponse,
    ProjectSummary,
)
from schemas.clarification_schema import ClarificationResponse
from services import project_repository
from services.llm_service import llm_service


logger = logging.getLogger(__name__)
PLAN_OUTPUT_KEYS = (
    "requirements",
    "research",
    "architecture",
    "sprint",
    "documentation",
)

app = FastAPI(
    title="Multi-Agent AI Project Manager",
    description="Generate structured project plans from a software idea.",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in os.getenv(
            "FRONTEND_ORIGINS", "http://localhost:3000"
        ).split(",")
        if origin.strip()
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


def _validate_plan_result(result: dict) -> ProjectPlan:
    if result.get("error") is not None:
        logger.error("Project planning workflow failed: %s", result["error"])
        raise HTTPException(
            status_code=502,
            detail="Project planning failed while generating the plan. Please retry.",
        )

    missing_outputs = [key for key in PLAN_OUTPUT_KEYS if result.get(key) is None]
    if missing_outputs:
        logger.error(
            "Project planning workflow completed without outputs: %s",
            ", ".join(missing_outputs),
        )
        raise HTTPException(
            status_code=502,
            detail="Project planning did not generate a complete plan. Please retry.",
        )

    try:
        return ProjectPlan.model_validate(
            {key: result[key] for key in PLAN_OUTPUT_KEYS}
        )
    except Exception as error:
        logger.exception("Project planning workflow returned invalid output.")
        raise HTTPException(
            status_code=502,
            detail="Project planning returned an invalid plan. Please retry.",
        ) from error


def _save_project_plan(project_idea: str, result: dict) -> ProjectPlanResponse:
    plan = _validate_plan_result(result)
    try:
        saved_project = project_repository.save_project(
            project_idea=project_idea,
            plan=plan.model_dump(mode="json"),
        )
    except Exception as error:
        logger.exception("Could not persist the generated project plan.")
        raise HTTPException(
            status_code=503,
            detail="The project plan was generated but could not be saved.",
        ) from error

    return ProjectPlanResponse(
        project_id=saved_project["project_id"],
        created_at=saved_project["created_at"],
        **plan.model_dump(),
    )


def _server_event(event: dict) -> str:
    return f"data: {json.dumps(event)}\n\n"


def _project_input_with_clarifications(request: ProjectPlanRequest) -> str:
    if not request.clarifications:
        return request.project_idea

    choices = "\n".join(
        f"- {answer.question}: {answer.answer}"
        for answer in request.clarifications
    )
    return (
        f"{request.project_idea}\n\n"
        "User-confirmed scope choices (treat these as requirements):\n"
        f"{choices}"
    )


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/api/v1/projects/clarify",
    response_model=ClarificationResponse,
)
def clarify_project_idea(request: ClarificationRequest) -> ClarificationResponse:
    try:
        structured_llm = llm_service.get_structured_llm(ClarificationResponse)
        questions = structured_llm.invoke(
            get_clarification_prompt(request.project_idea)
        )
        return ClarificationResponse.model_validate(questions)
    except Exception as error:
        logger.exception("Could not generate project clarification questions.")
        raise HTTPException(
            status_code=502,
            detail="Could not prepare project questions. Please retry.",
        ) from error


@app.post("/api/v1/projects/plan/stream")
def create_project_plan_stream(request: ProjectPlanRequest) -> StreamingResponse:
    try:
        project_repository.check_database_connection()
    except Exception as error:
        logger.exception("Database preflight check failed before project planning.")
        raise HTTPException(
            status_code=503,
            detail="Project storage is unavailable. Check DATABASE_URL and retry.",
        ) from error

    initial_state = {
        "user_input": _project_input_with_clarifications(request),
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

    def stream_events():
        result = {}
        try:
            for mode, chunk in progress_graph.stream(
                initial_state,
                stream_mode=["custom", "values"],
            ):
                if mode == "custom":
                    yield _server_event({"type": "progress", **chunk})
                elif mode == "values":
                    result = chunk

            plan = _save_project_plan(request.project_idea, result)
            yield _server_event(
                {"type": "complete", "plan": plan.model_dump(mode="json")}
            )
        except HTTPException as error:
            yield _server_event({"type": "error", "message": error.detail})
        except Exception:
            logger.exception("Streaming project planning workflow failed.")
            yield _server_event(
                {
                    "type": "error",
                    "message": "Project planning failed due to an internal error.",
                }
            )

    return StreamingResponse(
        stream_events(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.post(
    "/api/v1/projects/plan",
    response_model=ProjectPlanResponse,
)
def create_project_plan(request: ProjectPlanRequest) -> ProjectPlanResponse:
    try:
        project_repository.check_database_connection()
    except Exception as error:
        logger.exception("Database preflight check failed before project planning.")
        raise HTTPException(
            status_code=503,
            detail="Project storage is unavailable. Check DATABASE_URL and retry.",
        ) from error

    initial_state = {
        "user_input": _project_input_with_clarifications(request),
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

    try:
        result = graph.invoke(initial_state)
    except Exception as error:
        logger.exception("Project planning workflow raised an exception.")
        raise HTTPException(
            status_code=500,
            detail="Project planning failed due to an internal error.",
        ) from error

    return _save_project_plan(request.project_idea, result)


@app.get(
    "/api/v1/projects",
    response_model=list[ProjectSummary],
)
def list_project_plans(
    limit: int = Query(default=20, ge=1, le=100),
) -> list[ProjectSummary]:
    try:
        projects = project_repository.list_projects(limit=limit)
    except Exception as error:
        logger.exception("Could not list saved projects.")
        raise HTTPException(
            status_code=503,
            detail="Project storage is currently unavailable.",
        ) from error

    return [ProjectSummary.model_validate(project) for project in projects]


@app.get(
    "/api/v1/projects/{project_id}",
    response_model=ProjectPlanResponse,
)
def get_project_plan(project_id: UUID) -> ProjectPlanResponse:
    try:
        project = project_repository.get_project(project_id)
    except Exception as error:
        logger.exception("Could not retrieve project %s.", project_id)
        raise HTTPException(
            status_code=503,
            detail="Project storage is currently unavailable.",
        ) from error

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found.")

    return ProjectPlanResponse.model_validate(project)