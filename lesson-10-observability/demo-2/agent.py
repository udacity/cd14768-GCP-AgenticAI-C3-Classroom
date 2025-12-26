import os
from google.adk.agents import Agent
from .search_agent import search_agent_tool
from .tools import calculate_percentage_change, calculate_profit_or_loss

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

model = "gemini-2.5-flash"

tools = [
    search_agent_tool,
    calculate_percentage_change,
    calculate_profit_or_loss
]

root_agent = Agent(
    name="financial_assistant_agent",
    description="An agent that can find financial information and perform calculations.",
    instruction=instruction,
    model=model,
    tools=tools
)
