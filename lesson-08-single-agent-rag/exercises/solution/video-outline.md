# cd14768 - Lesson 8 - exercise

Implementing Single-Agent RAG with ADK and Vertex AI Search - Solution

- Objective: Demonstrate the solution for building a RAG agent that retrieves
  information from custom superhero documents indexed in Vertex AI Search.
- Setup
    - Generate at least 30 documents (superheroes, supervillains, TV series)
      using Gemini or Gemini CLI. Store them in a `docs` folder.
    - Create a Google Cloud Storage bucket and upload your generated documents.
    - Create a Vertex AI Search App (AI Applications) and Data Store, linking it
      to your GCS bucket.
    - Obtain `PROJECT_ID`, `LOCATION`, and `ENGINE_ID` from your Vertex AI
      Search setup.
    - Update your `.env` file with `GOOGLE_CLOUD_PROJECT`,
      `DATASTORE_PROJECT_ID`, `DATASTORE_LOCATION`, and `DATASTORE_ENGINE_ID`.
    - Authenticate your local environment by running
      `gcloud auth application-default login`.
- [agent.py] Explain the `root_agent` configuration
    - This is the main entry point of our agent.
    - Point out how the `instruction` from `agent-prompt.txt` guides the agent's
      behavior.
    - Highlight `tools=[datastore_search_tool]` to show how the custom tool is
      registered with the agent, enabling it to perform RAG.
- [datastore.py] Explain the `datastore_search_tool` function
    - This function acts as a simple wrapper, exposing the core search
      functionality to the agent.
    - Show how it retrieves environment variables (`DATASTORE_PROJECT_ID`,
      `DATASTORE_ENGINE_ID`, `DATASTORE_LOCATION`) to configure the search.
    - Explain that it calls the `search` function with the user's
      `search_query`.
- [datastore.py] Deep dive into the `search` function implementation
    - Explain the `discoveryengine.SearchServiceClient` initialization and why
      `ClientOptions` is used for location-specific endpoints.
    - Show the construction of the `serving_config` resource name, which points
      to the specific search engine.
    - Discuss the `request` dictionary, focusing on key parameters:
        - `content_search_spec` with `SearchResultMode.CHUNKS`: Crucial for RAG,
          ensuring only relevant text snippets are returned.
        - `query_expansion_spec` with `Condition.AUTO`: Enhances search by
          automatically broadening terms.
        - `spell_correction_spec` with `Mode.AUTO`: Improves search by
          correcting typos.
    - Demonstrate how `client.search(request)` is executed and `page_result` is
      obtained.
    - Show the loop that extracts `result.chunk.content` to gather all relevant
      text chunks.
- Running the code
    - Start `adk web` in the `lesson-08-single-agent-rag/exercises/solution`
      directory.
- Demonstration
    - Open the ADK web interface in your browser.
    - Ask a question about one of your created superheroes, supervillains, or TV
      series (e.g., "Who is [Superhero Name]?", "What is the plot
      of [TV Series Name] episode 5?").
    - Observe the agent's internal trace, showing it calling the
      `datastore_search_tool`.
    - Examine the input to the tool and the returned text chunks from Vertex AI
      Search.
    - Show how the agent synthesizes a grounded answer based on the retrieved
      information.
- Conclusion and summary
    - Recap how the solution effectively uses ADK and Vertex AI Search to build
      a custom RAG agent for domain-specific knowledge.
    - Emphasize the modularity provided by defining a dedicated search tool and
      integrating it with the agent.
