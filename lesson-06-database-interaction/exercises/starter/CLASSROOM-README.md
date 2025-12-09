# Module 6 Exercise: Creating a Warehouse Management Agent

In this exercise, you will create a secure, database-backed agent for managing
warehouse inventory. You will define SQL tools using the MCP Database Toolkit to
allow the agent to add products, check stock, and importantly, log all actions
to an audit table.

---

## Overview

### What You'll Learn

You will learn how to build an agent that performs CRUD (Create, Read, Update,
Delete) operations on a relational database in a controlled and safe manner.
Specifically, you will focus on implementing an audit trail, a critical
requirement for enterprise applications.

Learning objectives:

- Define SQL `INSERT` and `UPDATE` tools in `tools.yaml`.
- Configure an ADK agent to use multiple database tools.
- Implement an audit logging mechanism via a dedicated tool.
- Craft prompts that enforce business rules (like "always log an audit record").

### Prerequisites

- Basic understanding of SQL.
- A Google Cloud Project with billing enabled.
- The `gcloud` and `mysql` CLI tools installed.
- The MCP Database Toolkit installed (download instructions are part of the
  setup).

---

## Understanding the Concept

### The Problem

Managing inventory requires precision and accountability. If an agent changes
the stock level of a high-value item, we need to know *who* changed it, *when*,
and *why*. Simply giving an agent `UPDATE` access isn't enough; we need to
enforce a process where every change is accompanied by an audit log entry.

### The Solution

We will use the **MCP Database Toolkit** to define specific, safe tools:

1. **`add_product`**: Inserts a new row into the `products` table.
2. **`get_product`**: Reads from the `products` table.
3. **`update_product_stock`**: Updates the `stock_quantity` in `products`.
4. **`log_audit`**: Inserts a record into the `audit_log` table.

By defining these as separate tools, we can instruct the LLM (via the prompt) to
*always* call `log_audit` whenever it calls `add_product` or
`update_product_stock`. This moves the business logic (audit compliance) into
the agent's reasoning layer while keeping the data access layer (SQL) simple and
secure.

### How It Works

1. **Database Setup**: You run the `warehouse_database.sql` script to create the
   tables (`products` and `audit_log`).
2. **Tool Definition**: You edit `tools.yaml` to map tool names to SQL
   statements.
3. **Agent Logic**: You write a prompt telling the agent: "You are a warehouse
   manager. Every time you change stock, you must also log it."
4. **Execution**: When a user says "Add 10 widgets", the agent effectively
   performs a multi-step operation: calls `add_product` AND calls `log_audit`.

---

## SETUP INSTRUCTIONS

To run this exercise, you must set up your Google Cloud environment and the MCP
Database Toolkit.

### 1. Setup Google Cloud SQL

If you do not already have a MySQL instance:

1. In the Google Cloud Console, go to **SQL**.
2. Click **Create Instance** -> **MySQL**.
3. Select **Enterprise** edition (Sandbox preset is fine for exercises).
4. Set the ID, root password, and select region **us-central1** (or your
   preferred region).
5. In "Customize your instance", select a minimal machine type (e.g., **Shared
   core** -> **1 vCPU**).
6. Click **Create Instance**.
7. Once created, note the **Public IP address**.
8. Add this IP to your `.env` file as `MYSQL_HOST`.

### 2. Setup MCP Database Toolkit

1. Download the latest release of the **Google GenAI Toolbox** (MCP server) for
   your platform from
   the [official documentation](https://googleapis.github.io/genai-toolbox/getting-started/introduction/)
   or GitHub releases.
2. Make the binary executable (e.g., `chmod +x toolbox`).

### 3. Database Initialization

1. Connect to your database: `mysql -h <MYSQL_HOST> -u root -p`.
2. Run the provided SQL script to set up the schema:
   ```sql
   source docs/warehouse_database.sql;
   ```
3. Ensure your database user (e.g., `toolbox`) has permissions:
   ```sql
   GRANT SELECT, INSERT, UPDATE ON warehouse.* TO 'toolbox'@'%';
   FLUSH PRIVILEGES;
   ```

### 4. Configure Environment

1. Copy `.env-sample` to `.env`.
2. Update `MYSQL_HOST`, `MYSQL_USER`, and `MYSQL_PASSWORD` with your
   credentials.
3. Update `GOOGLE_CLOUD_PROJECT`.

### 5. Run MCP Server

1. Open a terminal in the starter directory.
2. Export your env vars: `export $(grep -v '^#' .env | xargs)`.
3. Run the toolbox: `./toolbox --tools-file tools.yaml --port 5001`.
4. If necessary, update the `.env` file to include the URL of the MCP server

---

## EXERCISE INSTRUCTIONS

### Your Task

Complete the warehouse agent by defining the necessary SQL tools and configuring
the agent to use them.

1. **Define Tools in `tools.yaml`**:
    * `add_product`
    * `get_product`
    * `update_product_stock`
    * `log_audit`
    * *Note: Pay attention to parameter names and types!*

2. **Configure Agent in `agent.py`**:
    * Load all four tools using `db_client.load_tool(...)`.
    * Add them to the `tools` list in the `Agent` constructor.

3. **Write Agent Prompt in `agent-prompt.txt`**:
    * Instruct the agent that it is a warehouse manager.
    * **Crucial**: Make sure that every activity is logged using the 
      `log_audit` tool.

### Requirements

1. The agent must be able to add new products.
2. The agent must be able to look up product details (to get the `product_id`
   for updates).
3. The agent must be able to update stock levels.
4. The agent must create an audit log entry for every add or update operation.

### Repository Structure

```
.
├── __init__.py
├── agent-prompt.txt      # (Your task) Instructions enforcing audit logging.
├── agent.py              # (Your task) Register the tools.
├── tools.yaml            # (Your task) Define the SQL for each tool.
├── README.md             # Overview.
├── .env-sample           # Configuration.
└── docs/
    └── warehouse_database.sql # Schema script.
```

### Starter Code

**`tools.yaml`**:

```yaml
tools:
# TODO: Define 'add_product' tool
# ...
```

**`agent.py`**:

```python
# ...
tools = [
  # TODO: Load the tools you defined in tools.yaml
]
# ...
```

### Expected Behavior

**Running the agent:**
Ensure the `toolbox` server is running in one terminal. (See above)

Then, in another terminal, run the adk web environment:

```bash
adk web
```

**Example usage:**

```text
Human: "Add a new product: 'Super Widget' costing $19.99 with 100 in stock."
Agent: "I have added 'Super Widget' to the inventory and logged the transaction."
```

*Verification*:
Check the database:

```sql
SELECT *
FROM products
WHERE name = 'Super Widget';
SELECT *
FROM audit_log; -- Should show an 'add_product' action
```

```text
Human: "Update the stock of 'Super Widget' to 150."
Agent: "I have updated the stock for 'Super Widget' (ID: 1) to 150 and logged the audit trail."
```

### Implementation Hints

1. **Parameter Matching**: Ensure the parameter names in `tools.yaml` (e.g.,
   `product_id`) exactly match what the LLM will try to infer. Clear
   descriptions help.
2. **Sequential Actions**: For the update, the agent might need to call
   `get_product` first to find the `product_id`, then `update_product_stock`,
   then `log_audit`. Your prompt should encourage this logical flow.
3. **Audit Details**: The `details` parameter for `log_audit` is free-text. The
   agent can use it to describe *why* the change happened or what the old value
   was.

---

## Important Details

### Best Practices

- **Separation of Duties**: The `audit_log` table should ideally be read-only
  for the agent (except for inserts), preventing it from tampering with history.
  In a real production setup, you would enforce this with database permissions.
- **Atomic Transactions**: In a perfect world, the update and the audit log
  would happen in a single database transaction. Here, the agent coordinates
  them. If the agent fails after the update but before the log, the audit trail
  is incomplete. This is a trade-off of agent-orchestrated logic vs. database
  triggers.

### Common Errors

**Error**: `OperationalError: (1048, "Column 'product_id' cannot be null")`

- **Cause**: The agent tried to call `update_product_stock` or `log_audit`
  without knowing the `product_id`.
- **Solution**: Prompt the agent to "Find the product details first" before
  updating.

**Error**: Agent says "I can't do that".

- **Cause**: The tool definitions in `tools.yaml` might be invalid or not loaded
  in `agent.py`.
- **Solution**: Check the console output of the MCP server for errors when
  loading the YAML.
