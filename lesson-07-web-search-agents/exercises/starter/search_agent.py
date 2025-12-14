import os
from google.adk.agents import Agent
from google.adk.tools import google_search, AgentTool
from pydantic import BaseModel, Field
from typing import List, Optional

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "search-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

model = "gemini-2.5-flash"

# TODO: Define the search tool
tools = [
]

# TODO: Create an agent that uses the search tool
search_agent =

class StockSearchResult(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol")
    company_name: str = Field(..., description="Full company name")
    current_price: float = Field(..., description="Current stock price")
    change_percent: float = Field(..., description="Today's change %")
    sources: List[str] = Field(..., description="Source URLs")

# TODO: Create an agent that structures the output from the search agent
structured_search_agent =

# Create search_agent_tool by wrapping search_agent with AgentTool
search_agent_tool = AgentTool(agent=structured_search_agent)
