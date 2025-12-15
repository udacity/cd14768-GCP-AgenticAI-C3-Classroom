# Module 9: Implementing Long-Term Agent Memory with ADK and VertexAI Agent Engine Memory Bank

This exercise asked you to build a research agent that had both access
to factual data using the `google_search` tool, as well as conversational
summaries from past sessions that were saved using the Agent Engine
Memory Bank.

---

## Overview

### What You've Learned

You have learned how to combine external tools (Google Search) with long-term
memory to create a research assistant that can recall information across
different sessions.

Learning objectives:

- Integrate `preload_memory_tool` and `auto_save_session_to_memory_callback`
  into a multi-tool agent.
- Coordinate between a search tool and a memory tool.
- Manage persistent state for a research assistant agent.

### Prerequisites

- Understanding of ADK tools and agents.
- Understanding how to integrate Grounding with Google Search and other tools
  in the ADK.

---

## Understanding the Concept

### The Problem

A research assistant often needs to perform multiple searches over time to
gather
information. If the agent forgets previous findings as soon as the session ends,
the user has to re-explain context or re-run searches, which is inefficient.

### The Solution

By equipping the agent with long-term memory, it can store the results of its
research (summarized by the Memory Bank). When the user returns for a follow-up
session, the agent can recall what was previously discussed and continue the
research without starting from scratch.

### How It Works

**Step 1: Search and Summarize**
The agent uses the `search_agent_tool` to find information on the web. The
conversation, including these findings, is saved to the Memory Bank at the end
of the turn.

**Step 2: Recall**
In a new session, the `preload_memory_tool` injects relevant summaries of past
research into the context. The agent uses this to answer questions or refine its
search strategy.

---

## CODE WALKTHROUGH

### Repository Structure

```
.
├── __init__.py
├── agent-prompt.txt    # System prompt for the main agent
├── agent.py            # Main agent implementation
├── requirements.txt
├── search-prompt.txt   # System prompt for the search agent
└── search_agent.py     # Helper agent for Google Search
```

### Step 1: Imports and Environment Setup

The solution begins by importing necessary modules, including the
`preload_memory_tool` for loading memories and `search_agent_tool` for
performing
searches. It also retrieves the Agent Engine configuration from environment
variables.

```python
import os
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from .search_agent import search_agent_tool
from google.adk.tools.preload_memory_tool import preload_memory_tool
```

**Key points:**

- `preload_memory_tool`: This tool is crucial for injecting past context into
  the agent's current session.

### Step 2: Saving Sessions to Memory

We define an asynchronous callback function that executes after every agent
turn.
This function takes the current session state and saves it to the Memory Bank.

```python
async def auto_save_session_to_memory_callback(
    callback_context: CallbackContext):
  print("save session to memory")
  await callback_context._invocation_context.memory_service.add_session_to_memory(
    callback_context._invocation_context.session)
```

**Key points:**

- `add_session_to_memory`: This method sends the conversation history to the
  Agent Engine for summarization and storage.
- `CallbackContext`: Provides access to the agent's internal state and services.

### Step 3: Agent Initialization

Finally, we configure the `root_agent` with the necessary tools and the saving
callback.

```python
tools = [
  search_agent_tool,
  preload_memory_tool
]

root_agent = Agent(
  name="research_assistant_agent",
  description="An agent that can search the web and has long-term memory of past conversations.",
  instruction=instruction,
  model=model,
  tools=tools,
  after_agent_callback=auto_save_session_to_memory_callback,
)
```

**Key points:**

- `tools`: Includes both the capability to search (`search_agent_tool`) and the
  capability to remember (`preload_memory_tool`).
- `after_agent_callback`: Ensures that the memory saving logic runs
  automatically after the agent has completed the work for a request.

### Complete Example

```python
import os
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from .search_agent import search_agent_tool
from google.adk.tools.preload_memory_tool import preload_memory_tool


# 1. Callback for saving memory
async def auto_save_session_to_memory_callback(
    callback_context: CallbackContext):
  print("save session to memory")
  await callback_context._invocation_context.memory_service.add_session_to_memory(
    callback_context._invocation_context.session)


script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
  instruction = f.read()

model = "gemini-2.5-flash"

# 2. Tool List
tools = [
  search_agent_tool,
  preload_memory_tool
]

# 3. Agent Definition
root_agent = Agent(
  name="research_assistant_agent",
  description="An agent that can search the web and has long-term memory of past conversations.",
  instruction=instruction,
  model=model,
  tools=tools,
  after_agent_callback=auto_save_session_to_memory_callback,
)
```

**How it works:**

1. The agent initializes with search and memory tools.
2. When a user asks a question, the agent uses `search_agent_tool` to find
   answers.
3. After answering, `auto_save_session_to_memory_callback` saves the
   interaction.
4. In the next session, `preload_memory_tool` loads the summarized context,
   allowing the agent to "remember" the previous findings.

**Expected output (Session 1):**

```
User: Search for the release date of Python 3.13.
Agent: (Uses search tool) Python 3.13 is expected to be released in October 2024...
(Console): save session to memory
```

**Expected output (Session 2):**

```
User: When is the new Python coming out?
Agent: As we found in our last research, Python 3.13 is expected in October 2024.
```

### Verification: Viewing Memory in Cloud Console

To confirm that your agent is successfully saving memories:

1. Visit the [Google Cloud Console](https://console.cloud.google.com/).
2. In the search bar at the top, type **"Agent Engine"** and select the
   service.
3. Click on the name of the Agent Engine instance you created.
4. Select the **"Memories"** tab.
5. You should see a list of users (or session IDs) and their stored memories.
6. Look for the summary of your recent conversation (e.g., facts about Python
   release dates).
7.  Clicking on the "Edit" button (three dots) will allow you to see the exact
    text that was saved and is available for recall.

---

## Comparison with Session/User State

You should be familiar with how the ADK works with Session and User state
and how tools can explicitly get and set values from this state. It is
important to understand how they differ from using long-term memory in this way:

- **Session State**:
    - Ephemeral data relevant only to the current conversation
      (e.g., current travel itinerary).
    - Lost when the session ends or is reset.
    - Values are readable and writable in a tool and you can specify where the
      values are inserted in the prompt.
- **User State**:
    - Key-value pairs linked to a user (e.g., "favorite_color":
      "blue").
    - Lasts longer than a session
    - Good for structured preferences but limited in complexity.
    - Values are readable and writable in a tool and you can specify where the
      values are inserted in the prompt.
- **Agent Engine Memory Bank (Long-Term Memory)**:
    - Designed for unstructured,
      semantic memories (e.g., "The user mentioned they like hiking in the fall").
    - Uses AI to summarize and index conversations, allowing for "fuzzy" recall
      of concepts over time, rather than just exact key matches.
    - Lasts longer than a session
    - Hooks save the conversation summary after each round of the conversation
      and a specialized tool adds the summary to the prompt before messages
      are sent to the LLM

---

## Important Details

### Best Practices

1. **Separation of Concerns**: We use a separate `search_agent` to handle the
   complexity of searching, while the `root_agent` manages the overall
   conversation and memory.
2. **Prompt Engineering**: Explicitly telling the agent to "remember" or
   "recall" helps the LLM understand the context that is injected later in 
   the prompt.
