import os
from google.adk.agents import Agent
from .tools import convert_currency

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

model = "gemini-2.5-flash"

root_agent = Agent(
    name="currency_converter",
    description="An agent that can convert currencies.",
    instruction=instruction,
    model=model,
    tools=[convert_currency]
)
