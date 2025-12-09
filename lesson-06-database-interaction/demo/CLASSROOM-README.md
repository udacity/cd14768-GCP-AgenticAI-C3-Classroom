# Module 6: Implementing Database Interaction for AI Agents with ADK and Google Cloud Databases

This demo showcases how to enable an ADK agent to interact securely with a
Google Cloud SQL database using the Google MCP Database Toolkit. We will explore
how to set up the Model Context Protocol (MCP) server, configure database access
via a `tools.yaml` file, and query data using natural language.

---

## Overview

### What You'll Learn

You will learn how to bridge the gap between an LLM agent and a relational
database. Instead of giving the LLM direct access to execute arbitrary SQL (a
huge security risk), we will use the MCP Database Toolkit to expose safe,
parameterized tools that the agent can call.

Learning objectives:

- Understand the role of the Model Context Protocol (MCP) in agent
  architectures.
- Set up and configure the Google MCP Database Toolkit.
- Connect an ADK agent to a Google Cloud SQL (MySQL) instance.
- Define safe SQL tools using a declarative `tools.yaml` configuration.

### Prerequisites

- Basic understanding of Python.
- Basic understanding of ADK.
- Basic understanding of SQL.
- A Google Cloud Project with billing enabled.
- The `gcloud` and `mysql` CLI tools installed.
- The MCP Database Toolkit installed (download instructions below).

---

## Understanding the Concept

### The Problem

Agents often need to access structured business data stored in databases.
However, letting an LLM write SQL queries directly (`Text-to-SQL`) can be
dangerous (SQL injection risks, hallucinated table names) and difficult to
control (giving the LLM too much access).

Agents typically use tools, written as function calls in the code, to bridge 
this gap. Tools allow us to code the business logic with clearly defined 
inputs from and outputs to the LLM.

### The Solution

The **Model Context Protocol (MCP)** is an open standard that allows developers
to build servers (often running on the same machine as the agent or client 
that uses them) that expose data and functionality to AI models in a
standardized way. The **Google MCP Database Toolkit** is a specific
implementation that allows you to define "tools" (pre-written, parameterized SQL
queries) in a YAML file. The MCP server runs locally or in the cloud, connects
to your database, and executes these safe queries when requested by the agent.

### How It Works

1. **Configuration (`tools.yaml`)**: You define specific tools (e.g.,
   `books-by-author`) and the exact SQL query they execute. You also define
   parameters (like `author_name`) that the LLM needs to provide.
2. **MCP Server**: You run the MCP Database Toolkit server, pointing it to your
   `tools.yaml` and your database credentials.
3. **ADK Agent**: The agent connects to the running MCP server and loads the 
   tool configuration for specific tools (such as `books-by-author`), getting 
   their definitions and parameters. It then includes this tool definition 
   when calling the LLM.
4. **Interaction**: When a user asks "What books did Jane Austen write?", 
   the LLM instructs the agent to call the `books-by-author` tool with 
   parameter `Jane Austen`. The MCP server executes the pre-defined SQL 
   safely and returns the results. 

It is important to understand that we don't write code for the agent to 
specifically call either the MCP server or the database. We are making a 
tool available, and the LLM may instruct the agent to call this tool and 
provide the results.

### Key Terms

**Model Context Protocol (MCP)**: A standard for connecting AI models to
external data and tools. It decouples the model from the specific implementation
of the tool.

**MCP Database Toolkit**: A tool provided by Google that implements an MCP
server specifically for database interactions. It emphasizes security by using
pre-defined SQL statements.

**`tools.yaml`**: The configuration file where you define your data sources (
database connection info) and the specific tools (SQL queries) you want to
expose to the agent.

---

## SETUP INSTRUCTIONS

### 1. Setup Google Cloud SQL

If you do not already have a MySQL instance:

1. In the Google Cloud Console, go to **SQL**.
2. Click **Create Instance** -> **MySQL**.
3. Select **Enterprise** edition (Sandbox preset is fine for demos).
4. Set the ID, root password, and select region **us-central1** (or your
   preferred region).
5. In "Customize your instance", select a minimal machine type (e.g., **Shared
   core** -> **1 vCPU**).
6. Click **Create Instance**.
7. Once created, note the **Public IP address**.
8. Add this IP to your `.env` file as `MYSQL_HOST`.

**Database Initialization**:
You need to create the database and tables. Connect to your instance using the
`mysql` CLI:

```bash
mysql -h <MYSQL_HOST> -u root -p
```

Then run the SQL commands found in `docs/demo_database.sql` (or similar) to
create the `demo` database and `books` tables. You also need to create a user (
e.g., `toolbox`) and grant it `SELECT` permissions on the `demo` database.

### 2. Setup MCP Database Toolkit

1. Download the latest release of the **Google GenAI Toolbox** (MCP server) for
   your platform from
   the [official documentation](https://googleapis.github.io/genai-toolbox/getting-started/introduction/)
   or GitHub releases.
2. Make the binary executable (e.g., `chmod +x toolbox`).

### 3. Run the MCP Server

1. Navigate to the demo directory containing `tools.yaml`.
2. Export your database credentials from your `.env` file so the server can read
   them.
   ```bash
   export $(grep -v '^#' .env | xargs)
   ```
3. Run the toolbox server:
   ```bash
   ./toolbox --tools-file tools.yaml --port 5001
   ```
4. Update `TOOLBOX_URL` in your `.env` file to `http://127.0.0.1:5001`.

---

## CODE WALKTHROUGH

### Repository Structure

```
.
├── __init__.py           # Package initialization.
├── agent-prompt.txt      # Agent instructions.
├── agent.py              # Agent configuration using ToolboxSyncClient.
├── tools.yaml            # (Crucial) Definition of SQL tools and database connection.
├── README.md             # Setup instructions.
├── requirements.txt      # Dependencies.
└── docs/                 # SQL scripts for setting up the database.
```

### Step 1: The Configuration (`tools.yaml`)

This file is the heart of the integration. It has two sections: `sources` and
`tools`.

**Sources**: Defines how to connect to the database. It uses environment
variables (`${MYSQL_HOST}`) for security. In this case, it creates a 
source named "demo" that we will reference later, and we specify that this 
is a mysql database that we're connecting to. The Database Toolkit offers 
many kinds of data sources.

```yaml
sources:
  demo:
    kind: mysql
    host: ${MYSQL_HOST}
    # ... other connection details ...
```

**Tools**: Defines the capabilities exposed to the agent. In this case, 
we're defining a tool named "books-by-author".

```yaml
tools:
  books-by-author:
    kind: mysql-sql
    source: demo
    description: Get the books written by a specific author
    parameters:
      - name: author
        type: string
        description: The name of the author we're looking for
    statement:
      SELECT b.title, a.name, b.publication_year
      FROM books b JOIN authors a ...
      WHERE LOWER(a.name) LIKE CONCAT('%', LOWER(?), '%')
```

**Why this is good**:

* **Security**: The SQL is hardcoded. The agent can only provide the
  *parameter* (`?`), preventing SQL injection attacks.
* **Control**: The agent can *only* run this specific query. It cannot
  `DROP TABLE` or access tables you haven't explicitly exposed.

### Step 2: The Agent (`agent.py`)

The agent uses the `ToolboxSyncClient` to connect to the running MCP server.

```python
from toolbox_core import ToolboxSyncClient

# Connect to the local MCP server
toolbox_url = os.environ.get("TOOLBOX_URL", "http://127.0.0.1:5000")
db_client = ToolboxSyncClient(toolbox_url)

# Load specific tools defined in tools.yaml
tools = [
  db_client.load_tool("books-by-author"),
  db_client.load_tool("books-in-year-range"),
]

root_agent = Agent(..., tools=tools)
```

**Key Point**: The agent code doesn't know anything about SQL or databases. It
just sees "tools" with descriptions and parameters, treating them exactly like
Python functions.

---

## Important Details

### Best Practices

- **Least Privilege**: Create a specific database user (like `toolbox`) that
  only has `SELECT` permissions on the specific tables needed. Never use the
  `root` user in your `tools.yaml` or `.env`.
- **Environment Variables**: Always use `${VAR_NAME}` syntax in `tools.yaml` for
  sensitive values like passwords and hosts.
- **Tool Descriptions**: Write clear, descriptive `description` fields in
  `tools.yaml`. The LLM uses these to decide which tool to call.

### Common Errors

**Error**: `Connection refused` when connecting to MCP server.

- **Cause**: The `toolbox` binary isn't running, or `TOOLBOX_URL` in `.env`
  points to the wrong port.
- **Solution**: Ensure the server is running and the ports match.

**Error**: Database connection failed.

- **Cause**: Incorrect IP, username, or password in `.env`, or the Cloud SQL
  instance doesn't allow connections from your IP (Authorized Networks).
- **Solution**: Check your `.env` variables. Go to Cloud SQL > Connections >
  Networking and add your current public IP to "Authorized networks".

**Error**: Agent hallucinates a tool or query.

- **Cause**: The agent is trying to guess SQL instead of using the tool.
- **Solution**: Ensure `agent-prompt.txt` clearly instructs the agent to *use
  the provided tools* to answer questions.
