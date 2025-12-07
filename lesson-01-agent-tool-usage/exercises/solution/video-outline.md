# cd14768 - Lesson 1 - exercise
Implementing Calculator Tools

- This exercise focuses on implementing an ADK agent that utilizes specific
  tools to perform arithmetic operations, showcasing how LLMs can delegate complex
  or deterministic tasks to external functions. You will gain practical experience
  in defining, implementing, and integrating tools within an ADK agent.
- [agent.py] Define tool functions (`addition`, `subtraction`, `multiplication`,
  `division`)
  - These functions provide deterministic mathematical capabilities to the agent.
  - Emphasize type hinting and descriptive docstrings crucial for the LLM's
    understanding of tool purpose and arguments.
  - Highlight error handling in the `division` function for robustness (e.g.,
    division by zero).
- [agent-prompt.txt] Define agent instructions and persona
  - This file sets the agent's role as a helpful mathematical assistant and
    explicitly guides it to use the available tools for calculations.
  - A clear and concise prompt is essential for effective tool utilization.
- [agent.py] Create the ADK Agent instance (`root_agent = Agent(...)`)
  - Show the model used ("flash" not "flash-lite"). Discuss how testing it 
    to find the right version was important
  - This step shows how the agent is assembled, integrating its name,
    description, model, instructions from `agent-prompt.txt`, and the defined
    calculator tools.
  - It demonstrates the central point where all components are brought together
    to form a functional calculator agent.
- running the code
  - start `adk web` in another window from the parent directory of the agent
    (i.e., `cd lesson-01-agent-tool-usage` then `adk web`)
  - navigate to the displayed URL in your browser.
- demonstration
  - In the `adk web` chat interface, provide prompts like:
    - "What is 5 plus 3?"
    - "What is 100 divided by 4?"
    - "What is 5 plus 3 plus two?" (to show multiple tool calls)
  - Observe the agent calling the appropriate calculator tools and returning
    accurate results.
  - Show how clicking on each message shows debugging information, including
    tool calls and their outputs.
  - Emphasize that customers only see the final, coherent response, not the
    intermediate tool execution steps.
- conclusion and summary
  - Tools are indispensable for LLMs to handle deterministic tasks like math
    accurately, overcoming their inherent limitations.
  - Clear tool definitions, including type hints and docstrings, are vital
    for the LLM to intelligently select and use the correct tools.
  - ADK streamlines the process of integrating and orchestrating these tools,
    enabling the creation of powerful and versatile agents.
