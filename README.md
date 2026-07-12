# 🤖 Multi-Agent AI Project Manager

An intelligent **Multi-Agent AI Project Manager** built using **LangGraph**, **Google Gemini**, and **Pydantic**. The system orchestrates multiple specialized AI agents that collaborate to transform a simple project idea into a complete software development plan.

Instead of relying on a single LLM prompt, this project simulates a real software engineering team where each AI agent has a dedicated responsibility and communicates through structured outputs.

---

# 🚀 Features

* 🧠 Supervisor Agent for intelligent workflow orchestration
* 📋 Requirement Analysis Agent
* 🔬 Research & Technology Recommendation Agent
* 🏗️ Architecture Design Agent *(In Progress)*
* 📅 Sprint Planning Agent *(In Progress)*
* 📖 Documentation Generation Agent *(In Progress)*
* 🔄 Dynamic routing using LangGraph
* 📦 Structured outputs using Pydantic
* 🧩 Context sharing between agents
* ⚡ Modular and scalable architecture

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

## 1. Supervisor Agent

The Supervisor Agent acts as the workflow orchestrator.

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

## 4. Architecture Agent *(Upcoming)*

Will design the complete high-level software architecture using the project requirements and research recommendations.

---

## 5. Sprint Agent *(Upcoming)*

Will generate Agile sprint plans, milestones, tasks, and timelines.

---

## 6. Documentation Agent *(Upcoming)*

Will automatically generate complete project documentation.

---

# ⚙️ Tech Stack

## AI

* Google Gemini
* LangGraph
* LangChain

## Backend

* Python

## Data Validation

* Pydantic

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

### ✅ Completed

* Supervisor Agent
* Requirement Agent
* Research Agent
* Context Builder
* Workflow Routing
* State Management
* Structured Output Models

### 🚧 In Progress

* Architecture Agent
* Sprint Planning Agent
* Documentation Agent

### 🔮 Planned

* Memory System
* Vector Database
* Retrieval-Augmented Generation (RAG)
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
git clone https://github.com/gamingdaddy8/multi-agent-ai-project-manager.git
```

Navigate into the project:

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

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add your Gemini API key.

Run the project:

```bash
python test_workflow.py
```

---

# 🤝 Contributions

Contributions, suggestions, and discussions are welcome.

Feel free to open an issue or submit a pull request.

---

# 👨‍💻 Author

**Rudresh Gawas**

Building AI systems focused on Multi-Agent Architectures, Generative AI, LLM Engineering, and Intelligent Workflow Automation.

If you found this project interesting, consider giving it a ⭐ on GitHub.
