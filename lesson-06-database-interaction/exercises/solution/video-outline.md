# cd14768 - Lesson 6 - exercise

Warehouse Management Agent

- For this exercise, you were asked to create a database-backed warehouse 
  management agent.
  - Warehouse employees could add new products and check and adjust the 
    inventory counts.
  - All activity needed to be logged to an audit log.
- We're using the MCP Database Toolbox since it allows for easy, yet highly 
  restricted, access to the database
- [Setup Check] Database & Toolbox
    - Make sure our database is running and that we have its IP address and 
      the account information we need. 
    - Verify that the `toolbox` server is running with the solution's
      `tools.yaml`.
- [tools.yaml] Review Tool Definitions
    - **`add_product`**: Show the `INSERT` statement. Note the parameters.
    - **`get_product`**: Show the `SELECT` statement. Explain why this is
      needed (to find IDs).
    - **`update_product_stock`**: Show the `UPDATE` statement.
      - Note that the order of parameters is important
      - They are mapped to the ? in the SQL statement in order
    - **`log_audit`**: Show the `INSERT` into the audit table.
    - **Safety**: Reiterate that the agent cannot execute `DROP TABLE` or other
      arbitrary SQL because only these specific tools are defined.
- [agent-prompt.txt] Review Instructions
    - Read the line: "Every transaction must be logged through an audit tool."
    - Explain that this instruction is what binds the `update` action to the
      `audit` action.
- [agent.py] Review Configuration
    - Show how `db_client.load_tool()` imports the definitions from the toolbox.
- running the code
    - start `adk web` in another window (`cd lesson-06-database-interaction`
      then `adk web`)
    - navigate to the URL.
- demonstration
    - Prompt: "Add a new product: 'HyperBeam' costing $500 with 5 in stock."
    - **Walkthrough**:
        - Agent calls `add_product`.
        - Agent calls `log_audit`.
        - Show the tool outputs in the chat.
    - Prompt: "Update HyperBeam stock to 4."
    - **Walkthrough**:
        - Agent might call `get_product` to find the ID of 'HyperBeam'.
        - Agent calls `update_product_stock`.
        - Agent calls `log_audit`.
- conclusion and summary
    - We've built a secure interface to a database.
    - We used the agent to enforce a business process (auditing) that isn't
      strictly enforced by the database itself.
