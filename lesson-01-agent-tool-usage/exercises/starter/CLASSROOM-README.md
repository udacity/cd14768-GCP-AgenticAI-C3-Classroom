# Module 1 Exercise: Implementing Calculator Tools


Build an agent that utilizes external Python functions to perform accurate 
mathematical calculations.


---


## Overview


### What You'll Learn


In this exercise, you will practice creating an agent that uses tools to overcome
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


1.  **User Request**: The user asks a math question (e.g., "What is 1234 * 5678?").
2.  **Tool Selection**: The agent recognizes the need for calculation and selects the appropriate tool (e.g., `multiplication`).
3.  **Execution**: The Python function runs with the provided arguments.
4.  **Response**: The function returns the result, and the agent incorporates it into a natural language answer.


### Key Terms


**Determinism**: The property of a system (like a calculator tool) always producing the same output for the same input, unlike the probabilistic nature of LLMs.


**Tool Registration**: The process of explicitly making a function available to the LLM agent by passing it in the `tools` list.


---


## Exercise Instructions


### Your Task


You need to complete the implementation of a "Calculator Agent". This agent
should be able to handle four basic arithmetic operations: addition, subtraction,
multiplication, and division. You will implement the tool functions, add them
to the agent's tool list, and provide the necessary instructions in the prompt file.


### Requirements


Your implementation must:
1.  Complete the four tool functions: `addition`, `subtraction`, `multiplication`, and `division` in `agent.py`.
2.  Update the `tools` list in `agent.py` to include these functions.
3.  Write a clear and effective system prompt in `agent-prompt.txt` that instructs the agent on its role and how to use the tools.


### Repository Structure


```
.
├── __init__.py           # Initializes the Python package.
├── agent-prompt.txt      # TODO: You will add the agent instructions here.
├── agent.py              # TODO: You will implement tool functions and register them here.
├── requirements.txt      # Lists dependencies.
└── .env-sample           # Sample environment variables.
```


### Starter Code


The `agent.py` file provides the structure but lacks the logic. You need to fill in the function bodies and the tools list.


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


Once completed, your agent should be able to accurately answer math questions by calling the appropriate tools.


**Example usage:**
You can run the agent using the ADK CLI (assuming you are in the root of the project):


```bash
adk run lesson-01-agent-tool-usage/exercises/starter/agent.py "What is 50 plus 25?"
```


**Expected output:**
The output should look something like this (logs will show the tool call):


```text
...
Function Call: addition(a=50, b=25)
Result: 75
...
Agent: The answer is 75.
```


### Implementation Hints


1.  **Type Hinting**: Ensure your tool functions have correct type hints (e.g., `int`, `float`). The ADK uses these to tell the LLM what kind of data to provide.
2.  **Docstrings**: Write clear docstrings for your functions. The LLM reads these to understand what the tool does.
3.  **Division**: Remember to handle the case where `b` is 0 in your division function to avoid crashing the program.
4.  **Prompt**: In `agent-prompt.txt`, tell the agent it is a calculator and should use the available tools for math questions.


---


## Important Details


### Common Misconceptions


**Misconception**: "The LLM calculates the answer itself."
**Reality**: The LLM only *extracts* the numbers and *calls* the function. The Python interpreter calculates the answer.


**Misconception**: "I don't need docstrings if the function name is clear."
**Reality**: While clear names help, docstrings provide the context and semantic meaning that the LLM relies on to choose the correct tool among many.


### Best Practices


1.  **Error Handling**: Implement basic error handling (like zero division checks) within your tools to make the agent more robust.
2.  **Simple Prompts**: Keep the system prompt simple and direct. Focus on the agent's capabilities and constraints.


### Common Errors


**Error**: The agent says "I cannot calculate that" or hallucinates an answer without using a tool.
- **Cause**: The tools might not be added to the `tools` list, or the prompt doesn't encourage tool usage.
- **Solution**: Verify the `tools` list in `agent.py` and ensure `agent-prompt.txt` explicitly mentions the available capabilities.


**Error**: `ValueError: Cannot divide by zero.`
- **Cause**: The division tool was called with `b=0` and the function didn't handle it gracefully or the user asked for it.
- **Solution**: Add a check in the `division` function: `if b == 0: ...`
