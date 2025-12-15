import os
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
# TODO: Import the preload memory tool and search agent tool

async def auto_save_session_to_memory_callback(callback_context: CallbackContext):
    # TODO: Create the callback function to save session to memory

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

model = "gemini-2.5-flash"

# TODO: Add the tools we need
tools = [
]

root_agent = Agent(
    name="research_assistant_agent",
    description="An agent that can search the web and has long-term memory of past conversations.",
    instruction=instruction,
    model=model,
    tools=tools,
    # TODO: Register the callback
)
