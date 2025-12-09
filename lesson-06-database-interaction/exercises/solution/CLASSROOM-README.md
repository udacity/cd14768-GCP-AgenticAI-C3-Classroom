# Module 6 Exercise Solution: Warehouse Management Agent

This solution demonstrates a secure, database-backed warehouse management agent.
It uses the MCP Database Toolkit to perform inventory operations while enforcing
an audit trail.

---

## Overview

### What You'll Learn

This solution illustrates how to configure the MCP Database Toolkit to expose
safe SQL tools and how to build an agent that uses these tools to enforce
business logic (audit logging) alongside data modification.

Learning objectives:

- Correctly mapping SQL statements to tools in `tools.yaml`.
- Configuring the agent to load tools from an MCP server.
- Prompting the agent to perform multi-step operations (Update + Log)
  consistently.

### Prerequisites

- A running MySQL database seeded with `warehouse_database.sql`.
- The `toolbox` server running with the solution's `tools.yaml`.

---

## Understanding the Concept

### The Problem

We needed to give an agent the power to modify inventory (a risky operation)
while ensuring accountability. Direct SQL access is unsafe, and relying on the
agent to "just remember" to log changes is brittle without specific tools and
instructions.

### The Solution

1. **Restricted Tools**: We defined specific `INSERT` and `UPDATE` queries in
   `tools.yaml`. The agent cannot execute arbitrary SQL; it can only run these
   pre-approved templates.
2. **Explicit Audit Tool**: We created a `log_audit` tool. This reifies the
   logging requirement into a concrete action the agent can take.
3. **Prompt Engineering**: We instructed the agent that its job *requires*
   logging every change.

---

## CODE WALKTHROUGH

### Repository Structure

```
.
├── __init__.py           # Package initialization.
├── agent-prompt.txt      # Agent instructions enforcing logging.
├── agent.py              # Agent configuration loading MCP tools.
├── tools.yaml            # Definitions of SQL tools.
├── README.md             # Overview.
├── .env                  # Environment config (not checked in).
└── docs/
    └── warehouse_database.sql # Database schema.
```

### Step 1: Tool Definitions (`tools.yaml`)

This is where the safety controls live.

```yaml
tools:
  add_product:
    kind: mysql-sql
    source: warehouse
    description: Adds a new product to the inventory.
    parameters:
      - name: name
        type: string
        description: The name of the product.
      - name: price
        type: float
        description: The price of the product.
      - name: stock_quantity
        type: integer
        description: The initial stock quantity.
    statement:
      INSERT INTO products (name, price, stock_quantity) VALUES (?, ?, ?);

  update_product_stock:
    kind: mysql-sql
    # ...
    statement:
      UPDATE products SET stock_quantity = ? WHERE product_id = ?;

  log_audit:
    kind: mysql-sql
    # ...
    statement:
      INSERT INTO audit_log (product_id, action, details) VALUES (?, ?, ?);
```

**Key Details**: 
- The source defines how we will connect to the database.
- The parameters and description are used in the tool definition for the LLM.
- The `?` placeholders map from the defined parameters to the statement and 
  mean the agent can provide values, but it cannot change the structure of 
  the query.

### Step 2: Agent Configuration (`agent.py`)

The agent code is minimal because the heavy lifting is done by the MCP server.

```python
# Connect to the local MCP server
toolbox_url = os.environ.get("TOOLBOX_URL", "http://127.0.0.1:5000")
db_client = ToolboxSyncClient(toolbox_url)

tools = [
  db_client.load_tool("add_product"),
  db_client.load_tool("get_product"),
  db_client.load_tool("update_product_stock"),
  db_client.load_tool("log_audit"),
]
```

### Step 3: Agent Instructions (`agent-prompt.txt`)

The prompt bridges the gap between the tools.

```text
You are a warehouse management agent.
You have tools that can modify the inventory...
Every transaction must be logged through an audit tool.
```

This instruction ensures that when the agent calls `update_product_stock`, it
follows up with `log_audit`.

### Complete Example

1. **User**: "Update stock for 'Widget' to 50."
2. **Agent (Reasoning)**: "I need the product_id for 'Widget'. Calling
   `get_product`."
3. **Tool (`get_product`)**: Returns `id: 1, name: 'Widget', ...`
4. **Agent (Reasoning)**: "Now I can update. Calling
   `update_product_stock(1, 50)`."
5. **Tool (`update_product_stock`)**: Success.
6. **Agent (Reasoning)**: "I updated data, so I must log it. Calling
   `log_audit(1, 'update', 'Stock set to 50')`."
7. **Tool (`log_audit`)**: Success.
8. **Agent (Response)**: "Stock updated and logged."

---

## Important Details

### Setup Verification

If the agent fails to connect:

1. Check that `toolbox` is running in a separate terminal.
2. Verify `TOOLBOX_URL` in `.env` matches the port `toolbox` is listening on.
3. Ensure the database user credentials in `.env` are correct.

### Best Practices

- **Tool Descriptions**: In `tools.yaml`, the `description` fields are vital.
  For example, `get_product` describes *what* it returns ("details... including
  current inventory"), which helps the agent know it's the right tool for
  lookups.
- **Audit Consistency**: In a real app, you might automate the audit log with
  database triggers to be 100% sure it happens. However, using an agent allows
  for richer, context-aware audit messages (e.g., explaining *why* the change
  was made if the user provided a reason).
