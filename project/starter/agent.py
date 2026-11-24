import os


from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from toolbox_core import ToolboxSyncClient

from .datastore import datastore_search_tool
from .search_agent import search_agent_tool

# Configure short-term session to use the in-memory service
session_service = InMemorySessionService()

# Read the instructions from a file in the same
# directory as this agent.py file.
script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

# Set up the tools that we will be using for the root agent
toolbox_url = os.environ.get("TOOLBOX_URL", "http://127.0.0.1:5000")
db_client = ToolboxSyncClient(toolbox_url)
tools = [
    db_client.load_tool("get_product_price"),
    db_client.load_tool("add_product"),
    db_client.load_tool("update_product_stock"),
    datastore_search_tool,
    search_agent_tool,
]

# Create our agent
root_agent = Agent(
    name="bettys_store_agent",
    description="Betty's bird shop customer service agent for products, documents, and web research.",
    instruction=instruction,
    model=os.environ.get("GOOGLE_GENAI_MODEL", "gemini-3.8-flash"),
    tools=tools,
)