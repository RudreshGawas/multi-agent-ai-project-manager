from services.llm_service import llm_service
from schemas.supervisor_schema import SupervisorDecision
from prompts.supervisor_prompt import get_supervisor_prompt

formatted_state = """
Project Idea:
Build an AI-powered Physiotherapy Platform

Requirements:
❌ Missing

Research:
❌ Missing

Architecture:
❌ Missing

Documentation:
❌ Missing

Current Node:
None

Status:
Not Started
"""

prompt = get_supervisor_prompt(formatted_state)

print("=" * 80)
print(prompt)
print("=" * 80)

structured_llm = llm_service.get_structured_llm(SupervisorDecision)

print("Calling Supervisor...")

response = structured_llm.invoke(prompt)

print(response)