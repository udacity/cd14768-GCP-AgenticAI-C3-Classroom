import os
from google.adk.agents import Agent
from .tools import change_stage

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

model = "gemini-2.5-flash"

root_agent = Agent(
    name="error_handling_agent",
    description="An agent that can handle tool call errors and retry.",
    instruction=instruction,
    model=model,
    tools=[change_stage]
)
