import os
from google.adk.agents import Agent
from .datastore import datastore_search_tool

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

model = "gemini-3.8-flash"

tools = [datastore_search_tool]

root_agent = Agent(
    name="superhero_faq_agent",
    description="An agent that can answer questions about superheroes.",
    instruction=instruction,
    model=model,
    tools=tools,
)
