# Module 4 Exercise Solution: Using Session state for trip planning

This solution demonstrates a completed travel agent that effectively uses both
user-scoped and session-scoped state to manage persistent preferences and
ephemeral trip itineraries.

---

## Overview

### What You'll Learn

This solution illustrates how to properly scope variables in the ADK to achieve
desired memory behaviors. You will see how `user:home_location` persists across
sessions to provide personalization, while `itinerary` (session-scoped) resets
cleanly for each new trip planning session.

Learning objectives:

- Correctly implementing `user:` prefix for persistent storage.
- Managing session-scoped lists (itineraries) without prefixes.
- Using dynamic prompt injection to modify agent behavior based on stored state.

### Prerequisites

- Understanding of the Exercise requirements.
- Familiarity with Python dictionaries and lists.

---

## Understanding the Concept

### The Problem

We needed an agent that could remember a user's home city "forever" (or until
changed) so they don't have to repeat it every time they want to plan a trip.
However, we also needed the agent to be able to plan *new* trips from scratch
without getting confused by old itineraries from previous sessions.

### The Solution

We used:

1. **`user:home_location`**: Stored in the User scope. This data survives the
   end of the session.
2. **`itinerary`**: Stored in the Session scope (no prefix). This data is wiped
   when a new session begins.

**Why not just rely on conversational context?**
If we just relied on the conversation history (the context window), the agent
would forget the home location as soon as that conversation ended or if the
context window got too full. By explicitly storing it in `user:` state, we
offload that "fact" to a durable store, making the agent more reliable and
capable of long-term personalization.

While we might be able to rely on the conversational history to keep track  
of the locations we wish to travel to, there is a good chance that the LLM 
would lose track of this and begin to hallucinate locations. By explicitly 
managing it in the state, we can keep track of it.  

---

## CODE WALKTHROUGH

### Repository Structure

```
.
├── __init__.py           # Package initialization.
├── agent-prompt.txt      # Agent instructions.
├── agent.py              # Agent configuration.
├── tools.py              # Tool logic for state management.
├── README.md             # Environment setup.
└── requirements.txt      # Dependencies.
```

### Step 1: Setting Home Location (`tools.py`)

In `set_home_location`, we use the `user:` prefix.

```python
def set_home_location(location: str, tool_context: ToolContext):
  # Store in USER scope
  tool_context.state["user:home_location"] = location

  # Set persistent instruction
  tool_context.state["user:home_location_instruction"] = f"""
      The customer's home location is: {location}.
      If they do not specify a different starting location, you should 
      add this home location as the first city of the itinerary.
    """
  return f"Home location set to {location}."
```

**Why it matters**: This ensures that even if you refresh the page (starting a
new session), the agent still knows your home location.

### Step 2: Managing Itinerary (`tools.py`)

In `add_city`, we *do not* use a prefix.

```python
def add_city(tool_context: ToolContext, city: str):
  # Get from SESSION scope (defaults to empty list)
  itinerary = tool_context.state.get("itinerary", [])

  itinerary.append(city)

  # Update SESSION scope
  tool_context.state["itinerary"] = itinerary
  return {"status": f"Added {city} to the itinerary."}
```

**Why it matters**: If we used `user:itinerary`, your old trips would show up
when you tried to plan a new one next week. By using session scope, we get a
fresh slate every time.

### Step 3: Creating Itinerary (`tools.py`)

The `create_itinerary` tool combines these scopes. It looks at the
session-scoped `itinerary` and, if needed, prepends the user-scoped
`user:home_location`.

```python
def create_itinerary(tool_context: ToolContext):
  itinerary = tool_context.state.get("itinerary", [])
  home_location = tool_context.state.get("user:home_location")

  # Logic to prepend home_location if it exists and itinerary doesn't start with it
  # ...
```

### Step 4: Dynamic Prompt (`agent-prompt.txt`)

The prompt injects the instruction we saved in `set_home_location`.

```text
You are a travel agent...
{user:home_location_instruction?}
```

This allows the agent to "know" the rule about using the home location without
us having to hardcode it or repeat it in every user query.

### Complete Example

1. **Session A**:
    - User: "Home is New York City." -> `user:home_location` = "New York City".
    - User: "Plan trip to London." -> `itinerary` = ["London"].
    - `create_itinerary` -> New York City -> London.
2. **Session B** (New Session):
    - `itinerary` is empty (reset).
    - `user:home_location` is still "New York City".
    - User: "Plan trip to Los Angeles." -> `itinerary` = ["Los Angeles"].
    - `create_itinerary` -> New York City -> Los Angeles.

The agent remembered "New York City" but forgot "London", which is exactly what
we wanted.

---

## Important Details

### Best Practices

- **Explicit Scoping**: Always be intentional about whether a piece of data
  belongs to the *user* (long-term) or the *session* (short-term).
- **Prompt Injection**: Use dynamic prompt injection (`{key?}`) to bring state
  into the LLM's reasoning context. This bridges the gap between structured
  state and unstructured conversation.
- **Testing Persistence**: Always verify your agent behavior by simulating a new
  session (refreshing the page) to ensure user-scoped data persists and
  session-scoped data resets.

### Common Errors

- **Leaking State**: Accidentally using `user:` prefix for temporary data (like
  the itinerary) causes confusion in future sessions.
- **Forgetting Preferences**: forgetting the `user:` prefix for preferences
  means the user has to repeat themselves every time.