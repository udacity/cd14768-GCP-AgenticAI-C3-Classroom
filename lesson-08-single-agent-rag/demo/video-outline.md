# cd14768 - Lesson 8 - demo
Implementing Single-Agent RAG with Vertex AI

- In this demo, we'll build a RAG agent that can answer questions about financial
  documents (10-Ks) using Vertex AI Agent Builder.
- [Setup Walkthrough] Cloud Console
  - **GCS Bucket**: Show the bucket where PDFs are uploaded.
  - **Agent Builder (Data Store)**:
    - Show the created "Search" App.
    - Show the "Data Store" configuration pointing to GCS.
    - Show the "Activity" tab to confirm documents are indexed.
  - **IDs**: Show where to find the `Project ID`, `Location`, and `Engine ID` (App ID).
- [datastore.py] The Search Logic
  - Review `search` function.
  - **Serving Config**: Explain that this path tells Google *which* search engine to query.
  - **Content Spec (`CHUNKS`)**: Explain that we request "Chunks", not documents. This is the "R" in RAG.
  - **Query Expansion**: Explain how this helps find synonyms ("revenue" vs "sales").
  - **Client Library**: Show `discoveryengine.SearchServiceClient`.
- [agent.py] Agent Integration
  - Show how `datastore_search_tool` is registered like any other tool.
  - Explain: "The agent doesn't know *how* to search, it just knows it *can* search."
- running the code
  - start `adk web` in another window (`cd lesson-08-single-agent-rag` then `adk web`)
  - navigate to the URL.
- demonstration
  - Prompt: "What was the revenue for Alphabet in 2023?"
  - **Walkthrough**:
    - Agent calls `datastore_search_tool("Alphabet revenue 2023")`.
    - `datastore.py` sends request to Vertex AI.
    - Vertex AI retrieves relevant text chunks from the PDF.
    - Agent receives chunks.
    - Agent synthesizes answer: "According to the documents, Alphabet's revenue was..."
- conclusion and summary
  - RAG connects LLMs to your private data.
  - Vertex AI Agent Builder handles the hard parts: OCR, chunking, and indexing.
  - The `discoveryengine` library provides a programmatic interface for agents.
