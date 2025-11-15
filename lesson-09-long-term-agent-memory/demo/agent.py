import os
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.preload_memory_tool import preload_memory_tool

agent_engine_project = os.environ.get("AGENT_ENGINE_PROJECT")
agent_engine_location = os.environ.get("AGENT_ENGINE_LOCATION")
agent_engine_id = os.environ.get("AGENT_ENGINE_ID")

async def auto_save_session_to_memory_callback(callback_context: CallbackContext):
    print("save session to memory")
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session)

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

model = "gemini-2.5-flash"

tools = [
    preload_memory_tool
]

root_agent = Agent(
    name="memory_agent",
    description="An agent that can save conversations to a Memory Bank.",
    instruction=instruction,
    model=model,
    tools=tools,
    after_agent_callback=auto_save_session_to_memory_callback,
)
