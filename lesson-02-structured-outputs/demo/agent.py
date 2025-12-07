import os
from google.adk.agents import Agent
from pydantic import BaseModel, Field
from typing import Literal, Optional

DirectionType = Literal["left", "right"]
DistanceUnitsType = Literal["feet", "yards", "meters"]
CommandType = Literal["turn", "walk", "dance", "get", "error"]

class Distance(BaseModel):
    num: float = Field(..., description="The numerical value of the distance.")
    units: DistanceUnitsType = Field(..., description="The units of measurement for the distance.")

class RobotCommands(BaseModel):
    command: CommandType = Field(..., description="The command for the robot.")
    direction: Optional[DirectionType] = Field(None, description="The direction for the robot.")
    distance: Optional[Distance] = Field(None, description="The distance for the robot to move.")
    object: Optional[str] = Field(None, description="The object the robot should interact with.")
    error: Optional[str] = Field(None, description="If the instruction was invalid or ambiguous, explain the problem.")

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

model = "gemini-2.5-flash"

root_agent = Agent(
    name="robot_commands",
    description="A tool for identifying instructions for a hypothetical robot.",
    instruction=instruction,
    model=model,
    output_schema=RobotCommands,   # See what happens if we remove this line
)
