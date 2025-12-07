# Module 4: Implementing Short-Term Agent Memory with ADK and Google Cloud Memorystore

This demo explores how to implement short-term, multi-turn and multi-session, 
agent memory using ADK's `Session` and `State` services. It specifically contrasts 
session-scoped state (for task progress) with user-scoped state (for 
persistent preferences), demonstrating how agents can remember information 
across different interactions. 

---

## Overview

### What You'll Learn

You will learn how to use the ADK's `State` object to manage different scopes of
memory. Specifically, you will see how to persist user preferences across
sessions using the `user:` prefix, while managing the state of a specific task
within a single session using standard session-scoped keys.

Learning objectives:

- Understand the difference between request-scoped, session-scoped and 
  user-scoped state in ADK.
- Implement tools that use session- and user-scoped state.
- Observe how persistent user preferences affect agent behavior across multiple
  sessions.
- Use state to control a multi-step conversation flow (asking a series of
  questions).

### Prerequisites

- Basic understanding of Python.
- Familiarity with State Management concepts (specifically request-scoped state).
- Basic familiarity with the ADK.

---

## Understanding the Concept

### The Problem

LLMs do not manage state, so one solution has been to provide the history of 
a conversation each time. This includes any "hidden" conversation that isn't 
shown to the customer. 

It may be tempting to rely on this conversational state to remember 
everything we need to. While this can sometimes work, agents often need to 
remember things during an exchange that are not represented well during a 
single conversation. For example, LLMs are bad at counting, and we often 
need to keep count of something. We also need to make sure that agents 
remember some data in between sessions or conversations.

To address these issues, ADK defines three types of memory that is saved in 
state:

1. **Request Memory**: Remembering information in between when a customer 
   makes a request and the LLM generates a final response.
2. **Session Memory**: Remembering where we are in a conversation (e.g., "We are
   on question 3 of 5"). This should last until the conversation ends.
3. **User Memory**: Remembering a user's preferences (e.g., "I always want to
   answer 5 questions"). This should persist even if the user closes the browser
   and comes back days later.

### The Solution

The ADK provides different namespaces for state variables to control their
lifespan:

* **`temp:key`**: Request-scoped (cleared after response).
* **`key` (no prefix)**: Session-scoped (persists for the duration of the
  conversation/session).
* **`user:key`**: User-scoped (persists across multiple sessions for the same
  user).

By carefully selecting the prefix, developers can control how long an agent "
remembers" information.

### How It Works

1. **Setting Preferences (`set_iterations`)**: The user tells the agent how many
   questions to ask. The tool stores this in `user:num_iterations`. This value
   is saved to a persistent store associated
   with the user's ID. This can be a database or Memorystore, however in our 
   case we're just saving it while the adk server is running.
2. **Tracking Progress (`run_task`)**: The agent loops through questions. It
   uses `current_iteration` (no prefix) to track progress. This variable exists
   only for the current session.
3. **Dynamic Prompting**: The prompt includes
   `{user:num_iterations_instructions?}`. This allows the agent to change its
   behavior (e.g., stop asking for the number of questions) once the user
   preference is known.

### Key Terms

**Session-Scoped State**: Data that persists for the duration of a single
interactive session. In ADK, keys without a prefix (e.g., `current_iteration`)
default to this scope. It is useful for tracking the context of the current
task.

**User-Scoped State**: Data that persists indefinitely for a specific user,
across multiple sessions. In ADK, keys with the `user:` prefix (e.g.,
`user:num_iterations`) are treated as user-scoped. This is ideal for
preferences, settings, and long-term profile information.

**Scope**: The lifespan and visibility of a variable. In ADK state management,
scope determines when data is deleted (Request vs. Session vs. User).

---

## CODE WALKTHROUGH

### Repository Structure

```
.
├── __init__.py           # Package initialization.
├── agent-prompt.txt      # Agent instructions with dynamic state injection.
├── agent.py              # Agent configuration.
├── tools.py              # Tool logic for setting preferences and running the task.
├── README.md             # Overview.
└── requirements.txt      # Dependencies.
```

### Step 1: Setting User Preferences (`tools.py`)

The `set_iterations` tool handles the user's preference.

```python
def set_iterations(num_iterations: int, tool_context: ToolContext):
  # ... validation ...

  # Store preference in USER scope (persists across sessions)
  tool_context.state["user:num_iterations"] = num_iterations

  # Set a flag/instruction to guide the agent in future turns
  tool_context.state["user:num_iterations_instructions"] = """
        But we do know,
        so you should start asking questions by calling the `run_task` tool.
    """

  return f"I'll remember that you want me to ask you {num_iterations} questions."
```

**Key Point**: The `user:` prefix ensures that if the user restarts the chat,
the agent will still know `num_iterations` and `num_iterations_instructions`.

### Step 2: Running the Task (`tools.py`)

The `run_task` tool manages the question loop.

```python
def run_task(tool_context: ToolContext):
  # Read USER preference
  num_iterations = tool_context.state.get("user:num_iterations", 1)

  # Read SESSION progress (defaults to 0 for new sessions)
  current_iteration = tool_context.state.get("current_iteration", 0)

  if current_iteration < num_iterations...:
    # ... get question ...
    current_iteration += 1

    # Update SESSION progress
    tool_context.state["current_iteration"] = current_iteration

    return {...
    "complete": False}
    else:
    return {"complete": True}
```

**Key Point**: `current_iteration` has no prefix, so it is session-scoped. If
the user starts a *new* session, `current_iteration` resets to 0, but
`user:num_iterations` remains whatever the user set previously.

### Step 3: Adaptive Prompt (`agent-prompt.txt`)

The prompt adapts based on whether the user preference is set.

```text
If we do not know how many questions to ask, you should
- ask how many questions they are willing to answer
- mention that we will not ask them again in the future
{user:num_iterations_instructions?}
```

If `user:num_iterations_instructions` is set (which happens in
`set_iterations`), the instructions change to tell the agent "But we do know...
start asking questions". This prevents the agent from re-asking the user for
their preference in every new session.

---

## Important Details

### Common Misconceptions

**Misconception**: "All state is the same."
**Reality**: Mixing up scopes is a common bug. Storing a preference in session
scope means the user has to repeat it every time. Storing task progress in user
scope means the user can never restart the task from the beginning.

**Misconception**: "I need a database for user state."
**Reality**: ADK abstracts the storage. While you *can* back it with a
database (like Firestore or Cloud SQL), the code looks the same (
`tool_context.state["user:key"] = val`). The ADK handles the persistence layer.

### Best Practices

1. **Prefix Correctly**: strict naming conventions (`user:`, `temp:`) are
   enforced by ADK to manage lifecycle. Use them intentionally.
2. **Clear Separations**: Keep session-specific logic (counters, current step)
   separate from user-specific logic (preferences, settings).
3. **Bootstrap Instructions**: Use state variables injected into the prompt (
   like `user:num_iterations_instructions`) to "bootstrap" the agent's behavior
   when it loads a new session with existing user context.

### Common Errors

**Error**: Agent asks for preference every time.

- **Cause**: Variable was stored without `user:` prefix, or the prompt logic
  doesn't check for the existing preference.
- **Solution**: Ensure `set_iterations` uses `user:num_iterations` and the
  prompt uses dynamic injection to check it.

**Error**: Agent starts in the middle of a task in a new session.

- **Cause**: Task progress (e.g., `current_iteration`) was stored with `user:`
  prefix.
- **Solution**: Remove the `user:` prefix from variables that should reset on a
  new conversation.