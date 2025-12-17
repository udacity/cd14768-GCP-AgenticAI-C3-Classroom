# cd14768 - Lesson 09 - demo

Implementing Long-Term Agent Memory with ADK and VertexAI Agent Engine Memory
Bank

- Objective: Learn to implement long-term agent memory using ADK and Vertex AI
  Agent Engine Memory Bank.
- What is the Memory Service?
    - A service that provides persistent storage for agent interactions.
    - It uses AI to summarize and index conversations.
    - Hooks in ADK allow it to save the conversation summary, and then 
      reload it during another session.
    - The conversation summary is included as part of the prompt sent to the 
      LLM.
    - **Why it's useful**: Allows agents to maintain context across different
      sessions and long periods of time, creating a more personalized and
      intelligent experience without managing complex database schemas manually.
- Comparison with Session/User State
    - **Session State**: 
      - Ephemeral key/value data for current conversation (e.g., itinerary).
      - Reset for each session
      - Read and write through a tool and prompts can be written to include 
        values.
    - **User State**: 
      - Simple key-value pairs (e.g., favorite color). 
      - Structured but limited.
      - Read and write through a tool and prompts can be written to include
        values.
    - **Agent Engine Memory**: 
      - Unstructured, semantic summaries. 
      - "Fuzzy" recall of concepts over time.
      - Pre-defined hooks to save the summary after every exchange and 
        include the summary in every prompt. 
- Setup (Prerequisites for running the code)
    - Before we get started, we need to set up the backend it needs.
    - Navigate to `notes` directory.
    - Run `python create_agent_engine.py` to create an Agent Engine
      instance.
    - **Crucial**: Copy the resource name output by the script. We will need
      this to start the agent. Also available later in the console.
- [agent.py] `root_agent` Initialization
    - Start by showing the `root_agent` definition.
    - Highlight `model="gemini-2.5-flash"` and `tools` list.
    - **Crucial Point**: Point out
      `after_agent_callback=auto_save_session_to_memory_callback`.
    - Explain that this parameter is the key to hooking into the agent's
      lifecycle for memory persistence.
- [agent.py] `auto_save_session_to_memory_callback` function
    - Move up to the definition of this callback function.
    - Explain it takes `CallbackContext`.
    - Show the call to
      `callback_context._invocation_context.memory_service.add_session_to_memory(...)`.
    - Explain how this saves the current session state to the configured 
      Memory Bank service. 
- [agent.py] Tools Configuration
    - Show the `tools` list containing `preload_memory_tool`.
    - Explain that while the callback *saves* memory, this tool *loads* relevant
      past memories into the agent's context before it generates a response.
    - Not a typical tool - we won't see it listed as a tool or the LLM
      request to call it.
- [agent.py] Imports
    - Scroll to the top to show the imports: `preload_memory_tool`,
      `CallbackContext`.
    - Note we do **not** configure the memory service in the code. That is
      injected at runtime.
- [agent-prompt.txt] System Prompt
    - Show the instruction: "You are a friendly agent..."
    - Discuss how we guide the agent to ask about hobbies.
    - Explain that the memory is injected by ADK, but the prompt guides the
      agent persona.
- Running the code
    - Start `adk web` in the terminal using the memory service URI.
    - `adk web --memory_service_uri agentengine://...` (paste your resource
      name)
- Demonstration
    - **First Conversation:**
        - Type "Hi, I love playing tennis on weekends."
        - Agent acknowledges.
        - **Highlight**: Observe "save session to memory" in the terminal
          output.
        - End session/refresh page.
    - **Second Conversation:**
        - Type "What should I do this Saturday?"
        - Agent recalls tennis and suggests it.
    - **Verification in Cloud Console:**
        - Go to Google Cloud Console -> Agent Engine -> "Memories" tab.
        - Show the stored "Fact" about tennis for the user.
        - Connect this visual proof back to the
          `auto_save_session_to_memory_callback` we saw in the code.
- Conclusion
    - By keeping the memory service configuration itself out of our code, we
      reduce dependency on a specific service.
    - Memory services are a powerful way to remember conversational summaries
      between sessions.

