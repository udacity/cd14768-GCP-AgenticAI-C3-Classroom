import os

from google.adk.agents import Agent
from google.adk.tools import AgentTool, google_search

# Definition of an agent tool that accesses Grounding with Google Search

# Read the instructions from a file in the same
# directory as this file.
script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "search-prompt.txt")
with open(instruction_file_path, "r") as f:
  instruction = f.read()

# Gemini Flash is a fast, cost-effective fit for grounded search and concise
# summaries; GOOGLE_GENAI_MODEL can override it when another model is preferred.
search_agent = Agent(
  name="bettys_store_search_agent",
  description="A grounded web search agent for current, externally sourced information.",
  instruction=instruction,
  model=os.environ.get("GOOGLE_GENAI_MODEL", "gemini-3.8-flash"),
  tools=[google_search],
)

search_agent_tool = AgentTool(agent=search_agent)
