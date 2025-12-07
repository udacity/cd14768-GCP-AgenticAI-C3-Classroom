import os
from datetime import date
from google.adk.agents import Agent
from pydantic import BaseModel, Field
from typing import Literal, Optional

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

# TODO: Define Pydantic types and classes

model = "gemini-2.5-flash"

# TODO: Configure the root_agent with the correct output_schema
root_agent = Agent(
    name="information_summarizer",
    description="A tool for summarizing customer service feedback.",
    instruction=instruction,
    model=model,
    # output_schema=
)
