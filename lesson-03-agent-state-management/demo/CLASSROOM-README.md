# Module 3: Implementing Agent State Management with ADK

This demo explores state management techniques within an ADK agent,
demonstrating how to track context during a single request-response cycle using
a simple color-mixing state machine.

---

## Overview

### What You'll Learn

You will learn how to use the ADK's `Session` and `State` objects to manage
agent context. Specifically, this module focuses on request-scoped state (using
the `temp:` prefix) to implement a finite state machine that transitions through
stages based on user input within a single turn.

Learning objectives:

- Understand the concept of "temp:" state for request-scoped variables.
- Implement a simple state machine using ADK tools.
- Read and write state within a tool using `ToolContext`.
- Observe how the agent's prompt updates dynamically based on state changes.

### Prerequisites

- Basic understanding of Python.
- Familiarity with the concept of State Machines.
- Basic understanding of LLMs, ADK, and tool calling.

---

## Understanding the Concept

### The Problem

LLMs are inherently stateless; they don't "remember" variables or data between
function calls or processing steps unless that information is passed back into
the context window. The core task of agents is to manage this conversation 
state, passing the history of the conversation to the LLM as part of each 
request.

However, when an agent needs to perform a multi-step logic process (like a 
state machine) to answer a single user request, this conversation may not be 
enough. LLMs often have problems with counting, for example. State machines 
are also difficult, since the conversation will show the "current" state of 
a value at different points in the conversation which can cause 
hallucinations. Because of these issues, the agent needs a concrete way to 
store and manage some values as it executes tools and report this in a 
consistent way to the LLM. 

### The Solution

The ADK provides a `State` service that allows agents and tools to store and
retrieve data. By using the `temp:` prefix for state variables (e.g.,
`temp:stage`), we define data that persists only for the duration of the current
customer request. This allows the agent to loop through tool calls, updating its
internal state (like the current color mix), until it reaches a final result,
without polluting the longer-term session memory or confusing the LLM with 
changing values in the conversational state.

### How It Works

1. **State Machine**: A theoretical model where a system exists in one "state"
   at a time and transitions to another state based on inputs. Here, the states
   are colors (BLACK, RED, GREEN, etc.), and inputs are commands like 
   `ADD_RED`.
2. **Tool Context**: When the LLM calls a tool, the ADK injects a `ToolContext`
   object. This gives the tool access to the agent's current state.
3. **Reading/Writing State**: The tool reads the current `temp:stage` (
   defaulting to "BLACK"), calculates the next state based on the LLM's command,
   and updates `temp:stage`.
4. **Prompt Injection**: The `agent-prompt.txt` includes a placeholder
   `{temp:stage?}`. The ADK automatically injects the current value of this
   state variable into the prompt sent to the LLM. This allows the LLM to "see"
   the state change after every tool execution and decide its next move. The 
   question mark as part of the state in the prompt indicates that if this 
   state variable is not set, then it should return an empty string, 
   otherwise it will generate an error.

### Key Terms

**State Machine**: A mathematical model of computation. It is an abstract
machine that can be in exactly one of a finite number of states at any given
time. The state machine can change from one state to another in response to some
inputs; the change from one state to another is called a transition.  While 
state machines seem somewhat abstract, they are very important tools to make 
sure business processes proceed along a well-defined path.

**`temp:` State**: In ADK, state keys starting with `temp:` are
"request-scoped." They are created when a user request begins and are cleared
when the final response is sent. They are perfect for intermediate calculations
or multi-step logic within a single turn.

**`ToolContext`**: An object passed to ADK tools that provides access to the
current session, state, and other contextual information.

---

## CODE WALKTHROUGH

### Repository Structure

```
.
├── __init__.py           # Initializes the Python package.
├── agent-prompt.txt      # Defines the agent's instructions and dynamic state injection.
├── agent.py              # Configures the ADK agent.
├── tools.py              # Implements the state machine logic and tool function.
├── README.md             # Overview.
└── requirements.txt      # Dependencies.
```

### Step 1: The State Machine Logic (`tools.py`)

The `TRANSITIONS` dictionary defines our state machine. It maps a
`current_state` (e.g., "RED") and a `command` (e.g., "ADD_BLUE") to a
`next_state` ("MAGENTA"). This logic is deterministic: Red + Blue always equals
Magenta.

```python
TRANSITIONS = {
  "BLACK": {
    "ADD_RED": "RED",
    # ...
  },
  "RED": {
    "ADD_GREEN": "YELLOW",
    # ...
  },
  # ...
}
```

### Step 2: The Tool Implementation (`tools.py`)

The `change_stage` function is the tool exposed to the LLM. It takes a `command`
and the `tool_context`.

1. **Read State**: It accesses `tool_context.state.get("temp:stage", "BLACK")`.
   Note the `temp:` prefix, indicating this state is local to this request. 
   Also note that if the "temp:stage" state isn't set, it defaults to "BLACK".
2. **Logic**: It calculates the next state using `transition_state`.
3. **Write State**: It updates `tool_context.state["temp:stage"]`.
4. **Return**: It returns the result to the LLM.

```python
def change_stage(command: str, tool_context: ToolContext):
  # Read the current state (default to BLACK)
  current_stage = tool_context.state.get("temp:stage", "BLACK")

  # Update a counter
  counter = tool_context.state.get("temp:counter", 0) + 1
  tool_context.state["temp:counter"] = counter

  # Calculate transition
  next_stage = transition_state(current_stage, command)

  # Write the new state back to context
  tool_context.state["temp:stage"] = next_stage

  # ... return result ...
```

### Step 3: Dynamic Prompting (`agent-prompt.txt`)

The prompt uses a special syntax `{temp:stage?}`. This tells the ADK to look up
the value of the `temp:stage` variable and insert it into the text. The `?`
means "if it doesn't exist, ignore it" (or print nothing/default).

```text
The current stage is: "{temp:stage?}".

You are an agent that manages a simple state machine.
...
You must keep sending commands until the current stage is "END".
```

When the agent starts, `temp:stage` is empty (or defaults). After the first tool
call updates it to "RED", the next prompt the LLM sees will say:
`The current stage is: "RED".`. This feedback loop is essential for the LLM to
progress.

### Step 4: Agent Configuration (`agent.py`)

The agent is set up normally, importing the `change_stage` tool.

```python
root_agent = Agent(
  name="state_management_agent",
  # ...
  tools=[change_stage]
)
```

### Complete Example

**Scenario**: User says "Mix red and blue."

1. **Initial State**: `temp:stage` is unset (or "BLACK" logic applies).
2. **LLM Action 1**: Sees "red" in request. Calls `change_stage("ADD_RED")`.
3. **Tool Execution**: Updates `temp:stage` to "RED". Returns "RED".
4. **LLM Prompt Update**: The system prompt now reads
   `The current stage is: "RED".`
5. **LLM Action 2**: Sees "blue" in request. Calls `change_stage("ADD_BLUE")`.
6. **Tool Execution**: Transition "RED" + "ADD_BLUE" -> "MAGENTA". Updates
   `temp:stage` to "MAGENTA".
7. **LLM Action 3**: All colors added. Calls `change_stage("SHOW")`.
8. **Tool Execution**: Transition "MAGENTA" + "SHOW" -> "END". Updates
   `temp:stage` to "END".
9. **LLM Completion**: Sees state is "END". Generates final response: "I made 3
   calls and the final color is Magenta."

---

## Important Details

### Common Misconceptions

**Misconception**: "The LLM automatically knows the state changed."
**Reality**: The LLM is stateless. Typically, we send the history of a 
conversation as part of the state to the LLM each time, but this may not 
include internal information that may be important. In this case, it only has 
the state changes because:

1. The tool returned a value.
2. Crucially, we injected the `temp:stage` variable back into the prompt for the
   *next* inference step. Without `{temp:stage?}` in the prompt, the LLM might
   get lost or repeat actions.

**Misconception**: "The conversation state is good enough to keep track of 
values."
**Reality**: While conversational state (the values in the message history 
with the LLM) *can* keep track of this information, LLMs may get confused 
when trying to keep count of how often an event occurred, or when an 
attribute changes values during the conversation. Having the agent inject 
specific values from the state into the instructions addresses this issue.

**Misconception**: "`temp:` state lasts forever."
**Reality**: `temp:` state is wiped clean after the final response to the user.
If you ask "What was the last color?" in a *new* message, the agent won't know (
unless you used session state, which is covered separately).

### Best Practices

1. **Use `temp:` for atomic tasks**: Use request-scoped state for calculations,
   multi-step reasoning, or loops that should finish within one user turn.
2. **Inject State into Prompts**: Always give the LLM visibility into the state
   variables that drive its logic.
3. **Deterministic Transitions**: When building state machines, ensure
   transitions are well-defined to prevent the agent from getting stuck in
   invalid states.

### Common Errors

**Error**: Agent loops indefinitely.

- **Cause**: The agent doesn't see the state updating to "END", or the prompt
  doesn't instruct it to stop when the state is "END".
- **Solution**: Check `agent-prompt.txt` for the `{temp:stage?}` injection and
  the termination condition ("When the current stage is 'END'...").
