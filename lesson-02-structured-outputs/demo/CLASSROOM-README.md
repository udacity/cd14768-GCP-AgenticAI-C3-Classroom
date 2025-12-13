# Module 2: Implementing Structured Outputs with Vertex AI Gemini and Pydantic

This demo illustrates how to take fuzzy, human-like plain text input and convert
it into a structured, machine-readable output using Vertex AI Gemini's
capabilities and Pydantic models.

---

## Overview

### What You'll Learn

This module demonstrates how to develop prompts and leverage Vertex AI Gemini's
capabilities to produce structured JSON outputs, validated with Pydantic models,
for downstream processing. You will learn to enforce specific output schemas for
reliable agent interactions.

Learning objectives:

- Use Pydantic to define desired output schemas for Gemini.
- Configure ADK agents to return structured JSON.
- Understand how to handle ambiguous or invalid inputs with structured error
  reporting.

### Prerequisites

- Basic understanding of Python programming including the Pydantic library.
- Familiarity with Large Language Models (LLMs) concepts.
- Basic familiarity with the Agent Development Kit (ADK).
- Basic understanding of JSON structures.

---

## Understanding the Concept

### The Problem

Large Language Models (LLMs) are excellent at generating free-form text, but
often lack the precision needed for machine-consumable outputs. When building
agents that need to interact with other systems (e.g., executing robot commands,
updating databases, calling APIs), unstructured text responses from an LLM can
be difficult or impossible to parse reliably. This leads to brittle integrations
and unpredictable agent behavior.

### The Solution

The solution involves enforcing a predefined structure for the LLM's output. By
using `Pydantic` models in conjunction with Gemini's structured output
capabilities (specifically, the `output_schema` parameter in ADK), we can ensure
that the LLM's responses adhere to a strict schema. This allows for robust
parsing and downstream processing, making agent interactions deterministic and
reliable, even with fuzzy natural language inputs.

### How It Works

The process of generating structured output typically involves these steps:

**Step 1: Define Output Schema**
Using the Pydantic library, a clear, type-hinted schema (a `BaseModel`) is
defined. This schema specifies all possible fields, their types, whether they
are required or optional, and even acceptable literal values (e.g., "left", "
right").

**Step 2: Instruct the LLM**
Via the `agent-prompt.txt`, the LLM is instructed on its role and the structure
it needs to follow. This includes describing the available commands, their
parameters, and guidelines for handling ambiguous or erroneous inputs by
reporting an error within the structured output itself. This works with the 
structure defined via Pydantic to reinforce the required output to the model.

**Step 3: Agent Configuration**
The ADK `Agent` is configured by providing the Pydantic `BaseModel` as its
`output_schema`. This tells Gemini to strictly adhere to this structure when
generating its response, making it suitable for direct parsing.

**Step 4: User Input**
The customer provides a natural language command or instruction to the agent.

**Step 5: Structured Output Generation**
Gemini, guided by the prompt and the `output_schema`, processes the input and
generates a JSON object that strictly conforms to the defined Pydantic model. If
the input is ambiguous or invalid, the LLM will use the `error` field in the
schema to explain the problem.

**Step 6: Downstream Processing**
Applications can then reliably parse this structured JSON output, knowing its
format is guaranteed, and execute the corresponding actions (e.g., send commands
to a robot, store data in a database).

### Key Terms

**Structured Output**: Generating responses from an LLM that conform to a
predefined, machine-readable format (e.g., JSON, XML) rather than free-form
text. This is crucial for integrating LLMs into automated workflows.

**Pydantic**: A Python library that provides data validation and settings
management using Python type hints. It is widely used to define data schemas and
parse data, ensuring that it meets specific structural and type requirements.

**Schema**: A blueprint or model that defines the structure and types of data.
In the context of LLMs, an output schema ensures that the generated response has
a consistent, predictable format, facilitating reliable parsing and processing.

**Named Entity Recognition (NER)**: The task of identifying and classifying
named entities (e.g., person names, organizations, locations, commands) in
unstructured text into predefined categories. This demo uses a form of NER to
extract robot commands and their parameters.

---

## CODE WALKTHROUGH

### Repository Structure

```
.
├── __init__.py           # Initializes the Python package.
├── agent-prompt.txt      # Defines the agent's instructions and persona for structured output.
├── agent.py              # Contains the agent's definition, including Pydantic models for output schema.
├── README.md             # Provides an overview and explanation of the demo.
└── requirements.txt      # Lists the Python dependencies for the project.
```

### Step 1: Define Pydantic Output Schema

In `agent.py`, we define several Pydantic models and Literal types to create a
strict schema for the robot commands. `DirectionType`, `DistanceUnitsType`, and
`CommandType` use `typing.Literal` to restrict values to a predefined set.

We define a `RobotCommand` model that represents a single action, including
attributes like `command`, `direction`, `distance`, `object`, and `error`. 

Crucially, we then define a `RobotCommands` model that contains a list of these
commands. This allows the agent to return multiple instructions in a single
response.

```python
import os
from google.adk.agents import Agent
from pydantic import BaseModel, Field
from typing import Literal, Optional

DirectionType = Literal["left", "right"]
DistanceUnitsType = Literal["feet", "yards", "meters"]
CommandType = Literal["turn", "walk", "dance", "get", "error"]


class Distance(BaseModel):
  num: float = Field(..., description="The numerical value of the distance.")
  units: DistanceUnitsType = Field(...,
                                   description="The units of measurement for the distance.")


class RobotCommand(BaseModel):
  command: CommandType = Field(..., description="The command for the robot.")
  direction: Optional[DirectionType] = Field(None,
                                             description="The direction for the robot.")
  distance: Optional[Distance] = Field(None,
                                       description="The distance for the robot to move.")
  object: Optional[str] = Field(None,
                                description="The object the robot should interact with.")
  error: Optional[str] = Field(None,
                               description="If the instruction was invalid or ambiguous, explain the problem.")


class RobotCommands(BaseModel):
  commands: list[RobotCommand] = Field(..., description="A list of robot commands.")
```

**Key points:**

- **Strict Type Enforcement**: `Pydantic` models ensure the output adheres to
  defined types and structures.
- **List Support**: The `RobotCommands` model allows for a list of `RobotCommand`
  objects, enabling the agent to handle multi-step instructions.
- **`Literal` Types**: Used to restrict string values to a predefined set,
  improving data quality.
- **Descriptive Fields**: `Field` descriptions provide essential context to the
  LLM for accurate parsing.
- **Error Handling**: It is important we define a way for it to report an error in the existing
  structure, otherwise it may hallucinate a response to fit into the reply if
  there is actually a problem.

### Step 2: Define Agent Instructions for Structured Output

The `agent-prompt.txt` file provides comprehensive instructions to the Gemini
model. It details each command the robot can perform and specific guidelines for
handling ambiguity. Note the instruction: "You can return one or more commands
in the response."

```text
You are a warehouse robot controller. Workers give you natural language instructions which you convert to structured
commands for the robot's control system.

You can perform the following commands:
*   **turn**: Change the robot's orientation. Must be combined with a `direction` (left/right)
*   **walk**: Move the robot. Can be combined with an optional `direction` (left/right) and a `distance` (e.g., 5 feet,
    10 yards) or an `object` to move towards
*   **dance**: Make the robot dance.
*   **get**: Retrieve an `object`.
*   **error**: Report an error in the instruction.

For each command, identify the primary action and any relevant optional attributes:
*   **command**: The main action (turn, walk, dance, get).
*   **direction**: (Optional) The direction for 'turn' or 'walk' commands (left, right).
*   **distance**: (Optional) For 'walk' commands, specify the numerical value (`num`) and units (feet, yards, meters).
*   **object**: (Optional) For 'get' commands, specify the object to retrieve.
*   **error**: (Optional) If there is a problem with the instruction, report it as an error with an explanation

If an attribute in the returned object would be null, you should omit it.

You can return one or more commands in the response.

Additional guidelines:
*   The first message you get, if it is not a command that you can execute, reply with the following message:
     "Hello. I'm the warehouse robot controller. Try commands like 'turn left', 'walk 10 feet', and I'll convert them
     to structured format."
*   If you are not sure what command was issued, report this as an error and ask for clarification
*   If the command has invalid values, report this as an error and ask for clarification
*   If the destination for "walk" is ambiguous (eg - "go somewhere" or "go over there") ask for clarification
*   If the object to "get" is ambiguous (eg - "something") ask for clarification
*   If there are other ambiguous instructions, ask for clarification
```

**Key points:**

- **Clear Role Definition**: The prompt establishes the agent's role as a
  translator.
- **Detailed Command Descriptions**: Each robot command and its parameters are
  clearly outlined.
- **Multi-Command Support**: Explicitly telling the model it can return one or
  more commands.
- **Error Handling**: Specific directives for reporting errors or ambiguities.

### Step 3: Create the ADK Agent with Output Schema

In `agent.py`, the `root_agent` is instantiated using the ADK's `Agent` class.
The `output_schema` parameter is set to our `RobotCommands` Pydantic model.
This tells Gemini that the final output must be an object containing a list of
commands.

```python
import os
from google.adk.agents import Agent
from pydantic import BaseModel, Field
from typing import Literal, Optional

# ... (Pydantic model definitions) ...

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
  instruction = f.read()

model = "gemini-2.5-flash"

root_agent = Agent(
  name="robot_commands",
  description="Warehouse robot controller - converts worker instructions to structured commands.",
  instruction=instruction,
  model=model,
  output_schema=RobotCommands,  # See what happens if we remove this line
)
```

**Key points:**

- **`output_schema` Parameter**: Enforces the `RobotCommands` structure.
- **Centralized Configuration**: Connects the model, instructions, and schema.

### Complete Example

Here is the full `agent.py` file, demonstrating a complete ADK agent configured
to produce structured output representing a list of robot commands.

```python
import os
from google.adk.agents import Agent
from pydantic import BaseModel, Field
from typing import Literal, Optional

DirectionType = Literal["left", "right"]
DistanceUnitsType = Literal["feet", "yards", "meters"]
CommandType = Literal["turn", "walk", "dance", "get", "error"]


class Distance(BaseModel):
  num: float = Field(..., description="The numerical value of the distance.")
  units: DistanceUnitsType = Field(...,
                                   description="The units of measurement for the distance.")


class RobotCommand(BaseModel):
  command: CommandType = Field(..., description="The command for the robot.")
  direction: Optional[DirectionType] = Field(None,
                                             description="The direction for the robot.")
  distance: Optional[Distance] = Field(None,
                                       description="The distance for the robot to move.")
  object: Optional[str] = Field(None,
                                description="The object the robot should interact with.")
  error: Optional[str] = Field(None,
                               description="If the instruction was invalid or ambiguous, explain the problem.")


class RobotCommands(BaseModel):
  commands: list[RobotCommand] = Field(..., description="A list of robot commands.")


script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
  instruction = f.read()

model = "gemini-2.5-flash"

root_agent = Agent(
  name="robot_commands",
  description="Warehouse robot controller - converts worker instructions to structured commands.",
  instruction=instruction,
  model=model,
  output_schema=RobotCommands,  # See what happens if we remove this line
)
```

**How it works:**

1. The agent receives a natural language instruction (e.g., "walk 10 feet to the
   left then turn right").
2. Gemini parses the instruction and creates a list of `RobotCommand` objects.
3. These are wrapped in a `RobotCommands` object.
4. The ADK receives this structured JSON.

**Expected output:**

```json
Human: "walk 10 feet to the left"
Agent: {
  "commands": [
    {
      "command": "walk",
      "direction": "left",
      "distance": {
        "num": 10.0,
        "units": "feet"
      }
    }
  ]
}
```

```json
Human: "dance then turn right"
Agent: {
  "commands": [
    {
      "command": "dance"
    },
    {
      "command": "turn",
      "direction": "right"
    }
  ]
}
```

```json
Human: "get the red ball"
Agent: {
  "commands": [
    {
      "command": "get",
      "object": "red ball"
    }
  ]
}
```

```json
Human: "go somewhere"
Agent: {
  "commands": [
    {
      "command": "error",
      "error": "The destination for \"walk\" is ambiguous. Please specify where to go."
    }
  ]
}
```

---

## Important Details

### Common Misconceptions

**Misconception**: "Gemini inherently understands and produces structured JSON
without explicit guidance."
**Reality**: While Gemini can be prompted to *try* to produce JSON, providing a
strict `output_schema` (especially with Pydantic) through the ADK guarantees
adherence to a specific structure and data types. Without it, the output might
be close to JSON but could contain subtle errors that break parsing. Also 
remember that Large Language Models do not "understand" anything, but rather 
they follow patterns. Providing a Pydantic schema helps define the expected 
pattern.

**Misconception**: "Pydantic models are just for Python developers; the LLM
doesn't care about them."
**Reality**: The ADK converts the Pydantic model into an OpenAPI schema (or
similar format) that is then passed to Gemini. This schema is critical for the
LLM to understand the exact structure, types, and constraints required for its
output. The descriptions within the `Field` definitions are particularly
important for guiding the LLM. The Pydantic model is just a standard, 
well-defined, way to specify this schema. 

### Best Practices

1. **Define Comprehensive Pydantic Schemas**: Create detailed Pydantic
   `BaseModel` classes with precise type hints (`Literal` for enums), `Field`
   descriptions, and validation rules. The more explicit your schema, the better
   Gemini will be at conforming to it. Similarly, the clearer the 
   description, the better chance Gemini will be able to populate the field 
   correctly.
2. **Explicit Prompting for Structure**: Your `agent-prompt.txt` should clearly
   articulate the expected output structure and the meaning of each field.
   Provide examples if necessary. Also, instruct the LLM on how to handle edge
   cases like ambiguous inputs (e.g., by using an `error` field in the output).
3. **Test with Edge Cases**: Always test your structured output agent with a
   variety of inputs, including valid, ambiguous, and invalid commands, to
   ensure it correctly maps to the schema or reports errors gracefully.

### Common Errors

**Error**: The output is not valid JSON, or fields are missing/incorrectly
typed.

- **Cause**: This often happens if the `output_schema` is not correctly
  configured in the `Agent` instantiation, or if the `agent-prompt.txt` is not
  clear enough in describing the expected structure. Sometimes, less capable
  models might also struggle more with strict schema adherence.
- **Solution**: Double-check that `output_schema` is set to your Pydantic
  `BaseModel` in `agent.py`. Refine your `agent-prompt.txt` to include more
  explicit instructions and examples. Consider experimenting with different
  Gemini models if the issue persists.

**Error**: Ambiguous inputs lead to incorrect structured outputs or generic text
responses instead of structured errors.

- **Cause**: The `agent-prompt.txt` may not have sufficient instructions for
  handling ambiguity, or the `RobotCommands` schema might lack a dedicated
  `error` field.
- **Solution**: Add clear instructions to `agent-prompt.txt` on how to use the
  `error` field for ambiguous inputs. Ensure your Pydantic schema includes an
  `error` field (as in `RobotCommands`) that the LLM can populate with an
  explanation.
