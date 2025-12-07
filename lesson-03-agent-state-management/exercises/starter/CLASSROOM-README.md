# Module 3 Exercise: Implement Agent State

This exercise challenges you to implement a state machine within an ADK agent to
manage tool call retries and build a more robust, fault-tolerant agent.

---

## Overview

### What You'll Learn

In this exercise, you will implement a state machine that uses ADK's `temp:`
(request-scoped) state to manage retries for a potentially failing tool call.
You'll learn how to use tool context to read and write state, enabling the agent
to adapt its behavior dynamically based on previous tool outcomes within a
single request.

Learning objectives:

- Design and implement a state machine for error handling and retries.
- Effectively use `tool_context.state` to read and update `temp:` scoped
  variables.
- Craft an `agent-prompt.txt` that guides the LLM through a stateful retry
  process.
- Understand the importance of robust error handling in agentic workflows.

### Prerequisites

- Basic understanding of Python and state machines.
- Familiarity with the ADK `Agent` and `ToolContext`.
- Understanding of `temp:` state scope.

---

## Understanding the Concept

### The Problem

By default, if an LLM agent calls a tool and that tool fails, the agent might
simply report the error and stop. In real-world applications, tools can be
unreliable (e.g., network issues, temporary API outages). A robust agent needs
the ability to detect failures, manage a retry mechanism, and eventually succeed
or gracefully report a persistent failure. This requires the agent to maintain
state about its attempts.

### The Solution

The solution involves implementing a simple state machine that guides the agent
through a retry process using ADK's `temp:` state. When a tool call fails, the
agent will update its `temp:retry_count` and, if within limits, transition its
`temp:stage` to re-attempt the tool call. This state-driven retry logic ensures
the agent is resilient to transient errors and can achieve its goal through
multiple attempts if necessary.

### How It Works

1. **State Machine**: A predefined sequence of states (START, GETTING_TIME,
   SUCCESS, FAILURE) that the agent can transition between. Commands like
   `GET_TIME`, `GOOD`, `BAD` trigger these transitions.
2. **`temp:` State for Retries**: Two key `temp:` variables are used:
    * `temp:stage`: Tracks the current step in the retry process.
    * `temp:retry_count`: Records how many attempts have been made.
3. **Failing Tool**: A simulated `get_time` tool is used, which has a 50% chance
   of failure, allowing us to test the retry mechanism.
4. **Tool Logic**: The `change_stage` tool reads the current `temp:stage` and
   `temp:retry_count`, executes `get_time` if in `GETTING_TIME` state, updates
   the retry count, and transitions the `temp:stage` based on the
   success/failure of `get_time` and the `retry_count`.
5. **Prompt Guidance**: The `agent-prompt.txt` dynamically injects `temp:stage?`
   and `temp:retry_count?` into the LLM's context. This allows the LLM to "see"
   the current state and number of retries, guiding its decision to `GET_TIME`
   again, or finally issue a `GOOD`/`BAD` command.

### Key Terms

**Retry Logic**: A common error-handling mechanism where a failed operation is
automatically re-attempted, often after a delay or a limited number of times, to
overcome transient errors.

**`temp:` State**: In ADK, state keys starting with `temp:` are
"request-scoped." They are created when a user request begins and are cleared
when the final response is sent. They are perfect for intermediate calculations
or multi-step logic within a single turn.

**Robust Agent**: An agent designed to handle unexpected inputs, errors, and
failures gracefully, maintaining functionality and providing helpful responses
even under adverse conditions.

---

## EXERCISE INSTRUCTIONS

### Your Task

Your task is to complete the ADK agent to robustly fetch the current time by
implementing a state machine that handles potential tool failures. Specifically,
you need to:

1. **Define State Transitions**: Complete the `TRANSITIONS` dictionary in
   `tools.py` to define the states and transitions for the retry logic (START ->
   GETTING_TIME -> SUCCESS / FAILURE).
2. **Implement `change_stage` Logic**: In `tools.py`, complete the
   `change_stage` function to:
    * Read and update `temp:stage` and `temp:retry_count`.
    * Call the `get_time()` tool when in the `GETTING_TIME` state.
    * Return the `get_time()` result or an empty dictionary as appropriate.
3. **Craft Agent Prompt**: In `agent-prompt.txt`, write instructions that guide
   the LLM to:
    * Start by issuing a `GET_TIME` command.
    * Retry `GET_TIME` up to 3 times if it fails.
    * Issue a `GOOD` command if `get_time` succeeds.
    * Issue a `BAD` command if `get_time` fails after 3 attempts.
    * Output the `get_time` result when in `SUCCESS` or `FAILURE` stage.
4. **Configure Agent**: Ensure `agent.py` correctly imports `change_stage` and
   registers it in the `root_agent`'s `tools` list.

The `get_time()` function is provided for you. It emulates a network tool 
call (in this case, to get the current time) that fails about 50% of the time.

### Requirements

Your implementation must:

1. Use the `TRANSITIONS` dictionary to define the state machine.
2. Utilize `temp:stage` to track the current state (START, GETTING_TIME,
   SUCCESS, FAILURE).
3. Utilize `temp:retry_count` to track the number of attempts.
4. Implement retry logic for `get_time` up to a maximum of 3 attempts.
5. Ensure the agent responds with the final `get_time` result (time or error)
   when in `SUCCESS` or `FAILURE`.

### Repository Structure

```
.
├── __init__.py           # Initializes the Python package.
├── agent-prompt.txt      # (Your task) Define agent instructions for stateful retry logic.
├── agent.py              # (Your task) Configure the ADK agent with the change_stage tool.
├── tools.py              # (Your task) Implement the state machine transitions and change_stage logic.
├── .env-sample           # Environment variables (copy to .env).
├── README.md             # Overview.
└── requirements.txt      # Dependencies.
```

Make sure you copy ".env-sample" to ".env" and edit it to add the Google Cloud
project you are working with.
Remember that you should **never** check-in your .env file to git.

### Starter Code

`agent.py`

```python
import os
from google.adk.agents import Agent

# TODO: Import change_stage from .tools

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
  instruction = f.read()

model = "gemini-2.5-flash"

root_agent = Agent(
  name="error_handling_agent",
  description="An agent that can handle tool call errors and retry.",
  instruction=instruction,
  model=model,
  tools=[]  # TODO: Add change_stage tool here
)
```

`agent-prompt.txt`

```text
TODO
```

`tools.py`

```python
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
    raise ValueError(
      f"Invalid transition from state '{start_state}' with command '{command}'")


def change_stage(command: str, tool_context: ToolContext):
  """
  Advances the agent to the next stage in the process.
  """
  # TODO: Implement and return the results of trying to get a time

  return result
```

### Expected Behavior

When the agent receives a request to get the time, it should repeatedly call the
`change_stage` tool with the `GET_TIME` command until `get_time()` succeeds or
it has attempted 3 times. Finally, it should report the outcome (successful time
or failure after retries).

**Running the agent:**

You will run the agent using the `adk web` tool. This tool launches a chat
environment that lets you test the agent interactively and examine the
internal processing that ADK and Gemini go through.

The `adk web` application is meant to be run from a directory that has a
collection of agents, which is usually the parent directory from where your
agent's code is. Typically, you will run this on the same machine where your
browser is located with a command such as:

```bash
adk web
```

**Example usage:**

```text
Human: "Get me the current time."
Agent: The current time is 2023-10-27T10:30:00.000000+00:00. (after 1-3 retries)
```

```text
Human: "Get me the current time."
Agent: Failed to get the time after 3 attempts. (if all retries fail)
```

### Implementation Hints

1. For the `TRANSITIONS` dictionary, consider states like `START`,
   `GETTING_TIME`, `SUCCESS`, and `FAILURE`.
2. The `change_stage` tool will be responsible for both updating the state
   variables (`temp:stage`, `temp:retry_count`) and calling `get_time()` when
   appropriate.
3. Pay close attention to how the LLM decides to transition states based on the
   success or failure of `get_time()` and the `temp:retry_count`.

---

## Important Details

### Common Misconceptions

**Misconception**: "The ADK automatically handles retries for failing tools."
**Reality**: The ADK provides the `Session` and `State` mechanisms, but the
retry logic itself must be explicitly implemented by the developer using a state
machine and `temp:` variables.

**Misconception**: "It's better to use global variables for retry counts."
**Reality**: Using `tool_context.state` with `temp:` prefix ensures that retry
counts are scoped to the current user request and don't interfere with other
concurrent requests, which is crucial in multi-user environments.

### Best Practices

1. **Clear State Definitions**: Define your state machine's states and
   transitions clearly to avoid confusion and ensure correct flow.
2. **Atomic Tool Calls**: Design tools to perform a single, well-defined action.
   This makes it easier to manage their success or failure and integrate them
   into retry logic.
3. **Informative Prompts**: Ensure your `agent-prompt.txt` gives the LLM all
   necessary context (current stage, retry count) to make informed decisions
   about state transitions.

### Common Errors

**Error**: Agent gets stuck in an infinite retry loop.

- **Cause**: The retry condition (`temp:retry_count`) is not correctly checked,
  or the `agent-prompt.txt` does not provide a clear instruction to stop
  retrying after a certain number of attempts.
- **Solution**: Double-check the logic in `change_stage` that increments and
  checks `temp:retry_count`. Ensure the prompt clearly instructs the LLM on when
  to issue the `BAD` command.

**Error**: Agent reports success even when `get_time()` failed.

- **Cause**: The LLM is not correctly interpreting the `success: False` return
  from `get_time()` or the `agent-prompt.txt` is ambiguous about how to handle
  failure states.
- **Solution**: Refine the prompt to explicitly instruct the LLM on what to do
  when `get_time()` returns `success: False` (e.g., transition to `FAILURE` or
  re-attempt if `retry_count` is low).