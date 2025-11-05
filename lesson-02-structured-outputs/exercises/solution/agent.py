import os
from datetime import date
from google.adk.agents import Agent
from pydantic import BaseModel, Field
from typing import Literal, Optional

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

FeedbackType = Literal["complaint", "suggestion", "praise"]

class FeedbackSummary(BaseModel):
    customer_name: Optional[str] = Field(None, description="The name of the customer providing feedback.")
    feedback_date: Optional[date] = Field(None, description="The date the feedback was provided.")
    feedback_type: FeedbackType = Field(..., description="The type of feedback.")
    summary: str = Field(..., description="A summary of the feedback.")

model = "gemini-2.5-flash"

root_agent = Agent(
    name="information_summarizer",
    description="A tool for summarizing customer service feedback.",
    instruction=instruction,
    model=model,
    output_schema=FeedbackSummary
)