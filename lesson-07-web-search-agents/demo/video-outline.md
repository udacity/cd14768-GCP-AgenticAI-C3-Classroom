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
  - The prompt is straightforward, but tries to bias the LLM to using the 
    search tool for all queries, not just ones requiring recent information.
  - This aims to make it more accurate.
- running the code
    - start `adk web` in another window (`cd lesson-07-web-search-agents` then
      `adk web`)
    - navigate to the URL.
- demonstration
    - Prompt: Who was the most recent Nobel Prize winner for physics?
        - Show how there are additional search buttons
        - Show how the event includes grounding metadata about the references
    - Prompt: What is 2+2?
        - Show how it does not do external references 
- conclusion and summary
    - Grounding solves the "knowledge cutoff" problem.
    - It reduces hallucinations by forcing the model to cite sources.
    - Since the tool is built into ADK and Gemini, implementation is trivial 
      (import `google_search`), but the impact is massive.
