# cd14768 - Lesson 3 - exercise
Implement Agent State

- We'll examine an ADK agent that implements a
  state machine to manage tool call retries, creating a robust, fault-tolerant system.
  We'll see how request-scoped state (`temp:`) tracks retry counts and process stages.
- [tools.py] Review the `TRANSITIONS` Dictionary
  - Notice the defined states: `START`, `GETTING_TIME`, `SUCCESS`, and `FAILURE`.
  - See how commands trigger specific transitions (e.g., `BAD` moves from `GETTING_TIME` to `FAILURE`).
- [tools.py] Review the `change_stage` Logic
  - See how we read `temp:stage` and `temp:retry_count` from `tool_context.state`.
  - Note the logic that increments the retry count on every call.
  - Observe how `get_time()` is only called when the new state is `GETTING_TIME`.
  - This logic ensures the tool is the executor, while the agent is the decision maker.
- [agent-prompt.txt] Review Agent Instructions
  - Highlight the dynamic state injection: `{temp:stage?}` and `{temp:retry_count?}`.
  - Read the instructions that guide the agent: "If attempts < 3, issue GET_TIME".
  - This prompt effectively programs the agent to act as the state machine's logic engine.
- [agent.py] Review Agent Configuration
  - Confirm that the `change_stage` tool is imported and registered with the `Agent`.
- running the code
  - start `adk web` in another window (`cd lesson-03-agent-state-management` then `adk web`)
  - navigate to the URL.
- demonstration
  - Prompt: "Get me the current time."
  - **Walkthrough**:
    - Observe the agent attempting to get the time.
    - Since `get_time` has a 50% failure rate, watch for retries.
    - Click on the event logs to show `temp:retry_count` incrementing in the `ToolContext`.
    - Show a successful run (State transitions to `SUCCESS` and time is returned).
    - Emphasize how `temp:` scoped state is reset after each user request / 
      agent response set.
    - Run again to try and trigger a failure case (State -> `FAILURE` after 3 tries).
- conclusion and summary
  - We've demonstrated how to handle uncertainty and tool failures using state.
  - By combining `temp:` state with a clear state machine, the agent autonomously
    managed retries and recovery within a single user request.
  - This pattern is essential for production-grade agents.