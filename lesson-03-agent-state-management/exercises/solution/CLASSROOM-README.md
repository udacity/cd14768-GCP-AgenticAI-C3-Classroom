# Module 3 Exercise Solution: Implement Agent State

This solution demonstrates how to implement a robust agent that uses a state
machine and request-scoped state to handle tool failures and retries.

---

## Overview

### What You'll Learn

This solution shows an implementation of a state machine in Python
using the ADK's `ToolContext` to manage `temp:` state. It highlights how to
guide the LLM through a retry process using dynamic prompts and defined state
transitions.

Learning objectives:

- Defining state transitions (`TRANSITIONS`) for a retry workflow.
- Implementing tool logic that reads/writes `temp:` state and executes
  conditional logic.
- Writing prompts that effectively use state variables (`{temp:stage?}`,
  `{temp:retry_count?}`) to drive agent decisions.

### Prerequisites

- Understanding of the Exercise requirements.
- Familiarity with Python dictionaries and ADK `ToolContext`.

---

## Understanding the Concept

### The Problem

We needed an agent that doesn't just give up when the `get_time` tool fails
(which happens 50% of the time in this example). It needs to try again, but not 
forever. This requires "memory" of the current attempt count and the current 
stage of the process within a single user request.

### The Solution

We implemented a state machine with the following states:

- `START`: The initial state.
- `GETTING_TIME`: The state where the agent is actively trying to fetch the
  time.
- `SUCCESS`: The final state if the time is fetched successfully.
- `FAILURE`: The final state if the time cannot be fetched after 3 attempts.

We used `temp:stage` to store the current state and `temp:retry_count` to track
attempts. The `change_stage` tool manages the logic: updating these variables
and calling `get_time` only when appropriate. The prompt acts as the "driver,"
instructing the LLM on which command (`GET_TIME`, `GOOD`, `BAD`) to issue next
based on the tool's output and the current state.

---

## CODE WALKTHROUGH

### Repository Structure

```
.
├── __init__.py           # Package initialization.
├── agent-prompt.txt      # Instructions for the agent.
├── agent.py              # Agent configuration.
├── tools.py              # State machine and tool logic.
├── README.md             # Environment setup.
└── requirements.txt      # Dependencies.
```

### Step 1: Defined Transitions (`tools.py`)

The `TRANSITIONS` dictionary defines the allowed moves. Note that from
`GETTING_TIME`, we can loop back to `GETTING_TIME` (retry), move to `SUCCESS` (
command `GOOD`), or move to `FAILURE` (command `BAD`).

```python
TRANSITIONS = {
  "START": {
    "GET_TIME": "GETTING_TIME"
  },
  "GETTING_TIME": {
    "GET_TIME": "GETTING_TIME",
    "GOOD": "SUCCESS",
    "BAD": "FAILURE"
  },
}
```

### Step 2: Implemented Tool Logic (`tools.py`)

The `change_stage` function performs the heavy lifting:

1. **State Management**: It gets the `current_stage` (defaulting to "START") and
   calculates `next_stage`.
2. **Retry Counting**: It increments `temp:retry_count` every time the state
   changes (which corresponds to an attempt or transition).
3. **Conditional Execution**: Crucially, it only calls `get_time()` if the *new*
   state is `GETTING_TIME`. This ensures we don't call the tool when we are just
   moving to a final state like `SUCCESS`.

```python
def change_stage(command: str, tool_context: ToolContext):
  # ... (state transition logic) ...

  retry_count = tool_context.state.get("temp:retry_count", 0) + 1
  tool_context.state["temp:retry_count"] = retry_count

  if next_stage == "GETTING_TIME":
    result = get_time()
  else:
    result = {}

  return result
```

### Step 3: Crafted Agent Prompt (`agent-prompt.txt`)

The prompt is designed to be the logic engine. It uses:

- **Dynamic Injection**: `{temp:stage?}` and `{temp:retry_count?}` let the LLM
  see the current status.
- **Conditional Logic**: Instructions like "If the result... has success set to
  True, then issue the 'GOOD' command" guide the LLM's next step.
- **Retry Limits**: "If the current number of attempts is less than 3..."
  explicitly handles the retry cap.

```text
The current stage is: "{temp:stage?}".
The current number of attempts is "{temp:retry_count?}"
...
If the result of the tool call has success set to False,
then you should issue one of the following commands:
- If the current number of attempts is less than 3, then issue the "GET_TIME" command
- Otherwise, issue the "BAD" command
...
```

### Complete Example

**Scenario**: `get_time` fails twice, then succeeds.

1. **Request**: "Get the time."
2. **Turn 1**: LLM sees `stage: ""`. Issues `GET_TIME`.
    - Tool: transitions to `GETTING_TIME`, `retry_count`=1. `get_time` fails.
      Returns `success: False`.
3. **Turn 2**: LLM sees `stage: "GETTING_TIME"`, `retry_count: 1`. Input was
   failure.
    - Rule: "success set to False" AND "attempts < 3" -> Issue `GET_TIME`.
    - Tool: transitions to `GETTING_TIME`, `retry_count`=2. `get_time` fails.
      Returns `success: False`.
4. **Turn 3**: LLM sees `stage: "GETTING_TIME"`, `retry_count: 2`. Input was
   failure.
    - Rule: "success set to False" AND "attempts < 3" -> Issue `GET_TIME`.
    - Tool: transitions to `GETTING_TIME`, `retry_count`=3. `get_time` SUCCEEDS.
      Returns `success: True`.
5. **Turn 4**: LLM sees `stage: "GETTING_TIME"`, `retry_count: 3`. Input was
   success.
    - Rule: "success set to True" -> Issue `GOOD`.
    - Tool: transitions to `SUCCESS`.
6. **Final**: LLM sees `stage: "SUCCESS"`.
    - Rule: "Stop... give results".
    - Output: "The current time is..."

---

## Important Details

### Best Practices

- **Explicit State Machines**: Defining transitions in a dictionary (like
  `TRANSITIONS`) makes the logic easier to reason about and debug than scattered
  `if/else` statements.
- **Prompt-Driven Logic**: In agentic workflows, the prompt often contains the
  "business logic" (e.g., "retry 3 times"). This allows you to tune behavior (
  change it to 5 times) without changing code.
- **Separation of Concerns**: The tool handles *doing* the work and *updating*
  the state variables. The LLM handles *deciding* the next move based on that
  state.

### Common Errors

- **Off-by-one Errors**: Retry counts can be tricky. Ensure you know if you are
  counting *starts* or *completions*. Here, we increment on every `change_stage`
  call.
- **Infinite Loops**: If the prompt doesn't have a clear "stop" condition (like
  the "Otherwise, issue 'BAD'" clause), the agent might retry forever.
