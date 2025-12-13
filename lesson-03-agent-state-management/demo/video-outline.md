# cd14768 - Lesson 3 - demo

Implementing Agent State Management with ADK

- Explore state machines and how the ADK can manage state in a single request,
  focusing on "temp:" (request-scoped) state.
- We will explore this by building an agent that takes as its input some 
  colors to mix and uses a state machine to determine what the resulting 
  color would be.
- Why do we need state? Isn't this just part of the conversation history?
    - **Precision & Reliability**: 
      - LLMs are not good at counting.
      - Asking an LLM to "remember the count" from 10 turns ago is unreliable.
      - State variables (`temp:counter`) are precise and deterministic.
    - **Single Source of Truth**: 
      - The history contains *all* past states. 
      - This can confuse the model. 
      - Injecting the *current* state variable into the prompt gives the model
        an unambiguous instruction.
    - **Separation of Concerns**: 
      - We don't pollute the permanent conversation history with temporary 
        variables (like loop counters) that are only relevant during agent 
        processing. 
- [agent.py] Show the `root_agent` configuration that includes a tool that
  will change what stage we are in.
- [tools.py] Explain the State Machine Logic (`TRANSITIONS`)
    - Briefly define a State Machine: a system with defined states (colors) and
      transitions triggered by inputs (commands).
    - Show the deterministic transitions (e.g., BLACK + ADD_RED -> RED).
- [tools.py] Explain the `change_stage` Tool
    - Highlight `ToolContext` usage to access state.
    - **CRITICAL**: Explain `temp:` prefix (e.g., `temp:stage`).
        - This means the variable lives *only* for the duration of this single
          request.
        - It is cleared when the response is sent to the user.
    - Show how the tool reads the current state, calculates the next state, and
      updates `temp:stage`.
- [agent-prompt.txt] Explain Dynamic State Injection
    - Point out `{temp:stage?}`.
    - Explain that ADK injects the current value of `temp:stage` into the prompt
      before every LLM call.
    - This is how the LLM "sees" the progress it's making.
- running the code
    - start `adk web` in another window (`cd lesson-03-agent-state-management`
      then `adk web`)
    - navigate to the URL.
- demonstration
    - Prompt: "Mix red and blue."
    - **Walkthrough of Events (Clicking on `adk web` events)**:
        - **Initial State**: Show the first prompt sent to LLM (State is likely
          empty or default).
        - **Tool Call 1**: Click the event for
          `change_stage(command="ADD_RED")`.
            - Show the HTTP request to show the prompt and how it changes
            - Show the tool output and the internal state update (if
              visible/logged).
        - **Intermediate Prompt**: Click the *next* request to the LLM.
            - **Highlight**: The prompt now says `The current stage is: "RED"`.
              This proves the state injection worked.
        - **Tool Call 2**: Click event for `change_stage(command="ADD_BLUE")`.
        - **Tool Call 3**: Click event for `change_stage(command="SHOW")`.
        - **Final Response**: Show the agent's final output ("Magenta").
    - Prompt: "Mix red, green, and blue." (Optional, to show longer chain).
- conclusion and summary
    - `temp:` state allows for complex, multi-step logic within a single turn
      without persisting data long-term.
    - `ToolContext` gives tools read/write access to this state.
    - Dynamic prompts (`{key?}`) keep the LLM informed of state changes,
      enabling it to act as a reasoning engine for the state machine.
    - This strategy is particularly useful in cases where
      - We need to keep track of numbers
      - Attribute values will change while the agent is determining a final 
        result
      - Conversation state proves unreliable or the LLM hallucinates results 
        from conversation state
