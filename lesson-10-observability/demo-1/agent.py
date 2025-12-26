import os
from google.adk.agents import Agent

def get_temperature(city: str) -> str:
    """Returns the temperature in a city."""
    return f"The temperature in {city} is 25 degrees Celsius."

def get_precipitation(city: str) -> str:
    """Returns the precipitation in a city."""
    return f"The precipitation in {city} is 10%."

def get_wind_speed(city: str) -> str:
    """Returns the wind speed in a city."""
    return f"The wind speed in {city} is 15 km/h."

# Experiment with the different models to see what works better
# model = "gemini-2.5-flash-lite"
model = "gemini-2.5-flash"
# model = "gemini-2.5-pro"

# Read the instructions from a file in the same
# directory as this agent.py file.
script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

tools = [
    get_temperature,
    get_precipitation,
    get_wind_speed,
]

root_agent = Agent(
    name="weather_tools",
    description="Multiple tools to illustrate different weather conditions to return and how the ADK will use multiple tools to derive an answer",
    model=model,
    instruction=instruction,
    tools=tools,
)
