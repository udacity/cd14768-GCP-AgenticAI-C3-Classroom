# Module 2 Exercise: Information Summarizer

This exercise guides you through building an ADK agent that summarizes customer
service feedback into a structured, machine-readable format using Pydantic
models and Vertex AI Gemini's structured output capabilities.

---

## Overview

### What You'll Learn

In this exercise, you will develop an agent to process free-form customer
feedback and extract key information into a predefined Pydantic schema. This
will reinforce your understanding of how to leverage structured outputs for
reliable data extraction and downstream processing, particularly for tasks like
sentiment analysis or database ingestion.

Learning objectives:

- Design a Pydantic model suitable for summarizing specific types of textual
  data.
- Configure an ADK agent to use this Pydantic model as its `output_schema`.
- Craft a clear and effective `agent-prompt.txt` to guide the LLM in extracting
  and structuring information.

### Prerequisites

- Basic understanding of Python programming, including the Pydantic library.
- Familiarity with Large Language Models (LLMs) concepts.
- Basic familiarity with the Agent Development Kit (ADK).
- Basic understanding of JSON structures.

---

## Understanding the Concept

### The Problem

Customer feedback often comes in unstructured, free-form text. While humans can
easily understand the nuances, automating the analysis of this feedback (e.g.,
categorizing by type, extracting key issues, tracking trends) is challenging.
Without a structured format, integrating feedback into analytics dashboards or
CRM systems requires manual effort or complex, error-prone parsing scripts.

### The Solution

The solution is to use an LLM such as Vertex AI Gemini with a Pydantic
`output_schema`, to act as an intelligent parser. By defining a Pydantic model
for a `FeedbackSummary`, we instruct the LLM to extract relevant entities (
customer name, feedback date, feedback type, summary) from the raw text and
present them in a consistent JSON format. This structured output can then be
easily consumed by other systems for automated processing, analysis, and
reporting.

### How It Works

1. **Define Feedback Schema**: A `Pydantic` `BaseModel`, `FeedbackSummary`, is
   created to specify the exact structure, types, and constraints for the
   summarized feedback. This includes optional fields for `customer_name` and
   `feedback_date`, and a `Literal` type for `feedback_type` (`complaint`,
   `suggestion`, `praise`).
2. **Instruction to LLM**: The `agent-prompt.txt` guides the LLM on its role as
   a customer service assistant and clearly outlines the pieces of information
   it needs to extract and the `FeedbackType` categories.
3. **Agent Configuration**: The ADK `Agent` is configured with the
   `FeedbackSummary` Pydantic model as its `output_schema`, ensuring all
   responses from Gemini strictly adhere to this format.
4. **Customer Feedback Input**: The agent receives a natural language paragraph
   of customer feedback.
5. **Structured Summary Generation**: Gemini processes the feedback, extracts
   the required information, and generates a `FeedbackSummary` JSON object.
   Optional fields are omitted if no relevant information is found.
6. **Automated Processing**: The structured JSON output can be directly fed into
   analytics tools, databases, or other applications for further automated
   sentiment analysis, trend tracking, or response generation.

### Key Terms

**Structured Data Extraction**: The process of programmatically identifying and
pulling specific pieces of information from unstructured text and organizing
them into a predefined data model.

**Sentiment Analysis**: The process of determining the emotional tone behind a
piece of text (e.g., positive, negative, neutral). Structured feedback summaries
can greatly aid in automated sentiment analysis.

**Pydantic `date` type**: A Pydantic field that expects and validates a `date`
object (YYYY-MM-DD format), ensuring temporal data is correctly extracted and
formatted.

---

## EXERCISE INSTRUCTIONS

### Your Task

Your task is to complete the ADK agent in `agent.py` so that it can accurately
summarize customer service feedback. You will need to:

1. **Define the `FeedbackSummary` Pydantic model**: This model should capture
   the `customer_name` (optional string), `feedback_date` (optional date),
   `feedback_type` (restricted to "complaint", "suggestion", or "praise"), and a
   `summary` (string).
2. **Implement the `agent-prompt.txt`**: Write clear instructions that guide the
   LLM to identify and extract the specified information from customer feedback,
   ensuring it uses the correct `feedback_type` and omits optional null
   attributes.
3. **Configure the `root_agent`**: Ensure the `Agent` is properly instantiated
   with the `FeedbackSummary` model as its `output_schema`.

### Requirements

Your implementation must:

1. Use `pydantic.BaseModel` to define the output schema.
2. Utilize `typing.Literal` for the `feedback_type` field.
3. Correctly extract optional `customer_name` and `feedback_date` when present.
4. Categorize `feedback_type` as either "complaint", "suggestion", or "praise".
5. Generate a concise `summary` of the feedback content.
6. Omit any optional fields if their values are `null` or not found in the
   input.
7. The agent should be able to handle various feedback scenarios, including
   those with missing optional details.

### Repository Structure

```
.
├── __init__.py           # Initializes the Python package.
├── agent-prompt.txt      # (Your task) Define agent instructions for structured output.
├── agent.py              # (Your task) Define Pydantic model and configure agent.
├── README.md             # Provides environment setup information.
└── requirements.txt      # Lists the Python dependencies for the project.
```

Make sure you copy `.env-sample` to `.env` and edit it to add the Google Cloud
project you are working with.

Remember that you should **never** check-in your .env file to git.

### Starter Code

`agent.py`

```python
import os
from datetime import date
from google.adk.agents import Agent
from pydantic import BaseModel, Field
from typing import Literal, Optional

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
  instruction = f.read()

# TODO: Define FeedbackType using Literal for complaint, suggestion, praise
FeedbackType = Literal["TODO", "TODO", "TODO"]


# TODO: Define FeedbackSummary Pydantic BaseModel
# It should include:
# - customer_name: Optional[str]
# - feedback_date: Optional[date]
# - feedback_type: FeedbackType (required)
# - summary: str (required)
class FeedbackSummary(BaseModel):
  pass  # TODO: Implement fields


model = "gemini-2.5-flash"

# TODO: Configure the root_agent with the correct output_schema
root_agent = Agent(
  name="information_summarizer",
  description="A tool for summarizing customer service feedback.",
  instruction=instruction,
  model=model,
  # output_schema=FeedbackSummary # TODO: Uncomment and use your Pydantic model here
)
```

`agent-prompt.txt`

```text
TODO
```

### Expected Behavior

The completed agent should be able to take various customer feedback inputs and
output a JSON object conforming to the `FeedbackSummary` schema.

**Running the agent:**

You will run the agent using the `adk web` tool. This tool provides a web chat
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

```text
Human: "I am writing to express my extreme dissatisfaction with the recent service I received on October 26, 2023. The technician was late, unhelpful, and did not resolve my issue. My name is Alice Smith."
Agent: {
  "customer_name": "Alice Smith",
  "feedback_date": "2023-10-26",
  "feedback_type": "complaint",
  "summary": "Customer Alice Smith experienced poor service on 2023-10-26; technician was late, unhelpful, and did not resolve the issue."
}
```

```text
Human: "Just wanted to say that the new interface is fantastic! Great work team."
Agent: {
  "feedback_type": "praise",
  "summary": "Customer praises the new fantastic interface."
}
```

```text
Human: "I think it would be great if you could add a dark mode option to your mobile app. It would really help with eye strain at night."
Agent: {
  "feedback_type": "suggestion",
  "summary": "Customer suggests adding a dark mode option to the mobile app to reduce eye strain at night."
}
```

### Implementation Hints

1. Pay close attention to the `description` parameters in `pydantic.Field` to
   accurately guide the LLM.
2. Remember that `Optional` fields will be omitted from the output, or set 
   to Null, if the LLM determines they are not present in the input.
3. Ensure your `agent-prompt.txt` is unambiguous regarding the categorization of
   feedback types.

---

## Important Details

### Common Misconceptions

**Misconception**: "The LLM will automatically know how to summarize and
categorize feedback."
**Reality**: While LLMs are good at understanding text, they need explicit
guidance through the `agent-prompt.txt` and `output_schema` to reliably extract
and categorize specific information into a structured format. Without clear
instructions, the output might be inconsistent or miss crucial details. LLMs 
that provide structured output are specifically tuned to follow the output 
formatting that is provided.

**Misconception**: "All fields in the Pydantic model must always be present in
the output JSON."
**Reality**: By marking fields as `Optional` in Pydantic (`Optional[str]`,
`Optional[date]`), you tell the schema that these fields may or may not be
present. The LLM will only include them in the output if it can confidently
extract that information from the input, otherwise, they will be omitted or 
set to Null, making the output flexible.

### Best Practices

1. **Clear Pydantic Field Descriptions**: Use descriptive `description`
   arguments in `pydantic.Field` for every field in your `BaseModel`. This
   metadata is passed to the LLM and significantly improves its ability to
   correctly populate the structured output.
2. **Iterative Prompt Refinement**: Start with a basic `agent-prompt.txt` and
   gradually refine it. Test with diverse examples of customer feedback to
   identify cases where the LLM struggles with extraction or categorization,
   then adjust the prompt accordingly.
3. **Leverage `datetime.date` for Dates**: When extracting dates, use the
   `datetime.date` type hint in your Pydantic model. This encourages the LLM to
   format dates consistently (e.g., YYYY-MM-DD), simplifying downstream
   processing.

### Common Errors

**Error**: The agent fails to correctly identify `feedback_type` or
miscategorizes it.

- **Cause**: The `agent-prompt.txt` might not clearly define the criteria for
  each `feedback_type` (complaint, suggestion, praise), or the training data for
  the model might influence its categorization.
- **Solution**: Refine your `agent-prompt.txt` to provide more explicit examples
  or rules for distinguishing between feedback types. Consider including
  few-shot examples directly in the prompt if categorization remains a
  challenge.

**Error**: Optional fields like `customer_name` or `feedback_date` are not
extracted even when present in the input.

- **Cause**: The LLM might not be prioritizing the extraction of these optional
  fields, or the prompt might not sufficiently emphasize their importance.
- **Solution**: Ensure your `agent-prompt.txt` highlights the importance of
  extracting `customer_name` and `feedback_date` when available. Also, verify
  that the `description` in the `pydantic.Field` for these fields is clear and
  guides the LLM to look for them.