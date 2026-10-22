# 🤖 Multi-Agent AI Project Manager

An in-progress **Multi-Agent AI Project Manager** built using **FastAPI**, **LangGraph**, **Google Gemini**, and **Pydantic**. Its backend API transforms a project idea into structured requirements, technology recommendations, architecture, sprint planning, and project documentation.

Instead of relying on a single LLM prompt, this project simulates a real software engineering team where each AI agent has a dedicated responsibility and communicates through structured outputs.

---

# 🚀 Features

* 🧠 Workflow supervisor for routing between project-planning stages
* 💬 Optional, project-specific scope questions before planning
* 📋 Requirement Analysis Agent
* 🔬 Research & Technology Recommendation Agent
* 🏗️ Architecture Design Agent
* 📅 Sprint Planning Agent
* 📖 Documentation Generation Agent
* 🔄 Dynamic routing using LangGraph
* 📦 Structured outputs using Pydantic
* 🧩 Context sharing between agents
* ⚡ Modular backend API architecture
* 📡 Live per-agent progress updates while a plan is generated
* 📄 Downloadable PDF and JSON plans

---

# 🏗️ System Architecture

```text
                    User
                      │
                      ▼
              Supervisor Agent
                      │
        Decides Next Agent
                      │
        ┌─────────────┼─────────────┐
        ▼                           │
 Requirement Agent                  │
        │                           │
        ▼                           │
RequirementAnalysis                 │
        │                           │
        ▼                           │
   Research Agent                   │
        │                           │
        ▼                           │
 ResearchAnalysis                   │
        │                           │
        ▼                           │
 Architecture Agent                 │
        │                           │
        ▼                           │
ArchitectureDesign                  │
        │                           │
        ▼                           │
   Sprint Agent                     │
        │                           │
        ▼                           │
    SprintPlan                      │
        │                           │
        ▼                           │
Documentation Agent                 │
        │                           │
        ▼                           │
 Documentation                      │
        ▼
       END
```

---

# 🤖 AI Agents

## 1. Workflow Supervisor

The deterministic supervisor selects the next incomplete workflow stage from
the shared project state. It is workflow logic, not a separate Gemini-powered
agent.

Responsibilities:

* Understand the current workflow state
* Decide which agent should execute next
* Validate workflow progression
* Prevent invalid execution order
* End the workflow when all tasks are complete

---

## 2. Requirement Agent

Converts a high-level project idea into structured software requirements.

Produces:

* Functional Requirements
* Non-Functional Requirements
* User Stories
* Stakeholders
* Assumptions

Output Schema:

```text
RequirementAnalysis
```

---

## 3. Research Agent

Analyzes the project requirements and recommends the most suitable technology stack.

Produces recommendations for:

* Backend
* Frontend
* Database
* Authentication
* AI Framework
* Deployment
* Best Practices

Output Schema:

```text
ResearchAnalysis
```

---

## 4. Architecture Agent

Uses the requirements and technology recommendations to generate a system architecture, tech stack, database design, and API endpoint list.

## 5. Sprint Agent

Uses the requirements and architecture to generate a three-sprint task plan and milestones.

## 6. Documentation Agent

Uses the previous workflow outputs to generate an SRS, project proposal, and README.

## Scope Clarification

Before planning, an optional Gemini-powered clarification endpoint can ask up
to three project-specific questions. The user can answer, enter a custom
answer, or skip the questions. Confirmed answers are passed into the
requirements stage so downstream agents share the selected scope.

---

# ⚙️ Tech Stack

## AI

* Google Gemini, called through LangChain's `ChatGoogleGenerativeAI`
* LangChain structured output with Pydantic schemas
* LangGraph `StateGraph` for agent orchestration and progress streaming

## Backend

* FastAPI
* Python

## Frontend

* Next.js
* React

## Data Validation

* Pydantic

## Persistence

* PostgreSQL with JSONB for saved project plans

## Workflow

* LangGraph StateGraph

## Environment

* Python Virtual Environment

---

# 📂 Project Structure

```text
backend/
│
├── agents/
│   ├── supervisor/
│   ├── requirement/
│   ├── research/
│   ├── architect/
│   ├── sprint/
│   └── documentation/
│
├── graph/
│   ├── state.py
│   ├── workflow.py
│   └── router.py
│
├── prompts/
│
├── schemas/
│
├── services/
│
├── utils/
│   └── context_builder.py
│
├── tests/
│
└── main.py
```

---

# 🔄 Workflow

```text
START
   │
   ▼
Supervisor
   │
   ▼
Requirement Agent
   │
   ▼
Supervisor
   │
   ▼
Research Agent
   │
   ▼
Supervisor
   │
   ▼
Architecture Agent
   │
   ▼
Supervisor
   │
   ▼
Sprint Agent
   │
   ▼
Supervisor
   │
   ▼
Documentation Agent
   │
   ▼
Supervisor
   │
   ▼
END
```

## API

Run the backend from the `backend/` directory:

```bash
uvicorn main:app --reload
```

* `GET /health` checks that the API is responding.
* `POST /api/v1/projects/clarify` accepts `{"project_idea": "..."}` and returns up to three optional, idea-specific scope questions. Clear ideas may return no questions.
* `POST /api/v1/projects/plan` accepts `{"project_idea": "...", "clarifications": [{"question": "...", "answer": "..."}]}`, persists the generated plan, and returns it with a `project_id` and creation timestamp. `clarifications` is optional; project ideas must contain 1–10,000 non-whitespace characters.
* `POST /api/v1/projects/plan/stream` accepts the same request and streams agent progress followed by the completed plan.
* `GET /api/v1/projects?limit=20` lists recent project ideas and IDs; `limit` can range from 1 to 100.
* `GET /api/v1/projects/{project_id}` retrieves a saved plan.
* Interactive API documentation is available at `/docs`.

For an explanation of each LangGraph node and agent, see
[docs/agents.md](docs/agents.md).

Project persistence requires a running PostgreSQL server and an existing database. Set `DATABASE_URL` in `backend/.env`; the `projects` table is created automatically on first read or write.

For local development, the Next.js frontend runs from `frontend/` with `npm run dev`. Copy `frontend/.env.example` to `frontend/.env.local` to configure the API URL. Configure `FRONTEND_ORIGINS` in `backend/.env` to include the frontend origin if it differs from `http://localhost:3000`.

To start the complete local stack with Docker Compose, copy `.env.example` to `.env`, set a URL-safe PostgreSQL password, configure `backend/.env` as above, and run `docker compose up --build` from the repository root. Open `http://localhost:3000`; the API is available at `http://localhost:8000`. Compose defaults are for local development only; do not use them in a public deployment.

---

# 🧩 Architecture Principles

This project follows several software engineering principles:

* Single Responsibility Principle (SRP)
* Separation of Concerns
* Loose Coupling
* Modular Design
* Layered Architecture
* Structured AI-to-AI Communication

Each component has only one responsibility.

Example:

```text
ProjectState
      │
      ▼
ContextBuilder
      │
      ▼
Prompt Builder
      │
      ▼
LLM Service
      │
      ▼
Structured Output
      │
      ▼
ProjectState
```

---

# 📌 Current Progress

### ✅ API and workflow implemented; mocked tests pass

* Supervisor Agent and workflow routing
* Requirement, research, architecture, sprint planning, and documentation agent nodes
* Shared project state, context builder, prompts, and structured output models
* Gemini structured-output service and optional scope clarification endpoint
* FastAPI health check, streaming and non-streaming plan generation, recent project listing, and saved-plan retrieval
* PostgreSQL persistence for generated project plans
* Next.js interface with per-agent progress, expandable output cards, PDF/JSON downloads, and saved-plan history
* Docker Compose setup for running the frontend, API, and PostgreSQL locally

Automated tests verify API input handling, PostgreSQL repository behavior with mocked database connections, saved-plan retrieval, and the complete workflow with mocked LLM responses. Live Gemini calls and integration against a running PostgreSQL server are not covered by those tests. The frontend and API integration are implemented; the Docker stack has not been run in this environment.

GitHub Actions runs the backend unit suite, frontend production build, and Docker Compose configuration validation on pushes and pull requests. Database and Gemini tests are mocked, so CI does not require external services or credentials.

### 🔮 Planned

* Memory System
* Vector Database and Retrieval-Augmented Generation (RAG) — not implemented yet
* Human-in-the-Loop Approval
* Multi-LLM Support
* Tool Calling
* Web Research Agent
* Code Generation Agent
* Deployment Agent
* CI/CD Integration

---

# 💡 Why This Project?

Traditional AI applications rely on a single prompt to solve complex tasks.

This project demonstrates a more scalable approach where multiple specialized AI agents collaborate through structured outputs and workflow orchestration.

The goal is to simulate a real software engineering team using AI.

---

# 🚀 Future Roadmap

* Agent Memory
* Web Search Integration
* GitHub Integration
* Jira Integration
* Automatic Sprint Tracking
* Architecture Diagram Generation
* Cost Estimation Agent
* Security Review Agent
* Testing Agent
* Deployment Agent
* Multi-Model Support
* AI Code Review Agent

---

# 🛠️ Installation

Clone the repository:

```bash
git clone https://github.com/RudreshGawas/multi-agent-ai-project-manager.git
```

Navigate into the repository:

```bash
cd multi-agent-ai-project-manager
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

Windows:

```bash
venv\Scripts\activate
```

Install backend dependencies:

```bash
pip install -r backend/requirements.txt
```

Copy `backend/.env.example` to `backend/.env` and set `GOOGLE_API_KEY` and `DATABASE_URL`. Create the PostgreSQL database named in the URL before starting the API.

Run the API from the backend directory:

```bash
cd backend
uvicorn main:app --reload
```

In a second terminal, run the frontend:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

---

# 🤝 Contributions

Contributions, suggestions, and discussions are welcome.

Feel free to open an issue or submit a pull request.

---

# 👨‍💻 Author

**Rudresh Gawas**

Building AI systems focused on Multi-Agent Architectures, Generative AI, LLM Engineering, and Intelligent Workflow Automation.

If you found this project interesting, consider giving it a ⭐ on GitHub.
