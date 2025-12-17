# cd14768 - Lesson 09 - solution

Implementing Long-Term Agent Memory with ADK and VertexAI Agent Engine Memory
Bank

- Your task was to create a research assistant agent that would retain 
  information about the conversations and research results in between 
  sessions. This sort of business tool is great to help with long term data 
  collection and planning.
- Setup (Prerequisites)
    - Look at `create_agent_engine.py` that was used to setup the agent 
      engine and returned the Agent Engine ID.
    - **Crucial**: Make sure you have the resource name handy or you can get 
      it from the Cloud Console.
- [agent.py] `root_agent` Initialization
    - Start at the bottom with `root_agent`.
    - Highlight the key additions required for the exercise:
        - `tools` list included `preload_memory_tool`.
        - `after_agent_callback` set to `auto_save_session_to_memory_callback`.
- [agent.py] `auto_save_session_to_memory_callback`
    - Move up to the callback function implementation.
    - Explain this was the core task: implementing the logic to save the
      session.
    - Show
      `callback_context._invocation_context.memory_service.add_session_to_memory`.
    - This pushes the research session to the Memory Bank.
- [agent.py] Tools Configuration
    - Show `tools = [search_agent_tool, preload_memory_tool]`.
    - Explain we combined the provided `search_agent_tool` with the
      `preload_memory_tool`.
    - This allows the agent to both discover new information and recall old
      information.
- [agent.py] Imports
    - Show imports of `preload_memory_tool` and `search_agent_tool`.
    - Note we do **not** configure the memory service in the code. That is 
      injected at runtime. 
- Running the code
    - Start `adk web` in the terminal using the memory service URI.
    - `adk web --memory_service_uri agentengine://...` (paste your resource name)
- Demonstration
    - **Session 1 (Research):**
        - Ask: "What are the latest features about Google Gemini?"
        - Agent uses `search_agent_tool` to find answers.
        - **Highlight**: The terminal log "save session to memory" after the
          turn.
        - Comment about something being significant.
        - End session/refresh.
    - **Session 2 (Recall):**
        - Ask: "Was there anything I found important about Google Gemini?"
        - Agent answers *without* searching again.
        - Explain: It used the summarized memory injected by
          `preload_memory_tool`.
        - Look at the LLM request to see it in the prompt.
    - **Verification in Cloud Console:**
        - Go to Google Cloud Console -> Agent Engine -> Memories.
        - Find the user.
        - Show the summary containing the Python 3.12 facts.
- Conclusion
    - By keeping the memory service configuration itself out of our code, we 
      reduce dependency on a specific service.
  - Memory services are a powerful way to remember conversational state
    between sessions.
    - This let us upgrade a transient search agent into a persistent
      research assistant.
