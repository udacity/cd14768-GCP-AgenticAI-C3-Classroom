# Module 7 Exercise Solution: Using other tools with Google Search

This solution demonstrates a multi-agent system where a specialized search agent
acts as a tool for a financial assistant agent. This allows the system to combine
real-time web data with custom financial calculations.

---

## Overview

### What You'll Learn

This solution illustrates how to overcome the limitation of mixing Gemini's
built-in tools (like Google Search) with custom Python tools. By wrapping a
search-enabled agent in an `AgentTool`, we create a modular system where
responsibilities are cleanly separated.

Learning objectives:

- Implementing the `AgentTool` pattern to nest agents.
- Creating specialized sub-agents with focused prompts.
- Integrating calculation tools to process retrieved data.

### Prerequisites

- A Google Cloud Project with Vertex AI enabled.
- Understanding of the "Grounding with Google Search" feature.

---

## Understanding the Concept

### The Problem

We want an agent that can both "search the web for the latest stock price" and
"calculate profit/loss based on that price". However, directly mixing the
`google_search` tool with custom function tools in a single agent can be
problematic or unsupported depending on the model and platform constraints.
Additionally, keeping the search logic separate from the calculation logic makes
the system easier to maintain.

### The Solution

1. **Sub-Agent (`search_agent.py`)**: We created a dedicated agent whose sole
   purpose is to search. It uses the `google_search` tool.
2. **Wrapper (`AgentTool`)**: We wrapped this search agent in an `AgentTool`.
   This makes the entire agent look like a simple tool (function) to other
   agents.
3. **Main Agent (`agent.py`)**: The root agent sees `search_agent_tool` as just
   another tool in its toolkit, alongside `calculate_profit_or_loss`. It calls
   the search tool to get data, then calls the calculation tool to process it.

---

## CODE WALKTHROUGH

### Repository Structure

```
.
├── __init__.py           # Package initialization.
├── agent-prompt.txt      # Main agent instructions.
├── agent.py              # Main agent configuration.
├── search_agent.py       # Sub-agent definition and AgentTool creation.
├── search-prompt.txt     # Sub-agent instructions.
├── tools.py              # Custom calculation tools.
├── README.md             # Overview.
└── requirements.txt      # Dependencies.
```

### Step 1: The Search Agent (`search_agent.py`)

This agent is configured with the `google_search` tool.

```python
search_agent = Agent(
    name="search_agent",
    description="An agent that can search the web for stock information.",
    # ...
    tools=[google_search],
)

search_agent_tool = AgentTool(agent=search_agent)
```

**Key Detail**: The `AgentTool(agent=search_agent)` line is the bridge. It
exposes `search_agent` as a callable tool.

### Step 2: Calculation Tools (`tools.py`)

These are standard Python functions for deterministic math.

```python
def calculate_profit_or_loss(number_of_shares: int, purchase_price: float, current_price: float):
    total_cost = number_of_shares * purchase_price
    current_value = number_of_shares * current_price
    profit_or_loss = current_value - total_cost
    return {"profit_or_loss": profit_or_loss}
```

### Step 3: The Main Agent (`agent.py`)

The main agent integrates everything.

```python
tools = [
    search_agent_tool,
    calculate_percentage_change,
    calculate_profit_or_loss
]

root_agent = Agent(
    # ...
    tools=tools
)
```

### Step 4: Prompts

- **`search-prompt.txt`**: "You are a search agent. Your only purpose is to...
  find the latest stock information..." (Focused scope).
- **`agent-prompt.txt`**: "You are a financial assistant. You can use Google
  Search... and then perform calculations..." (Orchestration scope).

### Complete Example

1. **User**: "I bought 10 shares of Apple at $150. How much money have I made?"
2. **Main Agent**: "I need the current price of Apple. Calling
   `search_agent_tool`."
3. **Search Agent**: Calls the LLM as part of a different session to request 
   it to search for the current price of Apple using the `google_search` tool. 
   Returns "$220".
4. **Main Agent**: "I have the current price ($220) and purchase price ($150).
   Calling `calculate_profit_or_loss`."
5. **Tool**: Returns `{"profit_or_loss": 700}`.
6. **Main Agent**: "You have made a profit of $700."

---

## Important Details

### Best Practices

- **Focused Sub-Agents**: Keep sub-agents simple. If `search_agent` tried to do
  calculations too, it might get confused. By restricting it to just "find
  data," it becomes a reliable component.
- **Explicit Interfaces**: When using `AgentTool`, ensure the sub-agent's
  description clearly states what it does so the main agent knows when to call
  it.

### Common Errors

- **Infinite Loops**: If the main agent and sub-agent both think they are responsible
  for the high-level task, they might pass the buck back and forth. Distinct prompts prevent this.
- **Data Handoff**: Sometimes the sub-agent returns too much text. Instructing
  it to be concise or structured helps the main agent parse the result.
