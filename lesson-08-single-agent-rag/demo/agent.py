import os
from google.adk.agents import Agent
from .datastore import datastore_search_tool

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

model = "gemini-2.5-flash"

tools = [datastore_search_tool]

root_agent = Agent(
    name="financials_rag_agent",
    description="An agent that can answer questions about 10K and 10Q financial documents in a document store.",
    instruction=instruction,
    model=model,
    tools=tools,
)
