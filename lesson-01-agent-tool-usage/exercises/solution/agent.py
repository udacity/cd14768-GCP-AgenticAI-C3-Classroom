import os
from google.adk.agents import Agent

def addition(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b

def subtraction(a: int, b: int) -> int:
    """Subtracts two numbers."""
    return a - b

def multiplication(a: int, b: int) -> int:
    """Multiplies two numbers."""
    return a * b

def division(a: int, b: int) -> float:
    """Divides two numbers."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

# Experiment with the different models to see what works better
model = "gemini-2.5-flash"

# Read the instructions from a file in the same
# directory as this agent.py file.
script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

tools = [
    addition,
    subtraction,
    multiplication,
    division,
]

root_agent = Agent(
    name="calculator_tools",
    description="Multiple tools to do different mathematical calculations",
    model=model,
    tools=tools,
    instruction=instruction,
)
