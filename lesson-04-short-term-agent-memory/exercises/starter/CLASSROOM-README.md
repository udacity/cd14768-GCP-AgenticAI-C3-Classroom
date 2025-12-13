# Module 4 Exercise: Using Session state for trip planning

In this exercise you will build a multi-step travel agent that uses ADK's
session and user-scoped state to manage trip itineraries and remember user
preferences.

---

## Overview

### What You'll Learn

In this exercise, you will develop a basic travel agent that can help users plan
multi-leg journeys. You'll implement tools that interact with both
session-scoped state (for the current trip's itinerary) and user-scoped state (
for a persistent home location preference). This will solidify your
understanding of state management nuances for building intelligent,
context-aware agents.

Learning objectives:

- Implement tools that read and write session-scoped state for task progression.
- Implement tools that read and write user-scoped state for persistent
  preferences.
- Dynamically adapt the agent's prompt based on stored user preferences.
- Construct a multi-step conversation flow that leverages different memory
  scopes.

### Prerequisites

- Basic understanding of Python.
- Basic familiarity with the ADK and state management concepts.

---

## Understanding the Concept

### The Problem

Planning a trip is often a multi-step conversation. An agent needs to remember:

1. **Current Itinerary**: What cities has the user added so far? This is
   specific to the current planning session.
2. **User Preferences**: Does the user have a default "home" airport? This
   preference should persist across different planning sessions.

Without proper state management, the agent could either forget the itinerary
mid-conversation or constantly ask for the home location every time a new
session starts.

### The Solution

We solve this by leveraging ADK's state scoping:

* **Session-scoped state**: Used for the `itinerary`. This ensures the itinerary
  resets for each new planning conversation.
* **User-scoped state**: Used for `user:home_location`. This allows the agent to
  remember the user's preferred starting point across different sessions,
  providing a personalized experience.
* **Dynamic Prompt Injection**: The agent's prompt uses
  `{user:home_location_instruction?}` to adapt its behavior once a home location
  is set, avoiding redundant questions.

### How It Works

1. **Setting Home Location (`set_home_location` tool)**: The user explicitly
   tells the agent their home location. This is stored in `user:home_location`
   and persists across sessions.
2. **Adding Cities (`add_city` tool)**: The user adds cities to their
   itinerary. These are stored in a session-scoped `itinerary` list,
   accumulating over the current conversation.
3. **Creating Itinerary (`create_itinerary` tool)**: When the user is done, this
   tool constructs the final trip plan using the `itinerary` from the current
   session and potentially the `user:home_location` if no explicit starting
   point was given for the first leg.
4. **Adaptive Prompt**: The `agent-prompt.txt` dynamically incorporates
   instructions related to the `user:home_location_instruction` once it's set,
   streamlining the conversation.

### Key Terms

**Session-Scoped State**: Data that persists for the
duration of a single interactive session. Ideal for managing temporary
task-specific data like a draft itinerary.

**User-Scoped State**: Data that persists
indefinitely for a specific user across multiple sessions. Perfect for user
preferences or long-term settings.

**Multi-step Conversation**: An interaction that requires the agent to remember
context, choices, and progress over several user turns to achieve a larger goal.

---

## EXERCISE INSTRUCTIONS

### Your Task

Your task is to complete the ADK agent to function as a multi-step travel
planner. You will need to:

1. **Implement `set_home_location` tool**: Store the provided `location` in
   user state. This would also be a good place to set a dynamic instruction 
   to include in the prompt.
2. **Implement `add_city` tool**: Retrieve the current `itinerary` from
   session state (or initialize it), add the new `city`, and store the
   updated `itinerary` back into session state.
3. **Implement `create_itinerary` tool**: Retrieve the final `itinerary` from
   session state. Construct the legs of the trip (e.g.,
   `{"from": "New York City, NY", "to": "London, UK"}`). If the itinerary 
   starts without an explicit first airport and the home location is set, 
   prepend the home location.
4. **Craft Agent Prompt**: Write instructions in `agent-prompt.txt` that enable
   the agent to:
    * Understand commands to set home location, add cities, and create
      itineraries.
    * Include dynamic instructions if needed.
5. **Configure Agent**: Ensure `agent.py` correctly imports and registers all
   three tools (`set_home_location`, `add_city`, `create_itinerary`) in the
   `root_agent`'s `tools` list.

### Requirements

Your implementation must:

1. Use both session and user state to remember relevant information.
2. Generate trip legs in the format `{"from": CityA, "to": CityB}`.

### Repository Structure

```
.
├── __init__.py           # Initializes the Python package.
├── agent-prompt.txt      # (Your task) Define agent instructions for multi-step planning.
├── agent.py              # (Your task) Configure the ADK agent with the necessary tools.
├── tools.py              # (Your task) Implement the travel planning tools.
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

# TODO: Import add_city and create_itinerary from .tools

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
  instruction = f.read()

model = "gemini-2.5-flash"

root_agent = Agent(
  name="travel_agent",
  description="An agent that can help plan a multi-step trip.",
  instruction=instruction,
  model=model,
  # TODO: Register tools
  tools=[]
)
```

`agent-prompt.txt`

```text
TODO
```

`tools.py`

```python
from google.adk.tools import ToolContext


def set_home_location(location: str, tool_context: ToolContext):
  """
  Sets the customer's home location.
  Only do this if they explicitly tell you to.
  """
  # TODO: Store the location in the user-scoped state

  return f"Home location set to {location}."


def add_city(tool_context: ToolContext, city: str):
  """
  Adds an airport to the itinerary.
  """
  # TODO: Get the current itinerary from the session state (default to empty list)

  # TODO: Append the new city to the list

  # TODO: Update the session state with the new itinerary

  return {"status": f"Added {city} to the itinerary."}


def create_itinerary(tool_context: ToolContext):
  """
  Creates the itinerary based on the airports in the session state.
  """
  # TODO: Get the itinerary from session state

  legs = []
  # TODO: Loop through the itinerary and create legs {"from": ..., "to": ...}

  return {"itinerary": legs}
```

### Expected Behavior

The completed agent should be able to:

1. Allow the user to set a home city that persists across sessions.
2. Allow the user to add multiple cities to a current trip itinerary.
3. Generate a final itinerary with `{"from": ..., "to": ...}` legs, optionally
   starting with the home location if no other start is specified.

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
Human: "My home airport is LHR."
Agent: Home location set to LHR.

# Refresh the page (new session)
Human: "I want to plan a trip."
Agent: Your home location is LHR. If you don't specify a starting point, I will add it to the itinerary. What is your first stop?

Human: "Let's go to JFK, then LAX."
Agent: Added JFK to the itinerary. Added LAX to the itinerary.

Human: "What's my itinerary?"
Agent: {"itinerary": [{"from": "LHR", "to": "JFK"}, {"from": "JFK", "to": "LAX"}]}
```

### Implementation Hints

1. Remember that `tool_context.state` is your interface to memory. Use `user:`
   prefix for user state you wish to save and no prefix for session state.
2. The `create_itinerary` tool needs to check if the itinerary is empty and if
   if the home location is set to prepend the home location.
3. Test setting the home location, refreshing the page, and then adding airports
   to see persistence in action.
4. We're working with an in-memory storage model, so if you restart the 
   server, the user state goes away.

---

## Important Details

### Common Misconceptions

**Misconception**: "All state should be user-scoped if I want it to persist."
**Reality**: Only state that needs to persist *across distinct user
conversations* should be user-scoped. Task-specific, ephemeral data within a
single multi-turn conversation should be session-scoped so it resets cleanly.

**Misconception**: "I need complex logic to manage prepending home location."
**Reality**: Once `user:home_location_instruction` is correctly set, the LLM,
guided by your prompt, can often infer to prepend the home location as the first
leg if no other start is specified.

### Best Practices

1. **Choose the Right Scope**: Deliberately decide whether state should be
   `temp:`, session-scoped, or `user:`-scoped based on its lifecycle
   requirements.
2. **Clear Instructions for Preference Usage**: Provide explicit prompt
   instructions for how the agent should *use* remembered user preferences (
   e.g., using `user:home_location` as a default).
3. **Test Persistence**: After implementing, thoroughly test by setting
   preferences, refreshing the page, and starting new conversations to ensure
   user-scoped data is indeed persisting.

### Common Errors

**Error**: Home location is forgotten after refreshing the page.

- **Cause 1**: `home_location` was stored without the `user:` prefix.
- **Solution 1**: Ensure `tool_context.state["user:home_location"] = 
location` is
  used.

- **Cause 2**: You may have restarted the adk server in between runs.
- **Solution 2**: You can configure an external data store to retain 
  information in between conversation rounds.

**Error**: Itinerary from a previous conversation appears in a new session.

- **Cause**: The `itinerary` list was stored with the `user:` prefix instead of
  being session-scoped.
- **Solution**: Ensure `itinerary` is managed without a prefix in
  `tool_context.state`.
