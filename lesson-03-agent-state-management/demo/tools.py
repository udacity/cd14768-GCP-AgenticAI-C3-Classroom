from google.adk.tools import ToolContext

STAGES = ["START", "TASK_1", "TASK_2", "END"]

def advance_stage(tool_context: ToolContext):
    """
    Advances the agent to the next stage in the process.
    """
    current_stage = tool_context.state.get("temp:stage", "START")

    counter = tool_context.state.get("temp:counter", 0) + 1
    tool_context.state["temp:counter"] = counter

    if current_stage in STAGES:
        current_index = STAGES.index(current_stage)
        if current_index < len(STAGES) - 1:
            next_stage = STAGES[current_index + 1]
            tool_context.state["temp:stage"] = next_stage

    return {
        "number_of_calls": counter
    }