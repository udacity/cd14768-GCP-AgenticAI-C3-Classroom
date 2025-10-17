import os

# Configure short-term session to use the in-memory service
# TODO: Create session_service

# Read the instructions from a file in the same
# directory as this agent.py file.
script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

# Set up the tools that we will be using for the root agent
tools=[
  # TODO: Add tools
]

# Create our agent
# TODO: Create the root agent