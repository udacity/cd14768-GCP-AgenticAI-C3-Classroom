# cd14768 - Lesson 7 - solution

Using other tools with Google Search (Financial Assistant)

- In this exercise, you needed to build several tools to retrieve current 
  financial information using Grounding with Google Search and calculate 
  information such as percentage change or profit and loss.
  - The catch is that the `google_search` tool doesn't work with other tools 
    or structured output. So we needed a way to address this.
  - The solution is to create another agent that acts as our `search_agent` 
    that does nothing but searches. We can then use the special `AgentTool` 
    class to make this agent look like a tool.
  - In this case, when the tool is called, it passes the request on to an 
    agent, which makes its own call to the LLM. The LLMs response is 
    returned from the tool call to the root agent.
  - But there continues to be an issue - we want the search results to be 
    structured, and structured outputs are treated like a tool. So our 
    `search_agent` can't define a structured output schema.
  - Our workaround is to use *another* Agent.
  - This agent, our `structured_search_agent` wraps the `search_agent` as 
    its only tool and also defines the `output_schema` it wants to use.
  - It is this `structured_search_agent` that becomes the tool our 
    `root_agent` has available.
- [agent.py] Root Agent
    - Show `tools` list.
    - Includes `search_agent_tool` AND the math tools.
    - The root agent doesn't know about `google_search` directly; it just asks
      for structured stock data.
- [tools.py] Calculation Tools
    - Show `calculate_percentage_change` and `calculate_profit_or_loss`.
    - Simple Python functions, nothing special here.
- [search_agent.py] The Agent Chain
    - **Step 1: The Final Tool**
        - Show `search_agent_tool = AgentTool(agent=structured_search_agent)`.
        - This wraps the *structured* agent to be used by the root.
    - **Step 2: Output Model**
        - Show `StockSearchResult` Pydantic model.
        - Defines the contract: ticker, price, change, etc.
    - **Step 3: Structured Agent**
        - Show `structured_search_agent` definition.
        - **Critical**: `tools=[AgentTool(agent=search_agent)]`.
        - **Critical**: `output_schema=StockSearchResult`.
        - It uses the base agent to get data, then forces it into the schema.
    - **Step 4: Base Search Agent**
        - Finally show `search_agent` definition.
        - Point out `tools = [google_search]`.
        - Its job is purely to find raw information.
- Demo
    - Start `adk web`.
    - Query: "What's the profit if I bought 10 shares of GOOG at $150 and sold
      at today's price?"
    - **Trace the flow**:
        1. Root calls `search_agent_tool`.
        2. Structured agent calls `search_agent`.
        3. Search agent calls `google_search`.
        4. Data returns up the chain, getting structured.
        5. Root calls `calculate_profit_or_loss`.
        6. Final answer.
- Conclusion
    - Using `AgentTool` allows us to chain agents as tools.
    - We bypassed the limitation of mixing Search+Tools by isolating Search in
      its own agent and wrapping it.