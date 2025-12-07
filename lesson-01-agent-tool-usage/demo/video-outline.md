# cd14768 - Lesson 1 - demo
Implementing Agent Tool Usage with ADK and Vertex AI Gemini Function Calling

- Explain how LLM-based agents use external tools (e.g., Web Search, Database,
  APIs, Calculators) to expand their capabilities and interact with real-world
  systems, including concepts like function calling and the role of prompt/output
  parsing.
- [agent.py] Define tool functions (`get_temperature`, `get_precipitation`,
  `get_wind_speed`)
  - These functions simulate external capabilities the agent can leverage.
  - The docstrings are crucial for the LLM to understand how and when to call
    these tools.
- [agent-prompt.txt] Define agent instructions and persona
  - This file sets the agent's role as a weather reporter and guides its
    conversational style and tool usage strategy.
  - It demonstrates how agent behavior can be configured without modifying code.
- [agent.py] Create the ADK Agent instance (`root_agent = Agent(...)`)
  - This is where the agent is assembled, integrating its name, description,
    model, instructions from `agent-prompt.txt`, and the defined weather tools.
  - It shows how ADK facilitates the creation of a functional LLM agent with tools.
- running the code
  - start `adk web` in another window from the parent directory of the agent
    (i.e., `cd lesson-01-agent-tool-usage` then `adk web`)
  - navigate to the displayed URL in your browser.
- demonstration
  - In the `adk web` chat interface, provide the prompt: "What's the weather like in London?"
  - Observe the agent calling multiple weather tools and synthesizing a single,
    coherent response.
  - Show how clicking on each message shows debugging
  - Emphasize how customers don't see the intermediate steps - just the 
    final result
- conclusion and summary
  - Tools are essential for extending LLMs beyond their training data, enabling
    real-time interaction and dynamic capabilities.
  - ADK simplifies the integration and orchestration of tools, making agent
    development efficient.
  - Function calling allows LLMs to intelligently select and execute the right
    tools based on user queries.
