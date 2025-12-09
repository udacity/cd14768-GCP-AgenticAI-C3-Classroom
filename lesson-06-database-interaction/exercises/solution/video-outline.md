# cd14768 - Lesson 6 - exercise

Warehouse Management Agent

- In this solution walkthrough, we'll examine a database-backed agent that
  performs secure inventory updates and enforces an audit trail.
- [Setup Check] Database & Toolbox
    - Verify that MySQL is running (`mysql` command).
    - Verify that the `toolbox` server is running with the solution's
      `tools.yaml`.
- [tools.yaml] Review Tool Definitions
    - **`add_product`**: Show the `INSERT` statement. Note the parameters.
    - **`get_product`**: Show the `SELECT` statement. Explain why this is
      needed (to find IDs).
    - **`update_product_stock`**: Show the `UPDATE` statement.
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
    - This pattern (Restricted Tools + Policy Prompt) is powerful for enterprise
      agents.
