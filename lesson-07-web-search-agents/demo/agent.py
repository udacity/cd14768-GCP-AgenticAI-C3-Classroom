import os
from google.adk.agents import Agent
from google.adk.tools import google_search

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

model = "gemini-2.5-flash"

tools = [
    google_search
]

root_agent = Agent(
    name="web_search_agent",
    description="An agent that can search the web.",
    instruction=instruction,
    model=model,
    tools=tools,
)
