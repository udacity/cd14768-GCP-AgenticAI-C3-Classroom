import os
from google.adk.agents import Agent
from toolbox_core import ToolboxSyncClient

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

model = "gemini-2.5-flash"

# Set up the tools that we will be using for the root agent
toolbox_url = os.environ.get("TOOLBOX_URL", "http://127.0.0.1:5000")
print(f"Connecting to Toolbox at {toolbox_url}")
db_client = ToolboxSyncClient( toolbox_url )
tools=[
    db_client.load_tool("books-by-author"),
    db_client.load_tool("books-in-year-range"),
]

root_agent = Agent(
    name="book_database_agent",
    description="An agent that can access a database about books and authors.",
    instruction=instruction,
    model=model,
    tools=tools
)
