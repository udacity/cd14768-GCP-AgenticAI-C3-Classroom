# Module 8: Implementing Single-Agent RAG with ADK and Vertex AI Search/RAG Engine

This exercise guides you through building a Retrieval-Augmented Generation (RAG)
agent. Your agent will use Vertex AI Search to index custom documents about
brand new superheroes and supervillains, and then retrieve relevant information
to ground its answers to user questions.

---

## Overview

### What You'll Learn

You will implement the complete workflow for setting up a RAG system on Google
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

1. **Document Generation**: You will use Gemini or Gemini CLI to generate
   creative content about superheroes, supervillains, and their TV series.
2. **Setup**: You create a "Search App" and "Data Store" in Vertex AI Search
   linked to your GCS bucket containing your generated documents.
3. **Tool Execution**: You will implement the `datastore_search_tool` in
   `datastore.py` which uses the Google Cloud Discovery Engine client library to
   query this Data Store.
4. **Search Configuration**: Your search request will be configured to return "
   chunks" (snippets of text) rather than full documents, and use features
   like "Query Expansion" to find relevant results.
5. **Result**: The tool will return a list of text chunks. The ADK passes these
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

## Exercise Instructions

### Your Task

Your task is to build a RAG agent that can answer questions about a custom
superhero universe. You will first create the content for this universe, set up
the necessary Google Cloud infrastructure, and then implement the ADK agent to
interact with it.

### Google Cloud Setup

This exercise requires significant setup in the Google Cloud Console.

#### 1. Generate Documents

Create at least 30 documents using Gemini or Gemini CLI, saving them as individual
files (e.g., Markdown or PDF).

- 10 documents detailing brand new superheroes (one hero per file).
- 10 documents detailing brand new supervillains (one villain per file).
- 10 documents describing a television series (one series per document),
  each centered around one of your superheroes. Each series should have at
  least 12 episodes, include the hero's origin story, and feature at least
  one crossover episode with another hero or villain.

#### 2. Google Cloud Storage (GCS)

1. In the Google Cloud Console, go to the "Cloud Storage" configuration.
   (Hint: You can search for it in the search bar).
2. Select "Create bucket".
3. Choose a unique name (e.g., `my-superhero-docs-bucket`) and a
   region (e.g., `us-central1`).
4. Select "Create".
5. If there is a pop-up about Public access, confirm that you want
   Enforce public access prevention enabled.
6. Upload your generated superhero, supervillain, and TV series
   documents into this bucket.

#### 3. Vertex AI Search

1. In the Google Cloud Console, go to the "AI Application"
   configuration. (Hint: You can search for "AI Applications" in the
   search bar).
2. Select "Create App".
3. Choose an app type of "Custom Search (general)".
4. Leave the app settings unchanged (you want Enterprise edition
   features and Generative responses, and leave the location as
   "global").
5. Enter an App name (e.g., "Superhero-FAQ-App"), a company name for the
   app, and select Continue.
6. You'll be taken to the Data Stores page. Select "Create Data Store":
    * Select "Cloud Storage" as the source.
    * Browse and select the GCS bucket you created previously.
    * Select "Unstructured documents" (PDF and markdown files are unstructured. 
      Things like CSV files are structured.).
    * Select a one time synchronization frequency.
    * Leave other settings alone for now and select Continue.
    * Enter a Data store name (e.g., "Superhero-Data-Store"). It is
      usually a good idea to give it a name based on the App name you
      chose.
    * Leave the other configuration settings as default and select
      Continue.
    * Select General Pricing and select Create.
7. **Link Data Store**: Select the data store you just created and
   click "Continue".
8. **Select Pricing Model**: Leave it set to General Pricing and select
   Create.
9. **Wait**: The indexing process takes a few minutes. Check the "Data"
   left navigation to see the "Activity" and then the "Documents" once
   imported.
10. **Get Configuration Values**: After creation, you can click on the
    "AI Applications" name in the left navigation to return to the list
    of all the Apps.
    * Note the **Location** of your App (usually `global`).
    * Find the **App ID** in the list of apps. This is the value you
      need for `DATASTORE_ENGINE_ID` in your `.env` file.
    * Note your **Project ID**. This is usually the same as the Project
      ID you're using for Vertex AI Gemini, and you'll need it for
      `GOOGLE_CLOUD_PROJECT` and `DATASTORE_PROJECT_ID` in your `.env`
      file.

#### 4. Authenticate

Run `gcloud auth application-default login` in your terminal to allow the local
script to access the Discovery Engine API.

### Requirements

Your implementation must:

1. Implement `datastore.py`: Complete the `datastore_search_tool` function
   to correctly call the `search` function with environment variables.
2. Implement `agent.py`: Configure the `root_agent` to use your implemented
   `datastore_search_tool`.
3. Agent Prompt: Write an `agent-prompt.txt` that instructs the agent on how
   to use the search tool and answer questions about your superhero universe.

### Repository Structure

```
.
├── __init__.py           # Package initialization.
├── agent-prompt.txt      # (TODO) Agent instructions.
├── agent.py              # (TODO) Agent configuration.
├── datastore.py          # (TODO) The RAG retrieval logic.
├── .env-sample           # Environment variable template.
└── requirements.txt      # Dependencies.
```

Make sure you copy `.env-sample` to `.env` and edit it to add the Google Cloud
project details you are working with. Remember that you should **never**
check-in your .env file to git.

### Starter Code

You are provided with boilerplate code. Your primary tasks will involve filling
in the `TODO` sections.

**`agent.py`**

```python
import os
from google.adk.agents import Agent
from .datastore import datastore_search_tool

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
  instruction = f.read()

model = "gemini-2.5-flash"

# TODO: Add the datastore_search_tool to the tools list
tools = []

root_agent = Agent(
  name="superhero_faq_agent",
  description="An agent that can answer questions about superheroes.",
  instruction=instruction,
  model=model,
  tools=tools,
)
```

**`datastore.py`**

```python
import os
from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1 as discoveryengine


# Definition of a tool that accesses a Vertex AI Search Datastore

# This is based on code provided by Google at
# https://cloud.google.com/generative-ai-app-builder/docs/samples/genappbuilder-search
#
# The object definitions aren't available to all IDEs because of Google's ProtoBuf
# implementation, so the IDE may generate a warning, but work fine. I've used
# dicts here instead, but indicated the Class that could be used instead.
# You can see the definitions at
# https://cloud.google.com/python/docs/reference/discoveryengine/latest/google.cloud.discoveryengine_v1.types
#
def search(
    project_id: str,
    location: str,
    engine_id: str,
    search_query: str,
) -> list[str]:
  #  For more information, refer to:
  # https://cloud.google.com/generative-ai-app-builder/docs/locations#specify_a_multi-region_for_your_data_store
  client_options = (
    ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
    if location != "global"
    else None
  )

  # Create a client
  client = discoveryengine.SearchServiceClient(client_options=client_options)

  # The full resource name of the search app serving config
  serving_config = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/servingConfigs/default_config"

  # discoveryengine.SearchRequest.ContentSearchSpec
  content_search_spec = {
    "search_result_mode": discoveryengine.SearchRequest.ContentSearchSpec.SearchResultMode.CHUNKS
  }

  # discoveryengine.SearchRequest
  request = {
    "serving_config": serving_config,
    "query": search_query,
    "page_size": 10,
    "content_search_spec": content_search_spec,
    "query_expansion_spec": {
      "condition": discoveryengine.SearchRequest.QueryExpansionSpec.Condition.AUTO,
    },
    "spell_correction_spec": {
      "mode": discoveryengine.SearchRequest.SpellCorrectionSpec.Mode.AUTO,
    },
  }

  page_result = client.search(request)

  results = []
  for result in page_result:
    if result.chunk and result.chunk.content:
      results.append(result.chunk.content)

  return results


def datastore_search_tool(search_query: str):
  """
  Searches store information for the requested information.

  Args:
      search_query (str): What information about the store the customer is looking for
  """
  # TODO: Call the search function with the appropriate environment variables
```

**`agent-prompt.txt`**

```
TODO
```

### Expected Behavior

Once completed, your agent should be able to answer questions about the
superheroes, supervillains, and TV series you created. When a customer asks a
question, the agent should use the `datastore_search_tool` to retrieve relevant
information from your Vertex AI Search Data Store and then synthesize a grounded
answer.

**Running the agent:**

You will run the agent using the `adk web` tool. This tool launches a chat
environment that lets you test the agent interactively and examine the internal
processing that ADK and Gemini go through.

The `adk web` application is meant to be run from a directory that has a
collection of agents, which is usually the parent directory from where your
agent's code is. Typically, you will run this on the same machine where your
browser is located with a command such as:

```bash
adk web
```

**Example usage (once implemented):**

```
User: Tell me about Captain Comet.
Agent: Captain Comet, whose real name is David Carter, gained his powers after being exposed to cosmic radiation during a space mission... (response grounded in your document)
```

**Expected output (example):**

```
Captain Comet is a superhero with the ability to manipulate cosmic energy. He gained his powers after... (rest of the answer based on your generated document)
```

### Implementation Hints

1. **Generating Documents**:
    * You can use Gemini's free tier or the Gemini CLI to generate the content.
      For example, a prompt could be: "Generate a detailed origin story and
      powers for a new superhero named 'Captain Comet'." Save each generated
      response into a separate `.pdf` or `.md` file.
    * Ensure each document is sufficiently detailed to provide a good answer to
      potential questions.
    * Remember to save all documents into a `docs` folder that you will create
      within your `exercises/starter` directory.
2. **`datastore_search_tool` Implementation**: 
    * The `search` function is provided as boilerplate. You should read 
      through it, and the documentation linked, to get an idea of what 
      other options are available, but these tend to work fairly well for 
      our use case. 
    * Your task is to implement `datastore_search_tool` to correctly call 
      this `search` function using the environment variables set in 
      your `.env` file for `project_id`, `location`, and `engine_id`.
3. **`agent.py` Integration**: Import `datastore_search_tool` from
   `datastore.py` and add it to the `tools` list in your `root_agent`
   definition.
4. **`agent-prompt.txt`**: Craft a clear prompt that guides your
   `superhero_faq_agent` to use the `datastore_search_tool` whenever asked
   questions related to superheroes, supervillains, or TV series. Instruct it to
   provide grounded answers based on the retrieved information.

---

## Important Details

### Common Errors

**Error**: `404 Not Found` or `Resource not found`.

- **Cause**: The `DATASTORE_ENGINE_ID` or `DATASTORE_LOCATION` in your `.env`
  file is incorrect, or the Data Store hasn't finished creating/indexing.
- **Solution**: Double-check the `.env` values against the console. Ensure the
  Data Store status in the console says "Imported" or "Active".

**Error**: Empty results from the agent.

- **Cause**: The documents haven't finished indexing yet, or your search query
  is not effectively matching the content.
- **Solution**: Check the Data Store status in the console. Refine your
  `agent-prompt.txt` to better guide the agent's tool usage or the phrasing of
  `search_query`.

**Error**: `403 Permission Denied`.

- **Cause**: ADC (Application Default Credentials) not set up, or the service
  account/user lacks necessary permissions on the project (e.g., Discovery
  Engine Editor/Viewer roles).
- **Solution**: Run `gcloud auth application-default login`. Verify IAM roles in
  the Google Cloud Console.