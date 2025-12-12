# cd14768 - Lesson 09 - demo

Implementing Long-Term Agent Memory with ADK and VertexAI Agent Engine Memory
Bank

- Objective: Learn to implement long-term agent memory using ADK and Vertex AI
  Agent Engine Memory Bank.
- Setup
    - Ensure `.env` is configured with project, location, and
      `GOOGLE_GENAI_USE_VERTEXAI=TRUE`.
    - Navigate to `lesson-09-long-term-agent-memory/notes`.
    - Run `python create_agent_engine.py` to create an Agent Engine instance.
    - Copy the resource name output by the script.
    - Update `.env` with `AGENT_ENGINE_ID=<resource name>`,
      `AGENT_ENGINE_PROJECT`, and `AGENT_ENGINE_LOCATION`.
- [agent.py] Imports and Configuration
    - Import `preload_memory_tool` from `google.adk.tools`.
    - Import `CallbackContext` for the callback function.
    - Load `AGENT_ENGINE_PROJECT`, `AGENT_ENGINE_LOCATION`, and
      `AGENT_ENGINE_ID` from environment variables.
    - These are required to connect to the Memory Bank.
- [agent.py] `auto_save_session_to_memory_callback` function
    - Define an async function that takes `CallbackContext`.
    - Call
      `callback_context._invocation_context.memory_service.add_session_to_memory(...)`.
    - This hooks into the agent lifecycle to save the session state to the
      Memory Bank after each interaction.
- [agent.py] Tools Configuration
    - Add `preload_memory_tool` to the `tools` list.
    - This tool is responsible for injecting relevant past memories into the
      agent's context.
- [agent.py] `root_agent` Initialization
    - Register `after_agent_callback=auto_save_session_to_memory_callback`.
    - This ensures the saving logic runs automatically after the agent finishes
      its turn.
- [agent-prompt.txt] System Prompt
    - "You should remember past conversations and bring them up as part of your
      present conversation."
    - This explicit instruction guides the LLM to utilize the context provided
      by the memory system.
- Running the code
    - Start `adk web` in the terminal.
    - Ensure you are in the parent directory or have the correct path to the
      agent.
- Demonstration
    - **First Conversation:**
        - Type "Hi, I love playing tennis on weekends."
        - Agent should acknowledge and discuss tennis.
        - Observe "save session to memory" in the terminal output after the
          turn.
        - End the session/refresh the page to start a new session (simulate a
          new day/interaction).
    - **Second Conversation:**
        - Type "What should I do this Saturday?"
        - Agent should recall the previous conversation about tennis and suggest
          playing tennis.
        - This demonstrates the long-term memory in action.
    - **Verification in Cloud Console:**
        - Go to Google Cloud Console -> Agent Engine.
        - Select the created instance.
        - Navigate to the "Memories" tab.
        - Show the entry for the user/session, confirming the "Fact" about
          tennis is stored.
        - Explain that this stored summary is what the agent retrieved in the
          second conversation.
- Conclusion
    - Summarize how ADK's `MemoryService` and `after_agent_callback` combined
      with Vertex AI Agent Engine Memory Bank enable persistent, long-term
      context for agents.
