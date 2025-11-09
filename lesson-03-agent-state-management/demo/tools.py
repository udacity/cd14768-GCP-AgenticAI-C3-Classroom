from google.adk.tools import ToolContext

TRANSITIONS = {
    "START": {
        "ADVANCE": "TASK_1"
    },
    "TASK_1": {
        "ADVANCE": "TASK_2"
    },
    "TASK_2": {
        "ADVANCE": "END"
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
    current_stage = tool_context.state.get("temp:stage", "START")

    counter = tool_context.state.get("temp:counter", 0) + 1
    tool_context.state["temp:counter"] = counter

    try:
        next_stage = transition_state(current_stage, command)
        tool_context.state["temp:stage"] = next_stage
        return {
            "number_of_calls": counter
        }
    except ValueError as e:
        return {
            "number_of_calls": counter,
            "error": str(e)
        }