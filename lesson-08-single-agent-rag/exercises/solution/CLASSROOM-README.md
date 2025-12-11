# Module 8: Implementing Single-Agent RAG with ADK and Vertex AI Search/RAG Engine

This exercise guides you through building a Retrieval-Augmented Generation (RAG)
agent. Your agent uses Vertex AI Search to index custom documents about
superheroes and supervillains that you and Gemini create, and then retrieve 
relevant information to ground its answers to user questions.

---

## Overview

### What You'll Learn

You will learn the complete workflow for setting up a RAG system on Google
Cloud and connecting it to an ADK agent. This involves generating custom
unstructured data, indexing it in Vertex AI Search, and writing code to query
it.

Learning objectives:

- Generate custom documents using Gemini or Gemini CLI.
- Configure Google Cloud Storage and Vertex AI Search for RAG.
- Implement a search tool using the `google.cloud.discoveryengine` library.
- Connect the search tool to an ADK agent for grounded responses.

### Prerequisites

- A Google Cloud Project with billing enabled.
- Basic understanding of Python and RAG concepts.
- `gcloud` CLI installed and authenticated.

---

## Understanding the Concept

### The Problem

Large Language Models (LLMs) have a knowledge cutoff and cannot access your
private or domain-specific data. Fine-tuning an LLM is often expensive and
time-consuming. If you want an agent to answer questions about specific, newly
created information (like details about fictional superheroes), you need a way
to feed that information to the model dynamically and reliably.

### The Solution

**RAG (Retrieval-Augmented Generation)** is the industry standard solution.

1. **Ingestion**: You create and upload custom documents to Google Cloud
   Storage.
2. **Indexing**: Vertex AI Search processes these documents into a "Data Store",
   chunking them into smaller pieces and creating a semantically searchable
   index.
3. **Retrieval**: When a user asks a question, your code makes an API call to
   the Discovery Engine API to search for relevant chunks that semantically
   match the question.
4. **Generation**: The retrieved chunks are passed to the LLM (Gemini), which
   synthesizes an answer based *only* on that retrieved context, ensuring the
   answer is grounded in your specific data.

### How It Works

1. **Document Generation**: You use Gemini or Gemini CLI to generate
   creative content about superheroes, supervillains, and their TV series.
2. **Setup**: You upload these documents to Google Cloud Storage (GCS) and 
   create a "Search App" and "Data Store" in Vertex AI Search linked to 
   this bucket.
3. **Tool Execution**: You implement the `datastore_search_tool` in
   `datastore.py` which uses the Google Cloud Discovery Engine client library to
   query this Data Store.
4. **Search Configuration**: Your search request is configured to return
   "chunks" (snippets of text) rather than full documents, and use features
   like "Query Expansion" to find relevant results.
5. **Result**: The tool returns a list of text chunks. The ADK passes these
   to the Gemini model, which uses them to answer the user's question, providing
   grounded responses about your superhero universe.

### Key Terms

**Vertex AI Search (Discovery Engine)**: Google's platform for building search
and chat applications using RAG. It handles the complex infrastructure of vector
databases and indexing.

**Unstructured Data**: Data that doesn't have a pre-defined data model, like PDF
files or plain text documents.

**Chunking**: The process of breaking large documents into smaller, manageable
pieces (chunks) for better retrieval and context window management.

---

## Code Walkthrough

### Repository Structure

```
.
├── __init__.py           # Package initialization.
├── agent-prompt.txt      # Agent instructions.
├── agent.py              # Agent configuration.
├── datastore.py          # The RAG retrieval logic.
├── requirements.txt      # Dependencies.
```

### Step 1: The Search Logic (`datastore.py`)

This file contains the code to talk to Vertex AI Agent Builder.

```python
from google.cloud import discoveryengine_v1 as discoveryengine


def search(project_id, location, engine_id, search_query):
  # ... client setup ...
  client = discoveryengine.SearchServiceClient(...)

  # Define the "Serving Config" resource path
  serving_config = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/servingConfigs/default_config"

  # Configure the search request
  request = {
    "serving_config": serving_config,
    "query": search_query,
    "page_size": 10,
    # CHUNKS mode returns snippets, not full docs
    "content_search_spec": {
      "search_result_mode": discoveryengine.SearchRequest.ContentSearchSpec.SearchResultMode.CHUNKS
    },
    # Query Expansion helps matching synonyms
    "query_expansion_spec": {
      "condition": discoveryengine.SearchRequest.QueryExpansionSpec.Condition.AUTO,
    },
  }

  # Execute search
  page_result = client.search(request)

  # Extract just the text content from the chunks
  results = []
  for result in page_result:
    if result.chunk and result.chunk.content:
      results.append(result.chunk.content)

  return results
```

**Key Details**:

- **`serving_config`**: The resource name or path for the specific 
  configuration of your search engine. The default is usually fine. 
- **`CHUNKS` mode**: Critical for RAG. We don't want the whole PDF; we want the
  relevant portions of docs.
- **`query_expansion_spec`**: A powerful feature of Vertex AI Search that
  broadens the search terms automatically.

**Important Note**:

There are many other configuration options available. These are good for 
most uses, but you may want to read through the documentation URLs that are 
included to see what other options are available for other use cases.

### Step 2: The Tool Wrapper (`datastore.py`)

The `datastore_search_tool` wraps the complex `search` function into a simple
interface for the agent.

```python
def datastore_search_tool(search_query: str):
  """Searches store information..."""
  return search(
    project_id=os.environ.get("DATASTORE_PROJECT_ID"),
    # ... other env vars ...
    search_query=search_query,
  )
```

### Step 3: The Agent (`agent.py`)

The agent just sees a tool.

```python
root_agent = Agent(
  name="superhero_faq_agent",
  # ...
  tools=[datastore_search_tool],
)
```

---

## Important Details

### Best Practices

- **Metadata**: In a real app, you might also return the `document.id` or `link`
  from the search result so the UI can show citations ("Source: Page 5 of Q3
  Report").
- **Hybrid Search**: Vertex AI Search supports "Hybrid Search" (keyword +
  vector). This `demo` uses the default behavior, which is often a robust mix.
- **Request Configuration**: There are many other options available in the 
  request configuration, including filtering on specific metadata. See the 
  documentation URLs for more details.

### Common Errors

**Error**: `404 Not Found` or `Resource not found`.

- **Cause**: The `DATASTORE_ENGINE_ID` or `DATASTORE_LOCATION` is incorrect. The
  IDs can be tricky to find in the console; check the URL or the "Integration"
  tab.
- **Solution**: Double-check the `.env` values against the console.

**Error**: Empty results.

- **Cause**: The documents haven't finished indexing yet.
- **Solution**: Check the Data Store status in the console. It must say "
  Imported" or "Active".

**Error**: `403 Permission Denied`.

- **Cause**: ADC not set up or user lacks permission on the project.
- **Solution**: Run `gcloud auth application-default login` and check IAM
  roles (Discovery Engine Editor/Viewer).
