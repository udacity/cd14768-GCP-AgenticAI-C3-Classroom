import os
from google.adk.agents import Agent
from google.adk.tools import google_search, AgentTool

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "search-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

model = "gemini-2.5-flash"

# TODO: Define the search tool
tools = [
]

# TODO: Create an agent that uses the search tool
search_agent =

# Create search_agent_tool by wrapping search_agent with AgentTool
search_agent_tool = AgentTool(agent=search_agent)
