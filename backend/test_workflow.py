# backend/test_workflow.py

from graph.workflow import graph

def run_test():
    initial_state = {
        "user_input": """
Build an AI-powered Physiotherapy Platform
where patients perform exercises using pose estimation
and therapists can monitor patient progress remotely.
""",
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

    print("Starting workflow run...\n")
    result = graph.invoke(initial_state)

    print("\n========== FINAL STATE ==========\n")
    for key, value in result.items():
        print(f"--- {key} ---")
        print(value)
        print()

    print("========== SANITY CHECKS ==========")
    checks = {
        "requirements populated":  result.get("requirements") is not None,
        "research populated":     result.get("research") is not None,
        "architecture populated": result.get("architecture") is not None,
        "sprint populated":       result.get("sprint") is not None,
        "documentation populated":result.get("documentation") is not None,
        "no error recorded":      result.get("error") is None,
        "ended cleanly":          result.get("supervisor_decision") is not None
                                   and result["supervisor_decision"].next_agent == "end",
    }

    for label, passed in checks.items():
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {label}")


if __name__ == "__main__":
    run_test()