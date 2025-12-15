# Module 9: Implementing Long-Term Agent Memory with ADK and VertexAI Agent Engine Memory Bank

In this exercise, you'll be creating a research assistant that searches the 
web, but also maintains historical context of what the researcher has been 
working on. To do this, you'll implement long-term agent memory using ADK 
and Vertex AI Agent Engine Memory Bank.

---

## Overview

### What You'll Learn

You will learn how to combine external tools (Google Search) with long-term
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

A research assistant often needs to perform multiple searches over time to gather
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

## Exercise Instructions

### Setup: Agent Engine Memory Bank

Before writing any code, you must set up the backend service that will store the
agent's memory.

1.  **Configure Environment**:
    Ensure you have your `.env` file set up (copy from `.env-sample`). You need
    the basic Google Cloud configuration:

    ```bash
    GOOGLE_GENAI_USE_VERTEXAI=TRUE
    GOOGLE_CLOUD_PROJECT=<your project ID>
    GOOGLE_CLOUD_LOCATION=us-central1
    ```

2.  **Create Agent Engine Instance**:
    Navigate to the `notes` folder and run the
    creation script:

    ```bash
    python create_agent_engine.py
    ```

3.  **Update Configuration**:
    The script will output a **resource name**. Copy this value to use when 
    you run `adk web`.

    *Note: If you lose the resource name, you can find it in the Google Cloud
    Console by searching for "Agent Engine" and viewing your instance details.*

### Your Task

Build a "Research Assistant" agent that uses Google Search to answer questions
and the Vertex AI Agent Engine Memory Bank to remember what it has learned
across sessions.

### Requirements

Your implementation must:

1. **Implement Callback**: Write the `auto_save_session_to_memory_callback` to
    save the current session to the memory service.
2. **Configure Tools**: Add both the `search_agent_tool` (provided) and the
    `preload_memory_tool` to the agent's tool list.
3. **Register Callback**: Ensure the `root_agent` calls your saving callback
    after each turn.
4. **Write Prompts**: Complete `agent-prompt.txt` to instruct the agent to use
    memory, and `search-prompt.txt` to guide the search helper.

### Repository Structure

```
.
├── .env-sample         # Template for environment variables
├── __init__.py
├── agent-prompt.txt    # TODO: System prompt for the main agent
├── agent.py            # TODO: Main agent implementation
├── requirements.txt
├── search-prompt.txt   # TODO: System prompt for the search agent
└── search_agent.py     # provided: Helper agent for Google Search
```

**Note on Search Tool**:
The `search_agent.py` file contains a fully configured ADK agent that wraps the
Google Search tool. You do not need to modify this file. It is imported as
`search_agent_tool` in your main `agent.py` and simply needs to be added to
your tool list.

### Starter Code

The `agent.py` file provides the structure but is missing the memory
integration.

```python
import os
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
# TODO: Import the preload memory tool and search agent tool

async def auto_save_session_to_memory_callback(callback_context: CallbackContext):
    # TODO: Create the callback function to save session to memory
    pass

# ... (agent setup) ...

tools = [
    # TODO: Add the tools we need
]

root_agent = Agent(
    # ...
    # TODO: Register the callback
)
```

### Expected Behavior

1.  **Session 1**: You ask the agent to search for "latest features of Python
    3.12". The agent searches and summarizes the findings.
2.  **Session 2**: You ask "What did we find out about Python 3.12?". The agent
    should answer based on the memory of the previous session without needing to
    search again.

**Running the agent:**

```bash
adk web --memory_service_uri agentengine://<agent engine resource name>
```

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

1.  Visit the [Google Cloud Console](https://console.cloud.google.com/).
2.  In the search bar at the top, type **"Agent Engine"** and select the
    service.
3.  Click on the name of the Agent Engine instance you created during setup.
4.  Select the **"Memories"** tab.
5.  You should see a list of users (or session IDs) and their stored memories.
6.  Look for the summary of your recent conversation (e.g., facts about Python
    release dates).
7.  If you see the data here, your `auto_save_session_to_memory_callback` is
    working correctly!

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

### Implementation Hints

1.  **Callback Syntax**: The callback must be `async` and take a
    `CallbackContext`. You access the memory service via
    `callback_context._invocation_context.memory_service`.
2.  **Tool Imports**: You need `preload_memory_tool` from
    `google.adk.tools.preload_memory_tool` and `search_agent_tool` from the
    local `.search_agent` module.
3.  **Prompting**: In `agent-prompt.txt`, explicitly tell the agent it is a
    research assistant and that it *must* remember past conversations to help the
    user effectively.
