# Module 9: Implementing Long-Term Agent Memory with ADK and VertexAI Agent Engine Memory Bank

This lesson teaches how to implement long-term agent memory using ADK and Vertex
AI Agent Engine Memory Bank.

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

- Completion of the Module 9 Demo.
- Understanding of ADK tools and agents.
- A configured Agent Engine instance (from the demo or a new one).

---

## Understanding the Concept

### The Problem

A research assistant often needs to perform multiple searches over time to
gather information. If the agent forgets previous findings as soon as the
session ends, the user has to re-explain context or re-run searches, which is
inefficient.

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

### Your Task

Build a "Research Assistant" agent that uses Google Search to answer questions
and the Vertex AI Agent Engine Memory Bank to remember what it has learned
across sessions.

### Requirements

Your implementation must:

1. Configure the agent to use the Agent Engine environment variables.
2. Implement the `auto_save_session_to_memory_callback` to save sessions.
3. Add the `preload_memory_tool` to the agent's tool list alongside the
   `search_agent_tool`.
4. Register the callback with the `root_agent`.
5. Complete the `agent-prompt.txt` to instruct the agent to use its memory and
   search capabilities.

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

Make sure you copy `.env-sample` to `.env` and edit it to add the Google
Cloud project and Agent Engine details you are working with.

**Note:** You can reuse the `AGENT_ENGINE_ID` from the demo, or create a new one
using the script in the `notes` folder.

### Starter Code

The `agent.py` file provides the structure but is missing the memory
integration.

```python
import os
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from .search_agent import search_agent_tool
# TODO: Import the preload memory tool

# TODO: Get environment variables for Agent Engine

# TODO: Create the callback function to save session to memory
# async def auto_save_session_to_memory_callback(callback_context: CallbackContext):
#     pass
```

### Expected Behavior

1. **Session 1**: You ask the agent to search for "latest features of Python
   3.12". The agent searches and summarizes the findings.
2. **Session 2**: You ask "What did we find out about Python 3.12?". The agent
   should answer based on the memory of the previous session without needing to
   search again.

**Running the agent:**

```bash
adk web
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

### Implementation Hints

1. Refer to the `demo/agent.py` for the exact syntax of the callback and
   imports.
2. Don't forget to import `preload_memory_tool` and add it to the `tools` list.
3. Your prompt in `agent-prompt.txt` is crucial. It should tell the agent that
   it is a research assistant and that it should remember past research.
4. For `search-prompt.txt`, a simple instruction like "You are a helpful
   assistant that searches the web" is sufficient.

---

## Important Details

### Common Misconceptions

**Misconception**: "I need to manually save every search result to a database."
**Reality**: "The Agent Engine Memory Bank automatically summarizes the
conversation, which includes the results provided by the search tool. You just
need to save the session."

### Best Practices

1. **Separation of Concerns**: We use a separate `search_agent` to handle the
   complexity of searching, while the `root_agent` manages the overall
   conversation and memory.
2. **Prompt Engineering**: Explicitly telling the agent to "remember" or "
   recall" helps the LLM trigger the right behavior when context is injected.
