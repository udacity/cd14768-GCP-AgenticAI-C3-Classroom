# Module 1 Exercise: Implementing Calculator Tools

Build an agent that utilizes external Python functions to perform accurate
mathematical calculations.


---

## Overview

### What You'll Learn

In this exercise, you will practice creating an agent that uses tools to
overcome
the limitations of Large Language Models (LLMs) in performing mathematical
calculations. You will define Python functions as tools, register them with
the ADK agent, and craft a prompt that guides the agent to use them effectively.

Learning objectives:

- Define Python functions to serve as agent tools
- Register tools with an ADK agent
- Craft a system prompt that encourages correct tool usage

### Prerequisites

- Completed Module 1 Demo
- Basic Python programming knowledge (functions, arguments, return values)

---

## Understanding the Concept

### The Problem

While LLMs are excellent at language tasks, they often struggle with precise
mathematical calculations, especially with larger numbers or complex operations.
They predict the next token based on patterns rather than performing actual
arithmetic, which can lead to "hallucinated" or incorrect results.

### The Solution

To solve this, we can provide the agent with "tools"—deterministic code
functions—that it can call when it detects a mathematical request. This allows
the agent to delegate the calculation to a reliable execution engine (Python)
while handling the natural language understanding and response generation.

### How It Works

1. **User Request**: The user asks a math question (e.g., "What is 1234 *
   5678?").
2. **Tool Selection**: The agent recognizes the need for calculation and
   selects the appropriate tool (e.g., `multiplication`).
3. **Execution**: The Python function runs with the provided arguments.
4. **Response**: The function returns the result, and the agent incorporates it
   into a natural language answer.

### Key Terms

**Determinism**: The property of a system (like a calculator tool) always
producing the same output for the same input, unlike the probabilistic nature of
LLMs.

**Tool Registration**: The process of explicitly making a function available to
the LLM agent by passing it in the `tools` list.


---

## Exercise Instructions

### Your Task

You need to complete the implementation of a "Calculator Agent". This agent
should be able to handle four basic arithmetic operations: addition,
subtraction,
multiplication, and division. You will implement the tool functions, add them
to the agent's tool list, and provide the necessary instructions in the prompt
file.

### Requirements

Your implementation must:

1. Complete the four tool functions: `addition`, `subtraction`,
   `multiplication`, and `division` in `agent.py`.
2. Update the `tools` list in `agent.py` to include these functions.
3. Write a clear and effective system prompt in `agent-prompt.txt` that
   instructs the agent on its role and how to use the tools.

### Repository Structure

```
.
├── __init__.py           # Initializes the Python package.
├── agent-prompt.txt      # TODO: You will add the agent instructions here.
├── agent.py              # TODO: You will implement tool functions and register them here.
├── requirements.txt      # Lists dependencies.
└── .env-sample           # Sample environment variables.
```

### Environment variables

Make sure you copy ".env-sample" to ".env" and edit it to add the Google 
Cloud project you are working with.

Remember that you should **never** check-in your .env file to git.

### Starter Code

The `agent.py` file provides the structure but lacks the logic. You need to fill
in the function bodies and the tools list.

```python
import os
from google.adk.agents import Agent

# TODO: Define the tools we need

# Experiment with the different models to see what works better
model = "gemini-2.5-flash"

# ...

# TODO: Add the tools to this list
tools = [
]

root_agent = Agent(
  name="calculator_tools",
  description="Multiple tools to do different mathematical calculations",
  model=model,
  tools=tools,
  instruction=instruction,
)
```

### Expected Behavior

Once completed, your agent should be able to accurately answer math questions by
calling the appropriate tools.

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

Once the server is running:
1. Select the name of the agent you are testing in the upper left corner. 
   Agents are named based on the name of the subdirectory.
2. In the lower right, you can enter in questions.

For example, try asking it:
```text
What is fifty plus twenty-five?
```

**Expected output:**

You will see events that the ADK has recorded to execute your request. These 
include the LLM request to call the tool, the tool run itself that is sent 
back to the LLM, and the final message from the LLM. You can click on each 
event to get details about what was done. 

```text
⚡ addition
✔️addition
Fifty plus twenty-five is 75.
```

### Implementation Hints

1. **Type Hinting**: Ensure your tool functions have correct type hints (e.g.,
   `int`, `float`). The ADK uses these to tell the LLM what kind of data to
   provide.
2. **Docstrings**: Write clear docstrings for your functions. The LLM reads
   these to understand what the tool does.
3. **Division**: Remember to handle the case where `b` is 0 in your division
   function to avoid crashing the program.
4. **Prompt**: In `agent-prompt.txt`, tell the agent it is a calculator and
   should use the available tools for math questions.

---

## Important Details

### Common Misconceptions

**Misconception**: "The LLM calculates the answer itself."
**Reality**: The LLM only *extracts* the numbers and *calls* the function. The
Python interpreter calculates the answer.

**Misconception**: "I don't need docstrings if the function name is clear."
**Reality**: While clear names help, docstrings provide the context and semantic
meaning that the LLM relies on to choose the correct tool among many. You 
can even use docstrings to clarify parameters and if they are optional.

### Best Practices

1. **Error Handling**: Implement basic error handling (like zero division
   checks) within your tools to make the agent more robust.
2. **Simple Prompts**: Keep the system prompt simple and direct. Focus on the
   agent's capabilities and constraints.

### Common Errors

**Error**: The agent says "I cannot calculate that" or hallucinates an answer
without using a tool.

- **Cause**: The tools might not be added to the `tools` list, the prompt
  doesn't encourage tool usage, or the model may not be well tuned to use tools.
- **Solution**: Verify the `tools` list in `agent.py` and ensure
  `agent-prompt.txt` explicitly mentions the available capabilities. Test 
  with different models to see which work best.

**Error**: `ValueError: Cannot divide by zero.`

- **Cause**: The division tool was called with `b=0` and the function didn't
  handle it gracefully or the user asked for it.
- **Solution**: Add a check in the `division` function: `if b == 0: ...`
