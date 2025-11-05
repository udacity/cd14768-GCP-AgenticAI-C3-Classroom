import os
from google.adk.agents import Agent
from .tools import get_place_details

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

model = "gemini-2.5-flash"

tools = [get_place_details]

root_agent = Agent(
    name="location_agent",
    description="An agent that can help with location-based queries.",
    instruction=instruction,
    model=model,
    tools=tools
)
