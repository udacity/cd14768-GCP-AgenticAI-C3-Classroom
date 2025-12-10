# cd14768 - Lesson 7 - demo

Implementing Web Search Agents (Grounding)

- In this demo, we'll see how easily we can give an agent access to the entire
  internet using Grounding with Google Search.
- [agent.py] Review the Code
    - Point out `from google.adk.tools import google_search`.
    - Show that we simply add `google_search` to the `tools` list.
    - Explain: "We don't write any search logic. The ADK and Vertex AI handle
      it."
- [agent-prompt.txt] Review the Prompt
    - Show how simple it is: "You are a helpful assistant..."
    - Explain: "We don't even need to tell it to search. The model is smart
      enough to know when it needs external info."
- running the code
    - start `adk web` in another window (`cd lesson-07-web-search-agents` then
      `adk web`)
    - navigate to the URL.
- demonstration
    - Prompt 1 (Internal Knowledge): "What is the capital of France?"
        - Agent answers instantly: "Paris."
        - **Highlight**: No search tool was used because the model knows this.
    - Prompt 2 (External Knowledge): "What are the latest rumors about the
      iPhone 17 release date?" (Or any current event).
        - **Observation**:
            - The agent pauses slightly.
            - It returns a detailed answer with specific dates and features.
            - **Crucial**: Show the "Grounding Sources" or citations in the ADK
              Web UI (if visible) or explain that the response is constructed
              from search results.
- conclusion and summary
    - Grounding solves the "knowledge cutoff" problem.
    - It reduces hallucinations by forcing the model to cite sources.
    - Implementation is trivial (import `google_search`), but the impact is
      massive.
