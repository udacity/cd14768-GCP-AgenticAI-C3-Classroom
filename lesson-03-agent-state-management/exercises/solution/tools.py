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

def check_retry(tool_context: ToolContext):
    """
    Checks if the agent should retry a failed tool call.
    """
    retry_count = tool_context.state.get("temp:retry_count", 0)
    if retry_count < 3:
        tool_context.state["temp:retry_count"] = retry_count + 1
        return {"should_retry": True}
    else:
        return {"should_retry": False}