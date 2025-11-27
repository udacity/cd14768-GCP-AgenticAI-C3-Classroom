import os
from google.adk.agents import Agent

# TODO: Define the tools we need

# Experiment with the different models to see what works better
model = "gemini-2.5-flash"

# Read the instructions from a file in the same
# directory as this agent.py file.
script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

# TODO: Add the tools to this list
tools = [
]

root_agent = Agent(
    name="calculator_tools",
    description="Multiple tools to do different mathematical calculations",
    model=model,
    tools=tools,
    instruction=instruction,
)
