# Module 1: Implementing Agent Tool Usage with ADK and Vertex AI Gemini Function Calling


Explain how LLM-based agents use external tools (e.g.; Web Search; Database; APIs; Calculators) to expand their capabilities and interact with real-world systems; including concepts like function calling and the role of prompt/output parsing.


---


## Overview


### What You'll Learn


This module will teach you how to apply tool usage for LLM-based agents by
demonstrating Gemini's function calling capabilities and integrating pre-built
or custom tools within the Agent Development Kit (ADK).


Learning objectives:
- Learn ADK's tool structure
- Register and use tools with ADK agents
- Understand how the LLM uses tool responses


### Prerequisites


- Basic understanding of Python programming.
- Familiarity with the basic concepts of Large Language Models (LLMs).
- Basic familiarity with the ADK


---


## Understanding the Concept


### The Problem


Large Language Models (LLMs) are incredibly powerful at understanding and
generating human-like text. However, they have inherent limitations:
they can only access information up to their last training cut-off date and
cannot directly interact with external systems or perform real-time actions.
This means they cannot browse the web for current events, perform complex
calculations accurately, or interact with APIs to fetch live data without
assistance.


### The Solution


The concept of "tool usage" or "function calling" addresses these limitations
by allowing LLM-based agents to leverage external tools. These tools can be
anything from simple functions to complex API integrations, enabling the LLM
to access up-to-date information, perform specific actions, and interact
with the real world. This significantly expands the capabilities of LLM agents,
making them more versatile and powerful.


### How It Works


The process of an agent using tools typically involves several steps:


**Step 1: Customer Query**
The customer provides a natural language query or instruction to the LLM agent.
For example, "What's the weather like in London today?"


**Step 2: Tool Selection**
The LLM agent analyzes the customer's query and, based on its training and the
descriptions of available tools, decides if any of these tools can help
answer the query and uses one that seems likely to help answer the 
customer's request.


**Step 3: Function Calling**
If a tool is identified, the LLM formulates a "function call" – it generates
the precise name of the tool function to be executed along with the necessary
arguments extracted from the customer's query. For instance, `get_temperature
(city="London")`.


**Step 4: Tool Execution**
The ADK then executes the function that the LLM has requested, passing it 
the parameters that the LLM has specified.
The tool
performs its designated task, such as querying a weather API, running a
calculation, or accessing a database, and returning the results as the 
return value from the function call.


**Step 5: Response Generation**
The ADK then sends the output from the executed tool to the LLM. The LLM then
integrates this new information into its context. Depending on the original 
request, it may make further tool calls until it has enough information to 
respond, at which point it generates a coherent,
natural language response for the customer, fulfilling the original request.


### Key Terms


**Function Calling**: The capability of an LLM to identify when to use a
tool outside its built-in functionality and to generate the correct arguments 
for that tool's function based on a natural language prompt.


**Agent Development Kit (ADK)**: A framework designed to simplify the creation,
management, and deployment of LLM-powered agents, including robust mechanisms
for integrating and orchestrating external tools.


**Tool**: A function, API, or module that an LLM-based agent can
invoke to extend its capabilities beyond its core language model functions,
enabling real-world interaction or specialized data processing.


---


## CODE WALKTHROUGH


### Repository Structure


```
.
├── __init__.py           # Initializes the Python package.
├── agent-prompt.txt      # Defines the agent's instructions and persona.
├── agent.py              # Contains the agent's definition and tool implementations.
├── README.md             # Provides an overview and explanation of the demo.
└── requirements.txt      # Lists the Python dependencies for the project.
```


### Step 1: Define Weather Tools


This demo includes three simple Python functions that simulate retrieving
weather information for a given city. These functions act as "tools" that
our agent can call. Each tool takes a `city` as input and returns a string
representing a specific weather condition. Notice the clear function signatures
and docstrings; these are crucial as the ADK provides them to the LLM, which 
uses them to understand what each tool does and how to call it.


```python
def get_temperature(city: str) -> str:
    """Returns the temperature in a city."""
    return f"The temperature in {city} is 25 degrees Celsius."

def get_precipitation(city: str) -> str:
    """Returns the precipitation in a city."""
    return f"The precipitation in {city} is 10%."

def get_wind_speed(city: str) -> str:
    """Returns the wind speed in a city."""
    return f"The wind speed in {city} is 15 km/h."
```


**Key points:**
- Each function has a clear, descriptive name and purpose.
- The docstrings (`"""..."""`) are vital for the LLM to understand when
  and how to use the tool.
- These are synthetic examples; in a real-world scenario, these functions
  would likely make API calls to actual weather services.


### Step 2: Define Agent Instructions


The agent's behavior and conversational style are guided by its
`agent-prompt.txt` file. This prompt sets the persona for the agent (a
weather reporter) and provides guidelines on how it should use its tools
and format its responses. It instructs the agent to be pleasant and to
structure its output as if it were a radio broadcast.


```text
You are an agent that has tools available that can report on the weather.

Customers may ask for specific weather attributes, or they may want the
overall weather for a city. You may call as many tools as necessary to
answer the question.

Your response should be pleasant to read and structured as if it was being
said on the radio or read over the phone.
```


**Key points:**
- The prompt establishes the agent's persona and role.
- It provides explicit instructions on tool usage ("call as many tools as
  necessary").
- It dictates the desired output format and tone ("pleasant to read and
  structured as if it was being said on the radio").
- This file is read by the python code and provided to the LLM as part of 
  the prompt or system instructions.


### Step 3: Create the ADK Agent


The `agent.py` file brings everything together by defining the `root_agent`
using the ADK's `Agent` class. It specifies the agent's `name`, a `description`
of its purpose, the `model` to be used (e.g., "gemini-2.5-flash-lite"),
the `instruction` loaded from `agent-prompt.txt`, and the list of `tools`
(our weather functions) that the agent has at its disposal.


```python
import os
from google.adk.agents import Agent

# Define tool functions (as shown in Step 1)
def get_temperature(city: str) -> str:
    """Returns the temperature in a city."""
    return f"The temperature in {city} is 25 degrees Celsius."

# ... (other tool definitions) ...

# Experiment with the different models to see what works better
model = "gemini-2.5-flash-lite"

# Read the instructions from a file
script_dir = os.path.dirname(os.path.abspath(__file__))

instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")

with open(instruction_file_path, "r") as f:

    instruction = f.read()

# List of tools available to the agent
tools = [
    get_temperature,
    get_precipitation,
    get_wind_speed,
]

# Create the ADK Agent
root_agent = Agent(
    name="weather_tools",
    description="Multiple tools to illustrate different weather conditions to return and how the ADK will use multiple tools to derive an answer",
    model=model,
    instruction=instruction,
    tools=tools,
)
```


**Key points:**
- The `Agent` class from `google.adk.agents` is used to instantiate the agent.
- The `description` helps the ADK and potentially other LLMs understand the
  agent's overall purpose.
- The `instruction` parameter is dynamically loaded, allowing for easy
  modifications to the agent's persona without code changes.
- The `tools` list is where all defined functions are registered with the agent,
  making them available for function calling.


### Complete Example


Here is the full code for `agent.py`, demonstrating how to set up an ADK agent
with multiple tools for weather reporting. This agent can interpret user
requests, decide which weather-related tools to use, execute them, and
then synthesize the results into a friendly, broadcast-style response.


```python
import os
from google.adk.agents import Agent

def get_temperature(city: str) -> str:
    """Returns the temperature in a city."""
    return f"The temperature in {city} is 25 degrees Celsius."

def get_precipitation(city: str) -> str:
    """Returns the precipitation in a city."""
    return f"The precipitation in {city} is 10%."

def get_wind_speed(city: str) -> str:
    """Returns the wind speed in a city."""
    return f"The wind speed in {city} is 15 km/h."

# Experiment with the different models to see what works better
model = "gemini-2.5-flash-lite"

# model = "gemini-2.5-flash"

# model = "gemini-2.5-pro"

# Read the instructions from a file in the same

# directory as this agent.py file.

script_dir = os.path.dirname(os.path.abspath(__file__))

instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")

with open(instruction_file_path, "r") as f:

    instruction = f.read()

tools = [

    get_temperature,

    get_precipitation,

    get_wind_speed,

]

root_agent = Agent(

    name="weather_tools",

    description="Multiple tools to illustrate different weather conditions to return and how the ADK will use multiple tools to derive an answer",

    model=model,

    instruction=instruction,

    tools=tools,

)
```


**How it works:**
1.  The agent receives a user query (e.g., "What's the weather like in London?").
2.  Based on the prompt and tool descriptions, the Gemini model identifies the
    need to call one or more weather tools.
3.  It generates and executes the appropriate tool calls (e.g.,
    `get_temperature("London")`, `get_precipitation("London")`,
    `get_wind_speed("London")`).
4.  The results from these tools are then integrated by the agent, and a
    friendly, comprehensive weather report is generated as a response to the user.


**Expected output:**
```text
User: "What's the weather like in London?"
Agent: "Good morning/afternoon! Here's your weather update for London: The
temperature is 25 degrees Celsius, with 10% precipitation, and a wind speed
of 15 km/h. Have a wonderful day!"
```


---


## Important Details


### Common Misconceptions


**Misconception**: "LLMs can inherently access real-time data or browse the internet."
**Reality**: LLMs are trained on a static dataset, meaning their knowledge is
limited to their last training cut-off. To get real-time data, perform
calculations, or interact with external systems, they *must* be integrated
with external tools.


**Misconception**: "Adding tools makes the LLM itself 'smarter' or more capable of reasoning."
**Reality**: Tools extend the LLM's *functionality* by providing access to
external capabilities. The LLM's core reasoning and language generation
abilities remain the same; it's the *scope* of what it can accomplish that
expands dramatically.


### Best Practices


1.  **Clear and Descriptive Tool Definitions**: Ensure that each tool function
    has a clear name, precise parameters, and a comprehensive docstring.
    The LLM relies heavily on these descriptions to understand the tool's
    purpose and how to correctly invoke it.
2.  **Explicit Agent Instructions**: Provide your agent with detailed and
    unambiguous instructions within its prompt (`agent-prompt.txt`).
    Clearly define its persona, the scenarios in which it should use tools,
    and the desired format and tone for its final responses.
3.  **Modular Tooling**: Design tools to be modular and single-purpose.
    This makes them easier to manage, debug, and reuse, and it helps the
    LLM more accurately select the appropriate tool for a given task.


### Common Errors


**Error**: The agent fails to call a tool when expected, or calls the wrong tool.
- **Causes**: This can happen for several reasons: 
  - Use of a model or model configuration that is not good at tool use.
  - Ambiguous tool descriptions
  - Insufficiently clear agent instructions 
  - Lack of specific examples in the prompt that demonstrate tool usage.
- **Solutions**: Consider and test one or more of the following:
  - Experiment with other models or parameters that encourage more 
    predictable and reasoned behavior
  - Refine the docstrings of your tool functions to be 
    more precise.
  - Review and enhance your `agent-prompt.txt` to provide clearer guidance to
    the agent on when and how to use its tools, potentially including few-shot
    examples.


**Error**: The tool is called correctly, but its output is not correctly used
or parsed by the agent, leading to an irrelevant or malformed response.
- **Cause**: This typically indicates an issue either with the tool's
  implementation (e.g., returning data in an unexpected format) or with the
  agent's ability to integrate the tool's output into its final response.
- **Solution**: Debug the tool function itself to ensure it returns the
  expected data format. Adjust the agent's `agent-prompt.txt` to explicitly
  guide it on how to interpret and incorporate the tool's output into its
  conversational flow.
