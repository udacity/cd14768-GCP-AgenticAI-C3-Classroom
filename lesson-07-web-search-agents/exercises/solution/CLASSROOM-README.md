# Module 7 Exercise Solution: Using other tools with Google Search

This solution demonstrates how to build a robust financial assistant that
combines
web search capabilities with custom calculation tools using a multi-agent
architecture.

---

## Overview

### What You'll Learn

This solution implements a multi-layered agent system where a specialized
search agent retrieves data, a structured agent formats it, and a root agent
performs calculations.

Learning objectives:

- Implement `AgentTool` to wrap agents as tools.
- Orchestrate a chain of agents: Search -> Structure -> Calculate.
- Use Pydantic models to enforce structured output from a sub-agent.

### Prerequisites

- Understanding of the Exercise requirements.
- Familiarity with ADK `Agent`, `AgentTool`, and Pydantic.

---

## Understanding the Concept

### The Problem

We needed to fetch real-time stock data (which requires Google Search) but also
perform calculations on that data. Gemini restricts mixing the `google_search`
tool with other tools or structured outputs directly.

### The Solution

We solved this with a 3-layer architecture:

1. **`search_agent`**: A base agent with access to the `google_search` tool. It
   performs the raw information retrieval.
2. **`structured_search_agent`**: An agent that calls the `search_agent` (via
   `AgentTool`) and uses an `output_schema` (`StockSearchResult`). This ensures
   the messy search results are converted into a clean, predictable JSON format.
3. **`financial_assistant_agent`**: The root agent. It sees the
   `structured_search_agent` as just another tool (`search_agent_tool`). It
   calls this tool to get data, then calls its calculation tools (`tools.py`) to
   answer the user's question.

---

## CODE WALKTHROUGH

### Repository Structure

```
.
├── __init__.py
├── agent-prompt.txt      # Root agent instructions
├── agent.py              # Root agent configuration
├── search_agent.py       # Search & Structure agent chain
├── search-prompt.txt     # Search agent instructions
├── tools.py              # Calculation tools
├── .env-sample
└── requirements.txt
```

### Step 1: Calculation Tools (`tools.py`)

We implemented simple Python functions for the math logic.

```python
def calculate_percentage_change(initial_value: float, final_value: float):
  if initial_value == 0:
    return {"error": "Initial value cannot be zero."}
  percentage_change = ((final_value - initial_value) / initial_value) * 100
  return {"percentage_change": percentage_change}


def calculate_profit_or_loss(number_of_shares: int, purchase_price: float,
                             current_price: float):
  # ... logic ...
  return {"profit_or_loss": profit_or_loss}
```

### Step 2: The Search Agent Chain (`search_agent.py`)

This is the core of the solution.

**1. The Base Search Agent**
This agent has the `google_search` tool.

```python
tools = [google_search]

search_agent = Agent(
  name="search_agent",
  # ...
  tools=tools,
)
```

**2. The Structured Output Model**
We define what the data *should* look like.

```python
class StockSearchResult(BaseModel):
  ticker: str = Field(..., description="Stock ticker symbol")
  current_price: float = Field(..., description="Current stock price")
  # ... other fields
```

**3. The Structured Agent**
This agent uses the `search_agent` as a tool (`AgentTool(agent=search_agent)`)
and enforces the `output_schema`.

```python
structured_search_agent = Agent(
  name="structured_search_agent",
  # ...
  tools=[AgentTool(agent=search_agent)],
  output_schema=StockSearchResult,
)
```

**4. The Final Tool**
We wrap the structured agent so the root agent can use it.

```python
search_agent_tool = AgentTool(agent=structured_search_agent)
```

### Step 3: The Root Agent (`agent.py`)

The root agent brings everything together. It has access to the
`search_agent_tool` (which gives it structured data) and the local calculation
functions.

```python
tools = [
  search_agent_tool,
  calculate_percentage_change,
  calculate_profit_or_loss
]

root_agent = Agent(
  name="financial_assistant_agent",
  description="An agent that can find financial information and perform calculations.",
  # ...
  tools=tools
)
```

### Complete Example

**User Query**: "What is the profit if I bought 10 shares of GOOG at $150
and I sold it today??"

1. **Root Agent**: Decides it needs the current price of GOOG. Calls
   `search_agent_tool`.
2. **Structured Agent**: Receives request. Calls its tool (the `search_agent`).
3. **Search Agent**: Receives request. Calls `google_search`. Finds price is $
   160. Returns text.
4. **Structured Agent**: Takes text, formats it into `StockSearchResult` JSON (
   `current_price: 160.0`). Returns JSON.
5. **Root Agent**: Receives JSON. Now has `current_price=160.0`. Calls
   `calculate_profit_or_loss(10, 150, 160)`.
6. **Tool**: Returns `100.0`.
7. **Root Agent**: Responds "You made a profit of $100.00."

---

## Important Details

### Best Practices

- **Layered Agents**: Breaking complex tasks into specialized agents (one for
  searching, one for structuring) works around the problem that Gemini 
  imposes with Grounding with Google Search.
- **AgentTool**: This is a powerful way to compose agents, treating entire
  intelligent subsystems as simple function calls for a higher-level agent.