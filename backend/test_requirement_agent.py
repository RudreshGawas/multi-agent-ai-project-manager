from agents.requirement.agent import RequirementAgent

agent = RequirementAgent()

result = agent.analyze(
    """
Build an AI-powered Physiotherapy Platform
where patients perform exercises using pose estimation
and therapists monitor patient progress remotely.
"""
)

print(type(result))
print()

print(result.functional_requirements)
print()

print(result.user_stories)