# Module 2 Exercise Solution: Information Summarizer

This is the solution for the Information Summarizer exercise. It demonstrates a
fully implemented ADK agent that uses Pydantic models to extract structured data
from customer feedback.

---

## Overview

### What You'll Learn

This solution illustrates the correct implementation of a Pydantic `BaseModel`
and its integration with an ADK agent to achieve reliable structured output.

Learning objectives:

- Correctly defining Pydantic models with `Literal` types and `Optional` fields.
- Writing effective prompts that align with the defined schema.
- configuring the ADK agent to enforce the output schema.

### Prerequisites

- Basic understanding of Python and Pydantic.
- Familiarity with the ADK `Agent` class.

---

## Understanding the Concept

### The Problem

Extracting specific data points like names, dates, and sentiment categories from
free-text customer feedback is error-prone without a structured approach.

### The Solution

This solution uses a `FeedbackSummary` Pydantic model to define the expected
structure. The Gemini model is then instructed via the `agent-prompt.txt` to
extract this information, and the ADK ensures the output matches the Pydantic
schema.

### How It Works

1. **Schema Definition**: We define `FeedbackSummary` to capture
   `customer_name`, `feedback_date`, `feedback_type`, and `summary`.
2. **Prompting**: The prompt acts as a guide, telling the LLM what to look for
   and how to categorize the feedback.
3. **Enforcement**: By passing `output_schema=FeedbackSummary` to the agent, we
   force the LLM's response to be a valid JSON object conforming to our model.

---

## CODE WALKTHROUGH

### Repository Structure

```
.
├── __init__.py           # Initializes the Python package.
├── agent-prompt.txt      # The completed instructions for the agent.
├── agent.py              # The completed agent with Pydantic model and configuration.
├── README.md             # Environment setup information.
└── requirements.txt      # Python dependencies.
```

### Step 1: Defined Pydantic Model

In `agent.py`, we defined the `FeedbackSummary` model. Note the use of `Literal`
for `FeedbackType` to restrict values, and `Optional` for fields that might not
exist in the input.

```python
FeedbackType = Literal["complaint", "suggestion", "praise"]


class FeedbackSummary(BaseModel):
  customer_name: Optional[str] = Field(None,
                                       description="The name of the customer providing feedback.")
  feedback_date: Optional[date] = Field(None,
                                        description="The date the feedback was provided.")
  feedback_type: FeedbackType = Field(..., description="The type of feedback.")
  summary: str = Field(..., description="A summary of the feedback.")
```

**Key points:**

- **Strict Typing**: `FeedbackType` ensures we only get valid categories.
- **Descriptive Fields**: The `description` argument helps the LLM understand
  the purpose of each field.

### Step 2: Agent Instructions

The `agent-prompt.txt` was populated with clear instructions on what to extract
and how to handle missing information.

```text
You are a customer service assistant. Your task is to read customer feedback and summarize it in a structured format.

You should identify the following information and provide a structured reply:
* Customer's name (Optional)
* Date of the feedback (Optional)
* Type of feedback ("complaint", "suggestion", or "praise")
* A concise summary of the feedback content.

If an optional attribute in the returned object would be null, you should omit it.
```

### Step 3: Agent Configuration

Finally, the `root_agent` was configured with the schema.

```python
root_agent = Agent(
  name="information_summarizer",
  description="A tool for summarizing customer service feedback.",
  instruction=instruction,
  model=model,
  output_schema=FeedbackSummary
)
```

### Complete Example

The files in this directory represent the complete working solution. You can run
`adk web` from the parent directory to test this agent
against the examples provided in the exercise instructions.

**Expected behavior:**
When given feedback like "Great job!", the agent returns a JSON object with
`feedback_type: "praise"` and a summary, omitting the optional name and date
fields.

---

## Important Details

### Best Practices

- **Schema as Truth**: The Pydantic model is the single source of truth for your
  data structure.
- **Prompt Alignment**: Ensure your prompt instructions align with your schema
  definitions (e.g., using the same category names).
- **Handling Nulls**: Explicitly instructing the LLM to omit null fields keeps
  the output clean and reduces payload size.
