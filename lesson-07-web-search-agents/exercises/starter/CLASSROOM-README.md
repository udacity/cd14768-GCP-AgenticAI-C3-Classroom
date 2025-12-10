# Module 7 Exercise: Using other tools with Google Search

This exercise challenges you to build a financial assistant agent that combines
web search capabilities with custom calculation tools. The core of this is
understanding how to leverage the `AgentTool` class to integrate a specialized
search agent as a tool within a broader financial assistant.

---

## Overview

### What You'll Learn

You will learn to implement a multi-agent system where one agent (a search
agent) acts as a tool for another agent (a financial assistant). This pattern
allows for modularity, specialization, and robust handling of complex tasks
involving both external data retrieval and custom logic.

Learning objectives:

- Understand and implement the `AgentTool` class to create hierarchical agents.
- Design and implement custom Python tools for specific calculations (e.g.,
  percentage change, profit/loss).
- Craft prompts for both the main agent and the sub-agent to guide their
  specialized tasks.
- Orchestrate multiple tools and a sub-agent to solve a complex problem.

### Prerequisites

- Basic understanding of Python.
- Familiarity with ADK agent structure and tool integration.
- Knowledge of grounding with Google Search.

---

## Understanding the Concept

### The Problem

While grounding with Google Search provides a powerful way to access real-time
information, it often returns raw data. For many tasks, we need to process or
calculate based on that data. For example, finding stock prices is one step;
calculating percentage change or profit/loss is another. Trying to cram all this
logic into a single agent's prompt or a single complex tool can lead to a less
reliable or maintainable system.

### The Solution

We'll solve this by creating specialized agents and tools:

1. **Search Agent (`search_agent.py`)**: A dedicated agent whose *only* job is
   to search Google for specific information (like stock data). It uses the
   built-in `google_search` tool.
2. **`AgentTool`**: This ADK class allows us to wrap an entire `Agent` instance
   and expose it as a tool to another agent. This is necessary because 
   Gemini does not let you combine the `google_search` tool with external 
   function tools.
3. **Calculation Tools (`tools.py`)**: Simple Python functions (
   `calculate_percentage_change`, `calculate_profit_or_loss`) that perform
   deterministic mathematical operations on the data retrieved by the search
   agent.

This architecture creates a powerful financial assistant by combining the
strengths of specialized components.

### How It Works

1. **User Query**: The user asks a question like, "What's the profit if I bought
   100 shares of GOOG at $150 and it closed at $160 today?"
2. **Main Agent Reasoning**: The `financial_assistant_agent` understands it
   needs current stock information *and* a calculation. It will decide to use
   its `search_agent_tool`.
3. **Sub-Agent Activation**: The `search_agent_tool` activates the
   `search_agent`. The `search_agent`, guided by its own prompt, makes its 
   own call to an LLM and uses `google_search` to find the current GOOG 
   stock price. 
4. **Data Retrieval**: The `search_agent` returns the stock data (e.g., current
   price) which gets sent back to the LLM working with our root agent, the 
   `financial_assistant_agent`.
5. **Main Agent Calculation**: The `financial_assistant_agent` then takes the
   retrieved current price and the user-provided purchase details and calls its
   `calculate_profit_or_loss` tool.
6. **Final Response**: The main agent synthesizes the results to answer the
   user's original question.

### Key Terms

**`AgentTool`**: An ADK class that turns a complete `Agent` instance into a tool
callable by another agent. This allows our root agent to call both 
function-based tools and Gemini's built-in tools by giving it an additional 
tool that calls its own agent.

**Tool Chaining**: The process where an agent calls multiple tools sequentially,
often using the output of one tool as input for the next, to achieve a complex
goal.

---

## EXERCISE INSTRUCTIONS

### Your Task

Your goal is to complete the `financial_assistant_agent` to provide stock
information and perform calculations. This involves implementing custom
calculation tools, writing specific prompts, and correctly wiring up the
`search_agent` as a tool.

1. **Implement Calculation Tools (`tools.py`)**:
    * `calculate_percentage_change(initial_value: float, final_value: float)`
    *
    `calculate_profit_or_loss(number_of_shares: int, purchase_price: float, current_price: float)`
2. **Write Sub-agent Prompt (`search-prompt.txt`)**:
    * Instruct the `search_agent` to use Google Search to find specific stock
      information (symbol, high, low, open, close, date).
3. **Create `search_agent` (`search_agent.py`)**:
    * Give it the correct tools for Grounding with Google Search
    * Complete the creation of an `Agent` that uses this tool
    * You'll see that the `search_Agent_tool` has been defined for you.
4. **Write Main Agent Prompt (`agent-prompt.txt`)**:
    * Instruct the `financial_assistant_agent` to use its tools (search
      sub-agent and calculation tools) to answer financial questions.
5. **Configure Main Agent (`agent.py`)**:
    * Import all necessary tools including the `search_agent_tool`.
    * Register them in the `root_agent`'s `tools` list.

### Requirements

1. The `financial_assistant_agent` must be able to use the `search_agent_tool`
   to get stock data.
2. It must be able to perform percentage change calculations.
3. It must be able to calculate profit or loss for stock transactions.
4. The `search_agent` must be specifically instructed to find detailed stock
   information.
5. The `AgentTool` class must be used to expose `search_agent` to the
   `root_agent`.

### Repository Structure

```
.
├── __init__.py           # Package initialization.
├── agent-prompt.txt      # (Your task) Main agent instructions.
├── agent.py              # (Your task) Main agent configuration.
├── search_agent.py       # (Your task) Sub-agent definition and AgentTool creation.
├── search-prompt.txt     # (Your task) Sub-agent instructions.
├── tools.py              # (Your task) Custom calculation tools.
├── .env-sample           # Environment variables.
└── requirements.txt      # Dependencies.
```

### Starter Code

**`agent.py`**:

```python
import os
from google.adk.agents import Agent

# TODO: Import the tools

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
  instruction = f.read()

model = "gemini-2.5-flash"

# TODO: Register the tools for the root agent
tools = [
]

root_agent = Agent(
  name="financial_assistant_agent",
  description="An agent that can find financial information and perform calculations.",
  instruction=instruction,
  model=model,
  tools=tools
)
```

**`search_agent.py`**:

```python
import os
from google.adk.agents import Agent
from google.adk.tools import google_search, AgentTool

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "search-prompt.txt")
with open(instruction_file_path, "r") as f:
  instruction = f.read()

model = "gemini-2.5-flash"

# TODO: Define the search tool
tools = [
]

# TODO: Create an agent that uses the search tool
search_agent =

# Create search_agent_tool by wrapping search_agent with AgentTool
search_agent_tool = AgentTool(agent=search_agent)
```

**`tools.py`**:

```python
def calculate_percentage_change(initial_value: float, final_value: float):
# TODO: Implement calculate_percentage_change
# Calculates the percentage change between two numbers.

def calculate_profit_or_loss(number_of_shares: int, purchase_price: float, current_price: float):
# TODO: Implement calculate_profit_or_loss
# Calculates the profit or loss from a stock transaction.
```

### Expected Behavior

**Running the agent:**

```bash
adk web
```

**Example usage:**

```text
Human: "What was the closing price of Google and if I bought 10 shares for $200, how much would I have made or lost?" 
Agent: "The closing price of Google (GOOG) on December 9, 2025, was $317.68.

If you bought 10 shares for $200 each, you would have made a profit of $1176.80."
```

### Implementation Hints

1. For `calculate_percentage_change`, remember to handle `initial_value == 0` to
   avoid `ZeroDivisionError`.
2. The `search_agent`'s prompt should be very specific about the type of stock
   information it needs to extract (e.g., symbol, open, close, high, low, date).
3. The main agent (`financial_assistant_agent`) will likely call the
   `search_agent_tool` first to get the current price, then use
   `calculate_profit_or_loss`.

---

## Important Details

### Best Practices

- **Clear Prompts for Sub-agents**: A sub-agent's prompt should clearly define
  its single purpose, what information it needs to find, and what format it
  should return it in. (Example: The `search_agent` prompt).
- **Use `AgentTool` Sparingly**: We need to use it in this case to "wrap" a 
  tool that otherwise couldn't be called, but be careful how you use it.

### Common Errors

**Error**: The main agent fails to call the search sub-agent or calls it with
incorrect parameters.

- **Cause**: The `search_agent_tool`'s description or the main agent's prompt
  isn't clear enough about the sub-agent's capabilities.
- **Solution**: Refine the `description` of `search_agent` and ensure
  `agent-prompt.txt` guides the main agent on when to ask for stock info via the
  search tool.

**Error**: The `search_agent` returns generic web search results instead of
specific stock data.

- **Cause**: The `search-prompt.txt` for the `search_agent` is not specific
  enough in asking for structured stock information.
- **Solution**: Make the `search-prompt.txt` explicit about needing stock
  symbol, prices (open, close, high, low), and date.