from google.adk.tools import ToolContext

TRANSITIONS = {
    "BLACK": {
        "ADD_RED": "RED",
        "ADD_GREEN": "GREEN",
        "ADD_BLUE": "BLUE",
        "SHOW": "END",
    },
    "RED": {
        "ADD_RED": "RED",
        "ADD_GREEN": "YELLOW",
        "ADD_BLUE": "MAGENTA",
        "SHOW": "END",
    },
    "GREEN": {
        "ADD_RED": "YELLOW",
        "ADD_GREEN": "GREEN",
        "ADD_BLUE": "CYAN",
        "SHOW": "END",
    },
    "BLUE": {
        "ADD_RED": "MAGENTA",
        "ADD_GREEN": "CYAN",
        "ADD_BLUE": "BLUE",
        "SHOW": "END",
    },
    "YELLOW": {
        "ADD_RED": "YELLOW",
        "ADD_GREEN": "YELLOW",
        "ADD_BLUE": "WHITE",
        "SHOW": "END",
    },
    "MAGENTA": {
        "ADD_RED": "MAGENTA",
        "ADD_GREEN": "WHITE",
        "ADD_BLUE": "MAGENTA",
        "SHOW": "END",
    },
    "CYAN": {
        "ADD_RED": "WHITE",
        "ADD_GREEN": "CYAN",
        "ADD_BLUE": "CYAN",
        "SHOW": "END",
    },
    "WHITE": {
        "ADD_RED": "WHITE",
        "ADD_GREEN": "WHITE",
        "ADD_BLUE": "WHITE",
        "SHOW": "END",
    }
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
    Advances the agent to the next stage in the process based on the command
    and returns how many times it has been called.
    """
    current_stage = tool_context.state.get("temp:stage", "BLACK")

    counter = tool_context.state.get("temp:counter", 0) + 1
    tool_context.state["temp:counter"] = counter

    try:
        next_stage = transition_state(current_stage, command)
        tool_context.state["temp:stage"] = next_stage
        if next_stage == "END":
            color = current_stage
        else:
            color = next_stage
        return {
            "number_of_calls": counter,
            "color": color,
        }
    except ValueError as e:
        return {
            "number_of_calls": counter,
            "error": str(e)
        }