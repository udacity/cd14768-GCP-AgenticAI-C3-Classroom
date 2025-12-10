# cd14768 - Lesson 7 - exercise

Using other tools with Google Search

- In this solution walkthrough, we'll examine a multi-agent system that combines
  web search with custom calculations.
- [search_agent.py] Review the Sub-Agent
    - Show how `search_agent` is configured with `google_search`.
    - Point out this is a separate agent that runs independently of our root 
      agent.
    - **Critical**: Highlight
      `search_agent_tool = AgentTool(agent=search_agent)`.
    - Explain: "This `AgentTool` wrapper lets us treat the entire search agent
      as a single tool."
- [tools.py] Review Calculation Tools
    - Quickly show `calculate_percentage_change` and `calculate_profit_or_loss`.
    - Note: These are standard Python functions, completely separate from the
      search logic.
- [agent.py] Review Main Agent Configuration
    - Show the `tools` list: It contains both `search_agent_tool` AND the
      calculation functions.
    - This now works just like all the other agents with tools to call do.
- [Prompts] Review Orchestration
    - **Search Prompt**: Focused on finding facts (prices, dates).
    - **Main Prompt**: Focused on answering the user's financial questions using
      available tools.
- running the code
    - start `adk web` in another window (`cd lesson-07-web-search-agents` then
      `adk web`)
    - navigate to the URL.
- demonstration
    - Prompt: "If I bought 10 shares for $200, how much would I have made or 
      lost at closing today?" 
    - **Walkthrough**:
        - **Step 1**: Main agent calls `search_agent_tool` to get the current
          price.
        - **Step 2**: Search agent (internally) calls `google_search`.
        - **Step 3**: Search agent returns the price (e.g., "$180").
        - **Step 4**: Main agent calls `calculate_profit_or_loss(10, 150, 180)`.
        - **Step 5**: Main agent answers: "Yes, you made a profit of $300."
- conclusion and summary
    - We solved the problem of mixing search and calculation.
    - The `AgentTool` pattern allows for powerful, hierarchical agent designs.
    - This keeps our code modular and our prompts focused.
