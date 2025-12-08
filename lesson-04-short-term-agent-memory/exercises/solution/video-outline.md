# cd14768 - Lesson 4 - exercise

Using Session state for trip planning

- In this solution walkthrough, we'll examine a multi-step travel agent that
  leverages both user-scoped and session-scoped state to provide personalized,
  context-aware planning.
- [tools.py] Review `set_home_location` (User Scope)
    - Highlight `tool_context.state["user:home_location"]`.
    - Explain that `user:` ensures this preference persists across many
      different planning sessions.
    - Show the `user:home_location_instruction` which saves a specific
      instruction string for the prompt.
- [tools.py] Review `add_city` (Session Scope)
    - Highlight `tool_context.state.get("itinerary", [])`.
    - Note the lack of a prefix. This is **Session Scope**.
    - Explain why: We want the itinerary to be fresh for each new conversation.
      We don't want last month's trip to London interfering with today's trip to
      Paris.
- [tools.py] Review `create_itinerary` (Combined Scopes)
    - Show how it retrieves both the session-scoped `itinerary` and the
      user-scoped `home_location`.
    - Explain the logic: It combines long-term preference (Start at Home) with
      short-term intent (Go to Destination).
- [agent-prompt.txt] Review Dynamic Prompt
    - Point out `{user:home_location_instruction?}`.
    - Explain that this injects the "Use home location as default" rule only
      when
      a home location is actually set.
- running the code
    - start `adk web` in another window (`cd lesson-04-short-term-agent-memory`
      then `adk web`)
    - navigate to the URL.
- demonstration
    - **Session 1**:
        - "Set home to SFO." (Sets `user:` state).
        - "I want to go to NYC." (Sets `session` state).
        - "Create itinerary." -> Shows SFO -> NYC.
    - **Session 2 (Refresh Page)**:
        - "I want to go to London."
        - "Create itinerary." -> Shows SFO -> London.
        - **Key Takeaway**: It remembered SFO (User scope) but forgot NYC (
          Session scope).
- conclusion and summary
    - We've demonstrated the power of mixing scopes.
    - **User Scope** (`user:`) is for what is true about the *person* (
      preferences, profile).
    - **Session Scope** (no prefix) is for what is true about the *current
      task* (drafts, progress).
    - Using these correctly creates agents that feel both smart (remembering
      you) and clean (not getting confused by old tasks).