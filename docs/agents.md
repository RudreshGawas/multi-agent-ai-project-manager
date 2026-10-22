# Workflow Nodes and Agents

This document describes the workflow that is implemented in the repository.
The terms **node** and **agent** are not interchangeable here: most nodes call
Gemini to generate a result, while the supervisor is currently deterministic
workflow logic.

## At a glance

```text
User idea and optional scope answers
                 |
                 v
            Supervisor
                 |
                 v
        Requirements Agent
                 |
                 v
            Supervisor
                 |
                 v
           Research Agent
                 |
                 v
            Supervisor
                 |
                 v
         Architecture Agent
                 |
                 v
            Supervisor
                 |
                 v
           Sprint Agent
                 |
                 v
            Supervisor
                 |
                 v
       Documentation Agent
                 |
                 v
            Supervisor
                 |
                 v
                END
```

The LangGraph `StateGraph` is built in `backend/graph/workflow.py`. Each
planning node writes its output into the shared `ProjectState`; the supervisor
routes to the next stage based on which outputs are still missing.

## Shared state

`backend/graph/state.py` defines the state passed between nodes:

| Field | Purpose |
| --- | --- |
| `user_input` | Original project idea, optionally followed by user-confirmed scope choices. |
| `requirements` | `RequirementAnalysis` output. |
| `research` | `ResearchAnalysis` output. |
| `architecture` | `ArchitectureDesign` output. |
| `sprint` | `SprintPlan` output. |
| `documentation` | `Documentation` output. |
| `supervisor_decision` | The next stage selected by the supervisor. |
| `current_node` | Human-readable name of the most recently completed node. |
| `status` | Current node status, such as `Completed` or `Error`. |
| `error` | Error text; the router ends the graph when this is set. |

The Pydantic models in `backend/schemas/` validate generated stage outputs.
`backend/utils/context_builder.py` checks prerequisites and supplies each
downstream agent only the context it needs.

## Nodes in execution order

### 1. Supervisor

**Implementation:** `backend/agents/supervisor/node.py`

**Role:** Choose the next incomplete stage or end the workflow.

The current supervisor is deterministic. It selects the first missing output
in this order:

1. Requirements
2. Research
3. Architecture
4. Sprint plan
5. Documentation
6. End

If an earlier node set an error, the supervisor selects `end`. The selected
decision is stored in `supervisor_decision`; `backend/graph/router.py` maps it
to the corresponding graph node.

Although the repository contains a supervisor prompt and imports LLM helpers,
the current `supervisor_node` uses `_deterministic_decision` and does not call
Gemini.

### 2. Requirements Agent

**Implementation:** `backend/agents/requirement/node.py`
**Prompt:** `backend/prompts/requirement_prompt.py`
**Output model:** `RequirementAnalysis`

**Input:** `user_input`, including any scope choices confirmed by the user.

**Output fields:**

- `functional_requirements`
- `non_functional_requirements`
- `user_stories`
- `stakeholders`
- `assumptions`

This stage turns the project idea into a scoped requirements baseline. Later
stages use these requirements as their primary source of scope.

### 3. Research Agent

**Implementation:** `backend/agents/research/node.py`
**Prompt:** `backend/prompts/research_prompt.py`
**Context:** Built by `ContextBuilder.build_research_context()`
**Output model:** `ResearchAnalysis`

**Input:** Functional and non-functional requirements.

**Output fields:** Recommendations for `backend`, `frontend`, `database`,
`authentication`, `ai_framework`, and `deployment`; each contains a
recommendation, reason, and alternatives. It also returns `best_practices`.

The agent is instructed to recommend choices that fit the stated requirements.
Its output is advice for the plan, not proof that a technology has been
implemented in this repository.

### 4. Architecture Agent

**Implementation:** `backend/agents/architect/node.py`
**Prompt:** `backend/prompts/architect_prompt.py`
**Context:** Built by `ContextBuilder.build_architect_context()`
**Output model:** `ArchitectureDesign`

**Input:** Functional and non-functional requirements plus the research
recommendations.

**Output fields:**

- `system_architecture`
- `tech_stack`
- `database_design`
- `api_endpoints`

The prompt tells this stage to remain consistent with the research
recommendations and to design around the requirements.

### 5. Sprint Agent

**Implementation:** `backend/agents/sprint/node.py`
**Prompt:** `backend/prompts/sprint_prompt.py`
**Context:** Built by `ContextBuilder.build_sprint_context()`
**Output model:** `SprintPlan`

**Input:** Requirements, research recommendations, and architecture.

**Output fields:** `sprint_1`, `sprint_2`, `sprint_3`, and `milestones`.

The sprint prompt instructs the agent to base its tasks on the earlier
decisions rather than inventing unrelated scope. A generated sprint plan is a
proposal; it does not mean the tasks have been performed.

### 6. Documentation Agent

**Implementation:** `backend/agents/documentation/node.py`
**Prompt:** `backend/prompts/documentation_prompt.py`
**Context:** Built by `ContextBuilder.build_documentation_context()`
**Output model:** `Documentation`

**Input:** Requirements, research recommendations, architecture, and sprint
plan.

**Output fields:**

- `srs`
- `project_proposal`
- `readme`

This is the final planning node. Its documents summarize earlier agent output;
they should not be treated as evidence that the described code, deployment, or
performance has been independently verified.

## Node implementation pattern

The requirements, research, and documentation nodes are implemented directly.
The architecture and sprint nodes use `make_agent_node` from
`backend/utils/agent_factory.py`, which shares the common steps:

1. Build the stage-specific context.
2. Build the prompt.
3. Request structured output from the Gemini model via LangChain.
4. Store the result under the stage's state key.
5. Record completion or an error in the shared state.

An agent-node error is recorded in `error` and `status`; the router then ends
the workflow rather than running later stages with missing prerequisites.

## Progress streaming

`backend/graph/workflow.py` builds two compiled graphs:

- `graph` — used by the non-streaming plan endpoint.
- `progress_graph` — wraps each planning agent node to emit custom `working`
  and `completed`/`error` events.

The streaming API forwards those events to the frontend. This wrapper reports
when a node starts and finishes; it does not stream the agent's generated
tokens.

## Clarification is separate from the graph

The optional scope questions are generated by
`POST /api/v1/projects/clarify`, using
`backend/prompts/clarification_prompt.py` and the Pydantic models in
`backend/schemas/clarification_schema.py`. This happens before the planning
graph starts, so clarification is **not** a LangGraph node. The user's answers
are appended to `user_input` as explicitly confirmed scope choices.

## RAG status

Retrieval-Augmented Generation (RAG) is not part of the active node workflow.
The `backend/rag/` files are empty placeholders; no agent currently retrieves
documents from a vector store.
