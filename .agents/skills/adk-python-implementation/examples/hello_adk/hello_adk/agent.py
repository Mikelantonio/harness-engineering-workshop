"""Hello ADK: a workshop-planning agent with a deterministic function tool."""
import os
from google.adk.agents import Agent
from .tools import estimate_lab_time

root_agent = Agent(
    name="workshop_planner",
    model=os.getenv("ADK_MODEL", "gemini-flash-latest"),
    description="Helps instructors plan realistic hands-on labs for Python developers.",
    instruction=(
        "You support a technical workshop instructor. Reply in Italian. "
        "Use estimate_lab_time when estimating duration of hands-on labs. "
        "Clearly identify assumptions, include safety considerations, "
        "and do not claim that estimates are measured facts."
    ),
    tools=[estimate_lab_time],
)
