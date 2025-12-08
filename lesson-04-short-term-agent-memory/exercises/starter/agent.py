import os
from google.adk.agents import Agent
# TODO: Import functions from .tools

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

model = "gemini-2.5-flash"

root_agent = Agent(
    name="travel_agent",
    description="An agent that can help plan a multi-step trip.",
    instruction=instruction,
    model=model,
    # TODO: Register tools
    tools=[]
)
