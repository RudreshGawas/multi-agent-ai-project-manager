"use client";

import { useEffect, useState } from "react";

const apiUrl = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000").replace(
  /\/$/,
  "",
);

const sections = [
  {
    key: "requirements",
    title: "Requirements",
    eyebrow: "01 / DISCOVER",
    agent: "Requirements agent",
  },
  {
    key: "research",
    title: "Technology research",
    eyebrow: "02 / EVALUATE",
    agent: "Research agent",
  },
  {
    key: "architecture",
    title: "Architecture",
    eyebrow: "03 / DESIGN",
    agent: "Architecture agent",
  },
  {
    key: "sprint",
    title: "Sprint plan",
    eyebrow: "04 / DELIVER",
    agent: "Sprint agent",
  },
  {
    key: "documentation",
    title: "Documentation",
    eyebrow: "05 / SHARE",
    agent: "Documentation agent",
  },
];

function readableLabel(value) {
  return value.replaceAll("_", " ");
}

function initialAgentStatuses() {
  return Object.fromEntries(sections.map(({ key }) => [key, "pending"]));
}

function downloadJson(plan) {
  const file = new Blob([JSON.stringify(plan, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(file);
  const link = document.createElement("a");
  link.href = url;
  link.download = `project-plan-${plan.project_id}.json`;
  link.click();
  URL.revokeObjectURL(url);
}

function previewText(value) {
  if (Array.isArray(value)) {
    return value.map(previewText).filter(Boolean).join(" · ");
  }
  if (value && typeof value === "object") {
    return Object.values(value).map(previewText).filter(Boolean).join(" · ");
  }
  return String(value ?? "");
}

function PlanFields({ data }) {
  return Object.entries(data || {}).map(([field, value]) => (
    <section className="plan-field" key={field}>
      <h4>{readableLabel(field)}</h4>
      <ContentValue value={value} />
    </section>
  ));
}

function AgentProgress({ statuses }) {
  if (!statuses) return null;

  const completed = Object.values(statuses).filter(
    (status) => status === "completed",
  ).length;
  const activeAgent = sections.find(
    ({ key }) => statuses[key] === "working",
  );

  return (
    <section className="agent-progress" aria-live="polite">
      <div className="agent-progress-heading">
        <div>
          <p className="eyebrow">WORKFLOW PROGRESS</p>
          <h2>
            {activeAgent
              ? `${activeAgent.agent} is working`
              : completed === sections.length
                ? "All agents are done"
                : "Preparing your project team"}
          </h2>
        </div>
        <span className="progress-count">
          {completed} / {sections.length} complete
        </span>
      </div>
      <div
        className="agent-progress-track"
        role="list"
        aria-label="Agent progress"
      >
        {sections.map(({ key, agent }, index) => {
          const status = statuses[key];
          return (
            <div
              className={`agent-step agent-step-${status}`}
              key={key}
              role="listitem"
              aria-label={`${agent}: ${status}`}
            >
              <span className="agent-step-marker" aria-hidden="true">
                {status === "completed" ? "✓" : `0${index + 1}`}
              </span>
              <span className="agent-step-copy">
                <strong>{agent}</strong>
                <span>
                  {status === "completed"
                    ? "Complete"
                    : status === "working"
                      ? "Working..."
                      : status === "error"
                        ? "Needs attention"
                        : "Waiting"}
                </span>
              </span>
            </div>
          );
        })}
      </div>
    </section>
  );
}

function ContentValue({ value }) {
  if (Array.isArray(value)) {
    return (
      <ul className="content-list">
        {value.map((item, index) => (
          <li key={`${index}-${item}`}>{item}</li>
        ))}
      </ul>
    );
  }

  if (value && typeof value === "object") {
    return (
      <div className="nested-grid">
        {Object.entries(value).map(([key, child]) => (
          <div className="nested-item" key={key}>
            <h4>{readableLabel(key)}</h4>
            {key === "recommended" ? (
              <p className="recommendation">{child}</p>
            ) : (
              <ContentValue value={child} />
            )}
          </div>
        ))}
      </div>
    );
  }

  return <p className="content-text">{String(value)}</p>;
}

function PlanResults({ plan }) {
  const [selectedSection, setSelectedSection] = useState("requirements");
  if (!plan) return null;
  const selected = sections.find(({ key }) => key === selectedSection);

  return (
    <section className="results" aria-live="polite">
      <div className="results-heading">
        <div>
          <p className="eyebrow">YOUR PROJECT BLUEPRINT</p>
          <h2>Plan at a glance</h2>
        </div>
        <div className="project-meta">
          <span>Saved project</span>
          <code>{plan.project_id}</code>
          <time dateTime={plan.created_at}>
            {new Date(plan.created_at).toLocaleString()}
          </time>
        </div>
      </div>

      <div className="download-actions">
        <button
          className="secondary-button"
          onClick={() => window.print()}
          type="button"
        >
          Download PDF <span aria-hidden="true">↓</span>
        </button>
        <button
          className="secondary-button"
          onClick={() => downloadJson(plan)}
          type="button"
        >
          Download JSON <span aria-hidden="true">↓</span>
        </button>
      </div>

      <div className="agent-windows" aria-label="Project plan agents">
        {sections.map(({ key, title, eyebrow, agent }) => {
          const isSelected = selectedSection === key;
          const summary = Object.values(plan[key] || {})
            .map(previewText)
            .filter(Boolean)
            .join(" · ");

          return (
            <button
              aria-controls={selectedSection ? "agent-output" : undefined}
              aria-expanded={isSelected}
              className={`agent-window${isSelected ? " agent-window-selected" : ""}`}
              key={key}
              onClick={() => setSelectedSection(isSelected ? null : key)}
              type="button"
            >
              <span className="agent-window-top">
                <span className="eyebrow">{eyebrow}</span>
                <span className="agent-window-check" aria-label="Complete">
                  ✓
                </span>
              </span>
              <strong>{title}</strong>
              <span className="agent-window-agent">{agent}</span>
              <span className="agent-window-preview">
                {summary || "No output was returned for this agent."}
              </span>
              <span className="agent-window-action">
                {isSelected ? "Close details" : "View full output"}{" "}
                <span aria-hidden="true">{isSelected ? "−" : "+"}</span>
              </span>
            </button>
          );
        })}
      </div>

      {selected && (
        <section className="agent-output" id="agent-output" aria-live="polite">
          <div className="agent-output-heading">
            <div>
              <p className="eyebrow">{selected.eyebrow}</p>
              <h3>{selected.title}</h3>
              <p>{selected.agent} · Complete</p>
            </div>
            <button
              aria-label="Close agent details"
              className="close-output"
              onClick={() => setSelectedSection(null)}
              type="button"
            >
              Close <span aria-hidden="true">×</span>
            </button>
          </div>
          <div className="agent-output-fields">
            <PlanFields data={plan[selected.key]} />
          </div>
        </section>
      )}

      <div className="print-plan">
        {sections.map(({ key, title, eyebrow, agent }) => (
          <article className="print-plan-section" key={key}>
            <p className="eyebrow">{eyebrow}</p>
            <h3>{title}</h3>
            <p className="plan-agent">{agent} · Complete</p>
            <div className="agent-output-fields">
              <PlanFields data={plan[key]} />
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

export default function Home() {
  const [idea, setIdea] = useState("");
  const [projectId, setProjectId] = useState("");
  const [plan, setPlan] = useState(null);
  const [projects, setProjects] = useState([]);
  const [historyError, setHistoryError] = useState("");
  const [historyLoading, setHistoryLoading] = useState(false);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [busyAction, setBusyAction] = useState("");
  const [agentStatuses, setAgentStatuses] = useState(null);
  const [clarificationQuestions, setClarificationQuestions] = useState([]);
  const [clarificationAnswers, setClarificationAnswers] = useState({});
  const [clarificationOtherAnswers, setClarificationOtherAnswers] = useState({});

  async function refreshProjects() {
    setHistoryLoading(true);
    setHistoryError("");

    try {
      const response = await fetch(`${apiUrl}/api/v1/projects?limit=20`);
      const body = await response.json();
      if (!response.ok) {
        throw new Error(body.detail || "Could not load saved projects.");
      }
      setProjects(body);
    } catch (requestError) {
      setHistoryError(
        requestError instanceof TypeError
          ? "Could not connect to the API."
          : requestError.message,
      );
    } finally {
      setHistoryLoading(false);
    }
  }

  useEffect(() => {
    refreshProjects();
  }, []);

  async function requestPlan(path, options, action) {
    setBusy(true);
    setBusyAction(action);
    setError("");
    setPlan(null);
    setAgentStatuses(action === "generate" ? initialAgentStatuses() : null);
    setClarificationQuestions([]);

    try {
      let body;
      if (action === "generate") {
        const response = await fetch(
          `${apiUrl}/api/v1/projects/plan/stream`,
          options,
        );
        if (!response.ok) {
          const failure = await response.json();
          throw new Error(failure.detail || "The request could not be completed.");
        }
        if (!response.body) {
          throw new Error("The progress stream is unavailable.");
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";
        let completedPlan = null;

        function handleEvent(block) {
          const data = block
            .split(/\r?\n/)
            .filter((line) => line.startsWith("data:"))
            .map((line) => line.slice(5).trim())
            .join("\n");
          if (!data) return;

          const event = JSON.parse(data);
          if (event.type === "progress") {
            setAgentStatuses((current) => ({
              ...current,
              [event.agent]: event.status,
            }));
          } else if (event.type === "complete") {
            completedPlan = event.plan;
          } else if (event.type === "error") {
            throw new Error(event.message);
          }
        }

        while (true) {
          const { done, value } = await reader.read();
          buffer += decoder.decode(value, { stream: !done });
          const blocks = buffer.split(/\r?\n\r?\n/);
          buffer = blocks.pop() || "";
          blocks.forEach(handleEvent);
          if (done) break;
        }
        if (buffer.trim()) handleEvent(buffer);
        if (!completedPlan) {
          throw new Error("The workflow ended without returning a project plan.");
        }
        body = completedPlan;
      } else {
        const response = await fetch(`${apiUrl}${path}`, options);
        body = await response.json();
        if (!response.ok) {
          throw new Error(body.detail || "The request could not be completed.");
        }
      }
      setPlan(body);
      setProjectId(body.project_id);
      if (action === "generate") {
        refreshProjects();
      }
    } catch (requestError) {
      setAgentStatuses((current) => {
        if (!current) return current;
        const activeAgent = Object.keys(current).find(
          (key) => current[key] === "working",
        );
        return activeAgent
          ? { ...current, [activeAgent]: "error" }
          : current;
      });
      setError(
        requestError instanceof TypeError
          ? "Could not connect to the API. Check that the backend is running and its URL is configured."
          : requestError.message,
      );
    } finally {
      setBusy(false);
      setBusyAction("");
    }
  }

  async function createPlan(event) {
    event.preventDefault();
    setBusy(true);
    setBusyAction("clarify");
    setError("");
    setPlan(null);
    setAgentStatuses(null);
    setClarificationQuestions([]);
    setClarificationAnswers({});
    setClarificationOtherAnswers({});

    let shouldGenerate = false;
    try {
      const response = await fetch(`${apiUrl}/api/v1/projects/clarify`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ project_idea: idea.trim() }),
      });
      const body = await response.json();
      if (!response.ok) {
        throw new Error(body.detail || "Could not prepare project questions.");
      }

      const questions = body.questions || [];
      if (questions.length > 0) {
        setClarificationQuestions(questions);
        setClarificationAnswers({});
        setClarificationOtherAnswers({});
        return;
      }
      shouldGenerate = true;
    } catch (requestError) {
      setError(
        requestError instanceof TypeError
          ? "Could not connect to the API. Check that the backend is running and its URL is configured."
          : requestError.message,
      );
    } finally {
      setBusy(false);
      setBusyAction("");
    }

    if (shouldGenerate) {
      return generatePlan([]);
    }
  }

  function generatePlan(clarifications) {
    return requestPlan(
      "/api/v1/projects/plan/stream",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          project_idea: idea.trim(),
          clarifications,
        }),
      },
      "generate",
    );
  }

  function submitClarifications(event) {
    event.preventDefault();
    const answers = clarificationQuestions.flatMap((question, index) => {
      const answer =
        clarificationAnswers[index] === "__other__"
          ? clarificationOtherAnswers[index]?.trim()
          : clarificationAnswers[index];
      return answer ? [{ question: question.question, answer }] : [];
    });
    return generatePlan(answers);
  }

  function loadPlan(event) {
    event.preventDefault();
    const id = projectId.trim();
    if (!id) {
      setError("Enter a saved project ID to load its plan.");
      return;
    }
    return requestPlan(
      `/api/v1/projects/${encodeURIComponent(id)}`,
      { method: "GET" },
      "load",
    );
  }

  return (
    <main>
      <nav className="topbar">
        <a className="brand" href="/">
          <span className="brand-mark">P</span>
          <span>PROJECT PILOT</span>
        </a>
        <span className="topbar-note">AI planning workspace</span>
      </nav>

      <section className="hero">
        <div className="hero-copy">
          <p className="eyebrow">FROM FIRST THOUGHT TO FIRST SPRINT</p>
          <h1>
            A clear plan for
            <br />
            <span>what you want to build.</span>
          </h1>
          <p className="hero-description">
            Describe your software idea. A team of specialized AI agents will
            shape it into requirements, technology choices, architecture,
            sprints, and documentation.
          </p>
        </div>

        <div className="workflow-strip" aria-label="Planning workflow">
          {["Discover", "Research", "Design", "Plan", "Document"].map(
            (stage, index) => (
              <div className="workflow-stage" key={stage}>
                <span className="stage-number">0{index + 1}</span>
                <span>{stage}</span>
              </div>
            ),
          )}
        </div>
      </section>

      <section className="workspace">
        <div className="input-column">
          <form className="idea-card" onSubmit={createPlan}>
            <div className="card-title-row">
              <div>
                <p className="eyebrow">START A NEW PROJECT</p>
                <h2>What are you building?</h2>
              </div>
              <span className="input-icon" aria-hidden="true">
                ✳
              </span>
            </div>
            <label className="sr-only" htmlFor="project-idea">
              Describe your project idea
            </label>
            <textarea
              id="project-idea"
              maxLength={10_000}
              minLength={1}
              onChange={(event) => {
                setIdea(event.target.value);
                setClarificationQuestions([]);
                setClarificationAnswers({});
                setClarificationOtherAnswers({});
              }}
              placeholder="For example: A platform that helps independent tutors manage lessons, share learning materials, and track student progress."
              required
              value={idea}
            />
            <div className="form-footer">
              <span>{idea.length.toLocaleString()} / 10,000 characters</span>
              <button
                className="primary-button"
                disabled={busy || !idea.trim()}
                type="submit"
              >
                {busyAction === "generate" ? (
                  <>
                    <span className="spinner" /> Building your plan
                  </>
                ) : busyAction === "clarify" ? (
                  <>
                    <span className="spinner" /> Preparing questions
                  </>
                ) : (
                  <>
                    Clarify my idea <span aria-hidden="true">↗</span>
                  </>
                )}
              </button>
            </div>
          </form>

          {clarificationQuestions.length > 0 && (
            <form
              className="clarification-card"
              onSubmit={submitClarifications}
              aria-labelledby="clarification-title"
            >
              <div className="clarification-heading">
                <div>
                  <p className="eyebrow">OPTIONAL SCOPE CHECK</p>
                  <h3 id="clarification-title">A couple of quick choices</h3>
                  <p>
                    Your answers guide every agent. Leave any blank to keep the
                    plan focused on a simple MVP.
                  </p>
                </div>
              </div>
              <div className="clarification-questions">
                {clarificationQuestions.map((question, index) => (
                  <div
                    className="clarification-question"
                    key={`${index}-${question.question}`}
                  >
                    <label htmlFor={`scope-choice-${index}`}>
                      {question.question}
                    </label>
                    <select
                      id={`scope-choice-${index}`}
                      onChange={(event) =>
                        setClarificationAnswers((current) => ({
                          ...current,
                          [index]: event.target.value,
                        }))
                      }
                      value={clarificationAnswers[index] || ""}
                    >
                      <option value="">Skip this question</option>
                      {question.options.map((option) => (
                        <option key={option} value={option}>
                          {option}
                        </option>
                      ))}
                      <option value="__other__">Other (I'll specify)</option>
                    </select>
                    {clarificationAnswers[index] === "__other__" && (
                      <input
                        aria-label={`Your answer to: ${question.question}`}
                        onChange={(event) =>
                          setClarificationOtherAnswers((current) => ({
                            ...current,
                            [index]: event.target.value,
                          }))
                        }
                        placeholder="Tell us what you have in mind"
                        value={clarificationOtherAnswers[index] || ""}
                      />
                    )}
                    <span className="suggested-answer">
                      Simple MVP suggestion: {question.suggested_answer}
                    </span>
                  </div>
                ))}
              </div>
              <div className="clarification-actions">
                <button
                  className="secondary-button"
                  disabled={busy}
                  onClick={() => generatePlan([])}
                  type="button"
                >
                  Skip questions
                </button>
                <button className="primary-button" disabled={busy} type="submit">
                  Use my choices and build plan <span aria-hidden="true">↗</span>
                </button>
              </div>
            </form>
          )}

          <form className="load-card" onSubmit={loadPlan}>
            <div>
              <p className="eyebrow">PICK UP WHERE YOU LEFT OFF</p>
              <h3>Open a saved project</h3>
            </div>
            <label className="sr-only" htmlFor="project-id">
              Saved project ID
            </label>
            <div className="load-controls">
              <input
                id="project-id"
                onChange={(event) => setProjectId(event.target.value)}
                placeholder="Paste a project ID"
                value={projectId}
              />
              <button
                className="secondary-button"
                disabled={busy || !projectId.trim()}
                type="submit"
              >
                {busyAction === "load" ? "Loading..." : "Open"}
              </button>
            </div>
          </form>

          <section className="history-card" aria-labelledby="history-title">
            <div className="history-heading">
              <div>
                <p className="eyebrow">YOUR WORKSPACE</p>
                <h3 id="history-title">Recent projects</h3>
              </div>
              <button
                className="refresh-button"
                disabled={historyLoading}
                onClick={refreshProjects}
                type="button"
              >
                {historyLoading ? "Refreshing..." : "Refresh"}
              </button>
            </div>

            {historyError ? (
              <p className="history-message" role="status">
                {historyError}
              </p>
            ) : historyLoading && projects.length === 0 ? (
              <p className="history-message">Loading saved projects...</p>
            ) : projects.length === 0 ? (
              <p className="history-message">
                Your generated plans will appear here.
              </p>
            ) : (
              <ul className="project-list">
                {projects.map((project) => (
                  <li key={project.project_id}>
                    <button
                      className="project-list-item"
                      disabled={busy}
                      onClick={() => {
                        setProjectId(project.project_id);
                        requestPlan(
                          `/api/v1/projects/${encodeURIComponent(project.project_id)}`,
                          { method: "GET" },
                          "load",
                        );
                      }}
                      type="button"
                    >
                      <span className="project-list-copy">
                        <span>{project.project_idea}</span>
                        <time dateTime={project.created_at}>
                          {new Date(project.created_at).toLocaleString()}
                        </time>
                      </span>
                      <span className="project-list-arrow" aria-hidden="true">
                        ↗
                      </span>
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </section>

          {error && (
            <div className="error-message" role="alert">
              <span aria-hidden="true">!</span>
              {error}
            </div>
          )}
        </div>

        <aside className="aside-note">
          <span className="aside-star" aria-hidden="true">
            ✳
          </span>
          <p className="eyebrow">BUILT FOR MOMENTUM</p>
          <p>
            One project idea. Five focused agents. A connected blueprint you
            can actually start building from.
          </p>
          <div className="aside-divider" />
          <p className="aside-caption">
            Your generated plan is saved and can be reopened any time with its
            project ID.
          </p>
        </aside>
      </section>

      <AgentProgress statuses={agentStatuses} />
      <PlanResults plan={plan} />

      <footer className="footer">
        <span>PROJECT PILOT</span>
        <span>Ideas into action, one sprint at a time.</span>
      </footer>
    </main>
  );
}
