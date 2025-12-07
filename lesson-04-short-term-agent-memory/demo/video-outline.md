# cd14768 - Lesson 4 - demo

Implementing Short-Term Agent Memory with ADK

- Explore how ADK manages state with different scopes (`user:` vs. session),
  enabling agents to remember user preferences across sessions while managing
  task progress within a session.
  - This is necessary because, while the ADK may transmit some state during 
    the conversation with the LLM, some things are not well represented 
    in the conversation exchange.
  - Discuss request state, session state, and user state
  - State can be stored outside the ADK runtime, but we're using memory.
- [tools.py] Explain User vs. Session Scope
    - Review `set_iterations`:
        - Shows how to store `num_iterations` in `user:num_iterations`.
        - Explain that the `user:` prefix means "this state persists for this
          user across sessions".
        - Demonstrates storing `user:num_iterations_instructions` to dynamically
          change future prompt behavior.
    - Review `run_task`:
        - Shows how `num_iterations` is read from the `user:` scope (persistent
          preference).
        - Explains that `current_iteration` (no prefix) is session-scoped,
          meaning it resets with a new session.
- [agent-prompt.txt] Explain Adaptive Prompting
    - Highlight `{user:num_iterations_instructions?}`.
    - Explain how this conditional injection dynamically changes the agent's
      instructions
      based on whether a user preference has already been set, preventing
      repetitive questions.
- running the code
    - start `adk web` in another window (`cd lesson-04-short-term-agent-memory`
      then `adk web`)
    - navigate to the URL.
- demonstration
    - **Session 1 (Setting Preference)**:
        - Prompt: "Let's start."
        - Agent: "How many questions?" (Initial behavior).
        - User: "3 questions."
        - Agent: Calls `set_iterations(3)`. Explain that this updates `user:`
          state.
        - Agent: Calls `run_task`. Asks Question 1.
        - User answers.
        - Agent: Calls `run_task`. Asks Question 2.
        - (Stop here or finish).
        - Review the different values in the state during different rounds
    - **Session 2 (Persistence Demonstration)**:
        - **CRITICAL MOMENT**: Instruct to **refresh the page** or click "New
          Session" in ADK Web.
        - Prompt: "Let's start."
        - **Highlight**: The agent *does not* ask "How many questions?".
          Instead, it immediately calls `run_task` and asks Question 1.
        - Explain: This demonstrates that the agent "remembered" the user's
          preference from Session 1
          (due to `user:` scope), but the task's progress (`current_iteration`)
          correctly reset for the new session.
        - Again, review the different values in the state during different 
          rounds
- conclusion and summary
    - ADK's state scoping (`temp:`, session, `user:`) provides fine-grained
      control over agent memory lifecycles.
    - `user:` state enables powerful personalization and persistent preferences.
    - Session state allows for clean, task-specific tracking that resets with
      each new interaction flow.
    - Combining these scopes allows for sophisticated and context-aware agent
      behaviors.