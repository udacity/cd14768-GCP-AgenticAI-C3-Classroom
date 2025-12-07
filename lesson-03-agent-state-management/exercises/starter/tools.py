import random
from datetime import datetime, timezone
from google.adk.tools import ToolContext

def get_time():
    """
    A tool that gets the current time.
    If it fails, then it will return "success" as False
    """
    r = random.random()
    if r < 0.5:
        return {
            "success": False,
            "random": r,
            "error": "Failed to get the time."
        }
    else:
        return {
            "success": True,
            "random": r,
            "time": datetime.now(timezone.utc).isoformat()
        }

# TODO: Define the TRANSITIONS dictionary for the state machine
TRANSITIONS = {
}

def transition_state(start_state: str, command: str):
    """
    Transitions the state machine to the next state based on the current state and command.
    """
    if start_state in TRANSITIONS and command in TRANSITIONS[start_state]:
        return TRANSITIONS[start_state][command]
    else:
        raise ValueError(f"Invalid transition from state '{start_state}' with command '{command}'")

def change_stage(command: str, tool_context: ToolContext):
    """
    Advances the agent to the next stage in the process.
    """
    # TODO: Implement and return the results of trying to get a time

    return result
