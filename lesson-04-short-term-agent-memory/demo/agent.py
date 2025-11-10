import os
from google.adk.agents import Agent
from .tools import set_iterations, run_task

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

model = "gemini-2.5-flash"

root_agent = Agent(
    name="iterative_agent",
    description="An agent that can run a task multiple times.",
    instruction=instruction,
    model=model,
    tools=[set_iterations, run_task]
)
