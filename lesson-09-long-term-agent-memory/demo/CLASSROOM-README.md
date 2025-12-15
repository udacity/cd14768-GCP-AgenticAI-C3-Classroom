# Module 9: Implementing Long-Term Agent Memory with ADK and VertexAI Agent Engine Memory Bank

This lesson teaches how to implement long-term agent memory using ADK and Vertex
AI Agent Engine Memory Bank.

---

## Overview

### What You'll Learn

You will see how we can save and manage conversational context over
extended sessions using Vertex AI Agent Engine Memory Bank.

Learning objectives:

- Understand why we wish to update, prune, and manage an agent’s long-term
  memory and how we can do so with ADK and Vertex AI Agent Engine Memory Bank.
- Learn how to maintain context over extended sessions balancing performance and
  context length.

### Prerequisites

- Basic Python programming.
- Familiarity with Agent Development Kit (ADK) concepts.
- Understanding of basic AI agent principles.
- Basic familiarity with the Google Cloud Console.

---

## Understanding the Concept

### The Problem

Traditional LLMs are stateless, meaning they lose conversational context after
each interaction. This makes it challenging to build agents that can maintain
consistent and personalized interactions over extended periods or across
multiple sessions, leading to repetitive questions and a fragmented user
experience.

While agents largely address this issue within a single session by providing 
the full conversation history to an LLM, this may fall short for longer, 
multi-session, conversations. While tools can be used to remember specific 
properties, this does not solve the problem of remembering the "gist" of 
conversations over time.

### The Solution

Long-term memory solutions, such as Vertex AI Agent Engine Memory Bank, allow
agents to persist and retrieve conversational history and key facts. By
integrating these memory banks with ADK, agents can maintain context, provide
more coherent responses, and offer a personalized experience across extended
interactions.

### How It Works

**Step 1: Save and Summarize Conversation**
ADK session event hooks are used to intercept and save each session's
conversation into the Vertex AI Agent Engine Memory Bank, indexed by the 
user's name. The Memory Bank automatically summarizes conversations, 
identifying key facts and topics.

**Step 2: Integrate into Future Conversations**
These summaries are then incorporated into the system instructions for future 
conversations, allowing the agent to recall past interactions and provide 
relevant context.

### Key Terms

**Long-Term Memory**: The ability of an agent to retain and recall information
over extended periods and across multiple sessions. ADK provides hooks in to 
various implementations.

**Vertex AI Agent Engine Memory Bank**: A service that provides persistent
storage and summarization for agent conversations, enabling long-term memory.

**ADK Session Event Hooks**: Mechanisms within the Agent Development Kit that
allow custom logic to be executed at specific points during a session, such as
saving conversation data.

---

## Setting up Agent Engine Memory Bank

To use the long-term memory features, you need to create an Agent Engine
instance.

### Prerequisites

Ensure you have your `.env` file set up with the following variables:

```bash
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=<your project ID>
GOOGLE_CLOUD_LOCATION=us-central1
```

Replace `<your project ID>` with your actual Google Cloud Project ID.
`us-central1` is recommended for the location.

### Creating the Instance

1.  There is a `notes` folder that contains a `create_agent_engine.py` script.
2.  Run the `create_agent_engine.py` script:
    ```bash
    python create_agent_engine.py
    ```
3.  The script will output a **resource name**. Copy this value, since you 
    will need it when you start `adk web` later.

If you lose the resource name, you can find it in the Google Cloud Console under
the Agent Engine configuration page.

### Viewing Memory in Google Cloud Console

To verify that conversations are being saved and to explore the stored memory:

1.  Visit the [Google Cloud Console](https://console.cloud.google.com/).
2.  In the search bar, type "Agent Engine" and select the service.
3.  Select the Agent Engine instance you created.
4.  Select the "Memories" tab.
5.  You will see the saved information for a user for each app you have 
    using the Agent Engine.
6.  You can hover over the "Fact" column to see the summary that is stored, 
    or click on the three-dot menu on the right and select "Edit".

---

## CODE WALKTHROUGH

---

### Code Walkthrough

### Repository Structure

```
.
├── __init__.py         # Initializes the Python package.
├── agent-prompt.txt    # Contains the system prompt for the agent.
├── agent.py            # Defines the root agent and its functionalities.
└── requirements.txt    # Lists the Python dependencies.
```

### Step 1: Configuring the Agent for Memory Bank

We need to add two elements to our agent to handle session memory:
1. Saving information from the session is done by an `after_agent_callback` 
   hook. This is a function that is called after all the work has been done 
   for a request and right before the result is returned. We define the 
   `after_agent_callback` to the `auto_save_session_to_memory` function 
   which gets the memory service in use and adds the session to the context.
2. Loading the conversational state and injecting it into the prompt. This 
   is done using the predefined `preload_memory_tool`.

Note that neither of these specifically reference the Agent Engine Memory 
Bank. ADK can be configured to use other agent types. We discuss how to 
specifically set it to use the Memory Bank when we discuss running the agent 
below. 

```python
import os
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.preload_memory_tool import preload_memory_tool

# Callback function to save the session to memory bank
async def auto_save_session_to_memory_callback(
    callback_context: CallbackContext):
  print("save session to memory")
  await callback_context._invocation_context.memory_service.add_session_to_memory(
    callback_context._invocation_context.session)


script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
  instruction = f.read()

model = "gemini-2.5-flash"

tools = [
  preload_memory_tool
]

root_agent = Agent(
  name="memory_agent",
  description="An agent that can save conversations to a Memory Bank.",
  instruction=instruction,
  model=model,
  tools=tools,
  after_agent_callback=auto_save_session_to_memory_callback,
  # Register the callback
)
```

**Key points:**

- The `auto_save_session_to_memory_callback` function is an asynchronous
  callback that adds the current session to the memory service.
- `after_agent_callback` ensures that this saving mechanism is triggered after
  each agent interaction.
- The exact memory module depends on other configuration - not our code.

### Step 2: Agent Instruction for Memory

The `agent-prompt.txt` provides instructions to the agent to leverage its
memory. This prompt explicitly tells the agent to remember past conversations,
which guides its behavior in utilizing the long-term memory capabilities
provided by the Memory Bank.

```
You are a friendly agent that has conversations with people about their hobbies.

Keep the following in mind:
* When you first talk to someone, if you don't know what their hobbies are,
  you should ask and explain that is your primary goal.
* If they say they don't have any hobbies, you can start talking about things
  that interest them and steer this towards possible hobbies they may be
  interested in.
* Be careful about what topics they wish to talk about. You should be sure
  that their hobbies and interests are safe.
* Your suggestions and guidance should be encouraging. Your purpose is to
  encourage hobbies and activities that are with others and socially
  beneficial to the person you're talking to, their friends, and others.
```

**Key point:**

- Additional information about the past conversations will be injected into 
  the prompt by the ADK.

### Complete Example

```python
import os
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.preload_memory_tool import preload_memory_tool

# Asynchronous callback to save the current session to the memory service
async def auto_save_session_to_memory_callback(
    callback_context: CallbackContext):
  print("save session to memory")
  # Use the memory_service to add the current session for long-term storage
  await callback_context._invocation_context.memory_service.add_session_to_memory(
    callback_context._invocation_context.session)


# Read the agent's instructions from an external file
script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
  instruction = f.read()

# Define the model to be used by the agent
model = "gemini-2.5-flash"

# List of tools available to the agent
tools = [
  preload_memory_tool
  # A tool that helps preload memory into the agent's context
]

# Initialize the Agent with its configuration
root_agent = Agent(
  name="memory_agent",  # Unique name for the agent
  description="An agent that can save conversations to a Memory Bank.",
  # Description of the agent's purpose
  instruction=instruction,  # Instructions loaded from agent-prompt.txt
  model=model,  # The generative model to use
  tools=tools,  # The tools the agent can use
  # Register the callback to automatically save sessions to the Memory Bank
  after_agent_callback=auto_save_session_to_memory_callback,
)
```

**How it works:**

Since we don't specify the memory service that is used as part of the code, 
we need to specify it when we start `adk web`. We do so giving it the 
`--memory_service_uri` parameter with a value containing the resource name 
returned when we ran `create_agent_engine.py`.

So we would start our agent with:

```bash
adk web --memory_service_uri agentengine://projects/<project_id>/location/us
-central1/reasoningEngines/<engine_id>
```

Once running:
1. The `after_agent_callback` is set to `auto_save_session_to_memory_callback`,
   which ensures that after every interaction, the conversation session is saved
   to the configured Vertex AI Agent Engine Memory Bank.
2. The `agent-prompt.txt` guides the agent to remember past conversations,
   prompting the underlying LLM to utilize the stored memory when generating
   responses.

**Expected output:**
When you interact with this agent using `adk web`, after each turn, you will see
a message "save session to memory" in the console output, indicating that the
session is being saved. If you restart the agent and engage in a new
conversation, the agent should recall aspects of your previous interactions
based on the context stored in the Memory Bank.

---

## Comparison with Session/User State

You should be familiar with how the ADK works with Session and User state 
and how tools can explicitly get and set values from this state. It is 
important to understand how they differ from using long-term memory in this way:

- **Session State**: 
  - Ephemeral data relevant only to the current conversation
    (e.g., current travel itinerary). 
  - Lost when the session ends or is reset. 
  - Values are readable and writable in a tool and you can specify where the 
    values are inserted in the prompt. 
- **User State**: 
  - Key-value pairs linked to a user (e.g., "favorite_color":
    "blue").
  - Lasts longer than a session
  - Good for structured preferences but limited in complexity. 
  - Values are readable and writable in a tool and you can specify where the
    values are inserted in the prompt.
- **Agent Engine Memory Bank (Long-Term Memory)**: 
  - Designed for unstructured,
    semantic memories (e.g., "The user mentioned they like hiking in the fall").
  - Uses AI to summarize and index conversations, allowing for "fuzzy" recall
    of concepts over time, rather than just exact key matches.
  - Lasts longer than a session
  - Hooks save the conversation summary after each round of the conversation 
    and a specialized tool adds the summary to the prompt before messages 
    are sent to the LLM

---

## Important Details

### Common Misconceptions

**Misconception**: "The agent automatically remembers everything said in a
conversation without any specific configuration."
**Reality**: "While LLMs can process context within a single turn, true
long-term memory across sessions requires explicit mechanisms like the ADK's
`MemoryService` and a configured Memory Bank to store and retrieve past
interactions."

**Misconception**: "Saving conversations to Memory Bank will not affect token
usage or cost."
**Reality**: "Saving and retrieving memories, especially detailed ones, will
contribute to token usage as the agent's context window gets populated with past
conversation summaries. Efficient memory management, including pruning and
summarization, is crucial for cost and performance optimization."

### Best Practices

1. **Craft Effective Prompts**: Guide your agent with clear instructions in
   `agent-prompt.txt` to effectively utilize its long-term memory, encouraging
   it to recall and incorporate past conversations.

### Common Errors

**Error**: "Agent does not seem to remember past conversations."

- **Cause**: The `after_agent_callback` might not be correctly configured or 
  the resource name for the Memory Bank might be missing/incorrect.
- **Solution**: Double-check the `root_agent` initialization to ensure
  `after_agent_callback` points to a valid function that calls
  `memory_service.add_session_to_memory`. Verify that you started it 
  correctly with the right value for the `--memory_service_uri`

**Error**: "Errors related to Memory Bank connection or permissions."

- **Cause**: The service account running the agent may not have the necessary
  IAM permissions to access Vertex AI Agent Engine Memory Bank or you gave 
  the incorrect resource name for the Memory Bank.
- **Solution**: Grant the required IAM roles (e.g., `Agent Engine User`) to the
  service account. Ensure the project ID and location are accurate.