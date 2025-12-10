# Module 8: Implementing Single-Agent RAG with ADK and Vertex AI Search/RAG Engine

This demo illustrates how to build a Retrieval-Augmented Generation (RAG) agent.
The agent uses Vertex AI Agent Builder (formerly Gen App Builder) to index
unstructured documents (like financial reports) and retrieving relevant chunks
to ground its answers.

---

## Overview

### What You'll Learn

You will learn the complete workflow for setting up a RAG system on Google Cloud
and connecting it to an ADK agent. This involves processing unstructured data,
indexing it, and querying it via code.

Learning objectives:

- Configure Google Cloud Storage and Vertex AI Agent Builder for RAG.
- Implement a search tool using the `google.cloud.discoveryengine` library.
- Understand the `search` function configuration (content specs, query
  expansion).
- Connect the search tool to an ADK agent for grounded responses.

### Prerequisites

- A Google Cloud Project with billing enabled.
- Basic understanding of Python and RAG concepts.
- `gcloud` CLI installed and authenticated.

---

## Understanding the Concept

### The Problem

LLMs have a knowledge cutoff and can't access your private data. Fine-tuning is
expensive and slow. If you want an agent to answer questions about your
company's specific financial reports (10-Ks, 10-Qs), you need a way to feed that
information to the model dynamically.

### The Solution

**RAG (Retrieval-Augmented Generation)** is the industry standard solution.

1. **Ingestion**: You upload documents to Google Cloud Storage.
2. **Indexing**: Vertex AI Agent Builder processes these documents into a 
   "Data Store", chunking them into smaller pieces and creating a semantically 
   searchable index. 
3. **Retrieval**: When a user asks a question, your code makes an API call 
   to the Agent Builder Discovery Engine API to search for relevant chunks that 
   semantically match the question.
4. **Generation**: The chunks are passed to the LLM, which synthesizes an answer
   based *only* on that retrieved context.

### How It Works

1. **Setup**: You create a "Data Store" in Vertex AI Agent Builder linked to
   your GCS bucket.
2. **Tool Execution**: The `datastore_search_tool` in `datastore.py` uses the
   Google Cloud Discovery Engine client library to query this Data Store.
3. **Search Configuration**: The search request is configured to return
   "chunks" (snippets of text) rather than full documents, and uses features
   like "Query Expansion" to find relevant results even if the user uses
   different terminology.
4. **Result**: The tool returns a list of text chunks. The ADK passes these to
   the Gemini model, which uses them to answer the user's question.

### Key Terms

**Vertex AI Agent Builder (Discovery Engine)**: Google's platform for building
search and chat applications using RAG. It handles the complex infrastructure of
vector databases and indexing.

**Unstructured Data**: Data that doesn't have a pre-defined data model, like PDF
files, Word documents, or HTML pages.

**Chunking**: The process of breaking large documents into smaller, manageable
pieces (chunks) for better retrieval and context window management.

---

## SETUP INSTRUCTIONS

This demo requires significant setup in the Google Cloud Console.

### 1. Google Cloud Storage (GCS)

1. Go to **Cloud Storage** in the console.
2. Click **Create Bucket**. Choose a unique name (e.g.,
   `my-financial-docs-bucket`) and a region (e.g., `us-central1`).
3. Upload the sample PDF files from the `docs` folder into this bucket.

### 2. Vertex AI Agent Builder (Data Store)

1. Go to the "Agent Builder" or "Gen App Builder" in the console by 
   searching for **AI Applications** using the Google Cloud Console search bar.
2. Select **Create App**.
3. Choose an app type of **Custom Search (general)**.
4. Leave the app settings unchanged (you want Enterprise edition features 
   and Generative responses and leave the location as "global").
5. Enter an App name, a company name for the app, and select Continue.
6. You'll be taken to the data stores page. Select **Create a Data Store**:
    * Select **Cloud Storage** as the source.
    * Browse and select the bucket you created.
    * Select **Unstructured documents** (PDF, HTML, etc.).
    * Select a one time synchronization frequency.
    * Leave other settings alone for now and select Continue.
    * Enter a Data store name. It is usually a good idea to give it a name
      based on the App name you chose.
    * Leave the other configuration settings as default and select Continue.
    * Select General Pricing and select Create.
7. **Link Data Store**: Select the data store you just created and click 
   **Continue**.
8. **Select Pricing Model**: Leave it set to General Pricing and select Create.
9. **Wait**: The indexing process takes a few minutes. Check the "Data" left 
   navigation to see the "Activity" and then the "Documents" once imported.

### 3. Get Configuration Values

You can click on the "AI Applications" name in the left navigation to return 
to the list of all the Apps.

1. Note the **Location** of your App (usually `global`) which may be 
   different than the location of other parts of your project.
2. Find the **App ID** in the list of apps. It is a string of letters and 
   numbers. It is **not** the same as the Data Store ID, although they look 
   similar.
3. Note your **Project ID**. This is usually the same as the Project ID 
   you're using for Vertex AI Gemini, but you can make sure you have it by 
   going back to the Google Cloud Console home page.
4. Update your `.env` file:
   ```bash
   DATASTORE_PROJECT_ID=<your-project-id>
   DATASTORE_LOCATION=global # or us-central1
   DATASTORE_ENGINE_ID=<your-app-id>
   ```

### 4. Authenticate

Run `gcloud auth application-default login` to allow the local script to access
the Discovery Engine API.

---

## CODE WALKTHROUGH

### Repository Structure

```
.
├── __init__.py           # Package initialization.
├── agent-prompt.txt      # Agent instructions.
├── agent.py              # Agent configuration.
├── datastore.py          # (Crucial) The RAG retrieval logic.
├── docs/                 # Sample financial documents (PDFs).
├── README.md             # Setup instructions.
└── requirements.txt      # Dependencies (google-cloud-discoveryengine).
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
  name="financials_rag_agent",
  # ...
  tools=[datastore_search_tool],
)
```

---

## Important Details

### Best Practices

- **Metadata**: In a real app, you would also return the `document.id` or `link`
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
