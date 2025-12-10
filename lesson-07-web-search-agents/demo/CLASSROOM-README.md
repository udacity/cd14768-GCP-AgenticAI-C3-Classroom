# Module 7: Implementing Web Search Agents with ADK and Grounding with Google Search Tool

This demo illustrates how to enhance an agent's knowledge by grounding its
responses in real-time web search results using the Google Search tool
integrated into the ADK.

---

## Overview

### What You'll Learn

You will learn how to enable "Grounding with Google Search" for an ADK agent.
This allows the model to search the web when its internal knowledge is
insufficient or outdated, providing accurate, up-to-date answers with citations.

Learning objectives:

- Understand the concept of "Grounding" in LLMs.
- Integrate the `google_search` tool into an ADK agent.
- Observe how the model automatically decides when to search the web.
- Interpret the grounded responses, including citations and search metadata.

### Prerequisites

- Basic understanding of Python.
- Familiarity with ADK agent structure.
- A Google Cloud Project with the Vertex AI API enabled.

---

## Understanding the Concept

### The Problem

LLMs are trained on vast datasets, but that data has a cut-off date. They don't
know about events that happened today, the current weather, or real-time stock
prices. Furthermore, they can "hallucinate" facts when unsure.

### The Solution

**Grounding** is the process of connecting the model's generation to verifiable
sources of information. By integrating the **Google Search Tool**, we give the
model permission to query Google Search. When the user asks a question about
current events or specific facts, the model:

1. Recognizes the need for external information.
2. Generates a search query.
3. Retrieves results from Google Search.
4. Synthesizes an answer based *only* on those results.
5. Provides citations to the sources.

### How It Works

1. **Tool Registration**: We import `google_search` from `google.adk.tools` and
   add it to the agent's tool list.
2. **Automatic Invocation**: Unlike custom tools where we write the logic,
   `google_search` is a native integration. The Gemini model handles the query
   generation and result parsing automatically.
3. **Response Generation**: The ADK receives the grounded response, which
   includes not just the text but also metadata about the sources (grounding
   chunks), which can be displayed to the user.

### Key Terms

**Grounding**: Anchoring model outputs to verifiable sources (like Google Search
or a private document corpus) to reduce hallucinations and improve accuracy.

**Google Search Tool**: A built-in tool in Vertex AI that allows Gemini models
to perform web searches and incorporate the results into their responses.

**Citations**: References to the source URLs that support specific statements in
the model's response.

---

## CODE WALKTHROUGH

### Repository Structure

```
.
├── __init__.py           # Package initialization.
├── agent-prompt.txt      # Minimal agent instructions.
├── agent.py              # Agent configuration with google_search.
├── README.md             # Overview.
└── requirements.txt      # Dependencies.
```

### Step 1: The Agent Configuration (`agent.py`)

The code is remarkably simple because the complexity is handled by the platform.

```python
import os
from google.adk.agents import Agent
# Import the built-in search tool
from google.adk.tools import google_search

# ... load instructions ...

model = "gemini-2.5-flash"

# Register the tool
tools = [
  google_search
]

root_agent = Agent(
  name="web_search_agent",
  description="An agent that can search the web.",
  instruction=instruction,
  model=model,
  tools=tools,
)
```

**Key Point**: We don't need to write a `def search(query):` function.
`google_search` is a special object that tells the ADK to enable the Grounding
feature in Vertex AI.

### Step 2: The Prompt (`agent-prompt.txt`)

The prompt can be very simple.

```text
You are a helpful assistant that answers questions.
```

The model doesn't need explicit instructions on *how* to search (e.g., "If you
don't know, search Google"). It has been trained to use the provided search tool
whenever appropriate.

---

## Important Details

### Common Misconceptions

**Misconception**: "I need to parse the HTML of search results."
**Reality**: Grounding with Google Search handles the retrieval and parsing. The
model receives a clean summary of relevant snippets, not raw HTML.

**Misconception**: "The model searches for everything."
**Reality**: The model is efficient. If you ask "What is 2+2?", it relies on its
internal knowledge. If you ask "Who won the Super Bowl yesterday?", it triggers
a search.

### Best Practices

- **Enable it for Knowledge Agents**: If your agent needs to answer general
  knowledge questions, always enable grounding to prevent hallucinations.
- **Review Citations**: When building a UI, always display the citations
  returned by the ADK. This builds trust with the user.

### Common Errors

**Error**: `403 Permission Denied` or Grounding not enabled.

- **Cause**: The Google Search Grounding API might not be enabled in your Google
  Cloud Project, or your project isn't allowlisted for this feature (if it's in
  preview).
- **Solution**: Check the Vertex AI section of the Google Cloud Console to
  ensure Grounding is enabled.
