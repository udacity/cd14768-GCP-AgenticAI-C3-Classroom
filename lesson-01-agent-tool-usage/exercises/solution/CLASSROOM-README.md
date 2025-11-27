# Module 1 Exercise: Implementing Calculator Tools

This exercise demonstrates how to build an agent that accurately performs
mathematical calculations by leveraging external Python functions as tools.


---

## Overview

### What You'll Learn

This exercise focuses on implementing an ADK agent that utilizes specific
tools to perform arithmetic operations, showcasing how LLMs can delegate complex
or deterministic tasks to external functions. You will gain practical experience
in defining, implementing, and integrating tools within an ADK agent.

Learning objectives:

- Define and implement tool functions with proper type hints and docstrings
- Integrate these custom tools into an ADK agent
- Craft an effective system prompt to guide the agent's tool usage for specific
  tasks

### Prerequisites

- Basic understanding of Python programming
- Familiarity with the concepts of LLMs and tool usage (as covered in the demo)

---

## Understanding the Concept

### The Problem

While Large Language Models (LLMs) excel at language understanding and
generation,
they often struggle with precise mathematical calculations. Their strength lies
in pattern recognition and probabilistic text generation, not deterministic
arithmetic. Relying on an LLM for exact math can lead to inaccuracies or
"hallucinations."

### The Solution

The solution involves extending the LLM's capabilities with external tools. By
providing the agent with Python functions designed to perform specific
mathematical operations, we enable it to delegate calculation tasks to a
reliable
and deterministic executor. The LLM acts as an intelligent router, determining
when a calculation is needed and which tool to use, while the tool provides the
accurate result.

### How It Works

1. **Customer Inquiry**: The customer submits a query involving a mathematical
   calculation (e.g., "What is 25 multiplied by 4?").
2. **Tool Selection**: The LLM analyzes the query and identifies that a
   mathematical operation is required. Based on the available tool definitions (
   docstrings and function signatures), it determines the most appropriate
   tool (e.g., `multiplication`).
3. **Function Calling**: The LLM generates a structured function call,
   extracting the necessary arguments from the customer's query (e.g.,
   `multiplication(a=25, b=4)`).
4. **Tool Execution**: The ADK executes the identified Python function with the
   provided arguments.
5. **Result Integration**: The precise result from the Python function is
   returned to the LLM. The LLM then uses this result to formulate a natural
   language response to the customer, ensuring accuracy.

### Key Terms

**Determinism**: In the context of tools, determinism means that a given input
will always produce the same output. This is crucial for tasks like mathematical
calculations where accuracy is paramount.

**Tool Registration**: The process of explicitly making a Python function
available to an ADK agent, allowing the LLM to discover and invoke it based on
customer prompts and the tool's metadata.


---

## CODE WALKTHROUGH

### Repository Structure

```
.
├── __init__.py           # Initializes the Python package.
├── agent-prompt.txt      # Contains the agent's instructions and persona.
├── agent.py              # Defines the agent and its tool implementations.
├── README.md             # Provides environment setup information.
└── requirements.txt      # Lists the Python dependencies for the project.
```

### Step 1: Define Calculator Tools

The `agent.py` file defines four Python functions: `addition`, `subtraction`,
`multiplication`, and `division`. Each function is implemented to perform a
specific arithmetic operation and includes type hints for its arguments and
return value. Crucially, each function has a comprehensive docstring that
describes its purpose. These docstrings, along with the function signatures,
are what the LLM uses to understand the capabilities of each tool and how to
call them correctly. Note the error handling implemented in the `division`
function to prevent division by zero.

```python
def addition(a: int, b: int) -> int:
  """Adds two numbers."""
  return a + b


def subtraction(a: int, b: int) -> int:
  """Subtracts two numbers."""
  return a - b


def multiplication(a: int, b: int) -> int:
  """Multiplies two numbers."""
  return a * b


def division(a: int, b: int) -> float:
  """Divides two numbers."""
  if b == 0:
    raise ValueError("Cannot divide by zero.")
  return a / b
```

**Key points:**

- **Deterministic Logic**: Each function contains precise, deterministic logic
  for its operation.
- **Type Hinting**: Arguments and return values are type-hinted, which assists
  the LLM in understanding expected input and output types.
- **Descriptive Docstrings**: The docstrings are clear and concise, providing
  the LLM with sufficient information to decide when to invoke each tool.
- **Error Handling**: The `division` function includes a `ValueError` for
  division by zero, making the tool more robust.

### Step 2: Define Agent Instructions

The `agent-prompt.txt` file contains the system instructions for the agent.
This prompt establishes the agent's persona as a helpful mathematical assistant
and explicitly guides it to use the available tools to answer questions
involving
addition, subtraction, multiplication, and division. A well-crafted prompt is
essential for the LLM to effectively utilize its tools.

```text
You are a helpful assistant that can perform mathematical calculations. Use the
available tools to answer questions about addition, subtraction, multiplication,
and division.
```

**Key points:**

- **Persona Definition**: The prompt clearly defines the agent's role as a "
  helpful assistant for mathematical calculations."
- **Explicit Tool Usage**: It instructs the agent to "use the available tools to
  answer questions," directly encouraging function calling.
- **Scope Definition**: The prompt lists the specific operations the agent can
  handle, narrowing its focus.

### Step 3: Create the ADK Agent

The `agent.py` file then instantiates the ADK `Agent` class. It provides a
`name`
("calculator_tools"), a `description` outlining its capabilities, the `model`
to be used (e.g., "gemini-2.5-flash"), the `instruction` loaded from
`agent-prompt.txt`, and crucially, a list of all the implemented `tools`
(the `addition`, `subtraction`, `multiplication`, and `division` functions).
This setup makes the Python functions available for the Gemini model's function
calling mechanism.

```python
import os
from google.adk.agents import Agent

# ... (tool function definitions) ...

model = "gemini-2.5-flash"

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
  instruction = f.read()

tools = [
  addition,
  subtraction,
  multiplication,
  division,
]

root_agent = Agent(
  name="calculator_tools",
  description="Multiple tools to do different mathematical calculations",
  model=model,
  tools=tools,
  instruction=instruction,
)
```

**Key points:**

- **Agent Instantiation**: The `Agent` class from `google.adk.agents` is used to
  create the core agent.
- **Tool Integration**: The list of implemented tool functions is passed
  directly to the `tools` parameter, registering them with the agent.
- **Configuration**: The agent's behavior is configured via its `name`,
  `description`, `model`, and dynamic `instruction` from the prompt file.

### Complete Example

Here is the complete `agent.py` file, demonstrating a fully functional
calculator
agent built using the ADK. This agent can accurately interpret and respond to
mathematical queries by intelligently selecting and executing the appropriate
Python tool.

```python
import os
from google.adk.agents import Agent


def addition(a: int, b: int) -> int:
  """Adds two numbers."""
  return a + b


def subtraction(a: int, b: int) -> int:
  """Subtracts two numbers."""
  return a - b


def multiplication(a: int, b: int) -> int:
  """Multiplies two numbers."""
  return a * b


def division(a: int, b: int) -> float:
  """Divides two numbers."""
  if b == 0:
    raise ValueError("Cannot divide by zero.")
  return a / b


# Experiment with the different models to see what works better
model = "gemini-2.5-flash"

# Read the instructions from a file in the same
# directory as this agent.py file.
script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
  instruction = f.read()

tools = [
  addition,
  subtraction,
  multiplication,
  division,
]

root_agent = Agent(
  name="calculator_tools",
  description="Multiple tools to do different mathematical calculations",
  model=model,
  tools=tools,
  instruction=instruction,
)
```

**How it works:**

1. The agent receives a natural language query, such as "What is 100 divided by
   4?".
2. The Gemini model, guided by the agent's instructions and the tool
   definitions,
   recognizes the need for division and calls the `division` function with
   `a=100` and `b=4`.
3. The `division` function executes, returning `25.0`.
4. The agent then processes this result and generates a friendly
   response: "The result of 100 divided by 4 is 25.0."

**Expected output:**

```text
Human: "What is 5 plus 3?"
Agent: "The sum of 5 and 3 is 8."
```

```text
Human: "What is 100 divided by 4?"
Agent: "The result of 100 divided by 4 is 25.0."
```

---

## Important Details

### Common Misconceptions

**Misconception**: "The LLM calculates the answer itself."
**Reality**: The LLM does not perform calculations. It acts as an intelligent
router, extracting numerical values and operations from the customer's request
and invoking the appropriate external tool (the Python function) to get the
precise result.

**Misconception**: "I don't need docstrings if the function name is clear."
**Reality**: Docstrings are critical for tool functions. The LLM uses them to
understand the tool's purpose, its parameters, and when it should be called.
Clear docstrings improve the LLM's ability to correctly select and use tools,
especially when multiple tools have similar-sounding names.

### Best Practices

1. **Robust Error Handling**: Implement comprehensive error handling within your
   tool functions (e.g., handling division by zero, invalid inputs). This
   ensures
   the agent remains stable and can provide graceful responses even when
   unexpected
   conditions occur.
2. **Clear and Concise Prompts**: Keep the system prompt (`agent-prompt.txt`)
   focused on the agent's role and capabilities. Avoid overly verbose or
   ambiguous
   instructions that could confuse the LLM regarding tool usage.
3. **Type Hinting**: Consistently use type hints for all function arguments and
   return values. These provide explicit contracts for the LLM, helping it to
   correctly format function calls with the right data types.

### Common Errors

**Error**: The agent attempts to calculate mathematically instead of using a
tool.

- **Cause**: The agent's `tools` list might be empty, or the `agent-prompt.txt`
  does not sufficiently emphasize the use of tools for mathematical operations.
- **Solution**: Ensure all calculator functions are correctly registered in the
  `tools` list in `agent.py`, and review `agent-prompt.txt` to make instructions
  for tool usage more explicit.

**Error**: `ValueError: Cannot divide by zero.`

- **Cause**: The customer's query led to the `division` tool being called with
  `b=0`,
  and the tool correctly raised an error.
- **Solution**: This is a correct error response from the tool. The agent should
  be prompted to explain the error gracefully to the customer, or the tool 
  itself could return a more friendly message rather than raising an exception.
