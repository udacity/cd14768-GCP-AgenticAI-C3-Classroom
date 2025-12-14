# cd14768 - Lesson 6 - demo

Implementing Database Interaction with MCP

- In this demo, we'll be creating an agent that answers questions from a 
  literary database that contains information about authors and their books. 
  In particular, we will be able to get a list of books by an author, and 
  get a list of books that were published between two years.
- Since this data will be in a Google Cloud MySQL database, we'll
  explore how to securely access the database using the Model Context 
  Protocol (MCP) and the Google MCP Database Toolkit. 
- [Concept] What is MCP and what does it solve?
    - Problem: 
      - Agents often need to access a database
      - LLMs may hallucinate database instructions or may be tricked to 
        issue unsafe commands
    - General solution:
      - We've seen how we can use tools to implement our business logic
      - Typically, these tools are functions that we write
    - Explain MCP: 
      - A standard for connecting AI to systems.
      - Allows for a "tool server" that provides tools that an agent can 
        incorporate and a way to discover what tools and other resources the 
        server provides.
      - Allows for isolating authentication away from the agent and LLM.
      - Typically runs on the same machine as the client agent, but can run 
        elsewhere if it makes sense to do so.
    - Explain Database Toolkit: 
      - A "bridge" that translates tool calls into safe, pre-defined SQL.
      - Allows us to define how we are providing information separate from 
        the agent, which just needs to know the tool and what parameters it 
        requires.
      - All we need to do is define the connection, the parameters for each 
        tool, and the query that will run for each tool. The MCP Toolbox 
        takes care of other issues for us.
- [Setup Walkthrough] Cloud SQL & Toolbox
    - **Cloud SQL**: Show the instance in Google Cloud Console.
        - Mention creating a MySQL instance.
        - Mention creating a restricted user (`toolbox`) for security.
        - Mention authorizing the local IP address.
    - **MCP Toolbox**:
        - Explain that we downloaded the `toolbox` binary.
        - Show the command to run it: `./toolbox --tools-file tools.yaml`.
        - Explain that this server runs locally and handles the DB connection.
- [tools.yaml] The Heart of the Demo
    - **Sources**: 
      - Show the `sources` section connecting to MySQL using env
        vars (`${MYSQL_HOST}`).
      - These named sources are referenced by the tools to know where and 
        how to connect to the database.
    - **Tools**: Walk through the `books-by-author` tool definition.
        - **Kind**: `mysql-sql`.
        - **Parameters**: `author` (string).
        - **Statement**: The actual SQL query `SELECT ... WHERE name LIKE ?`.
        - **Key Takeaway**: This is *safe* because the SQL is fixed; the agent
          only fills in the `?`.
- [agent.py] Connecting the Agent
    - Show `ToolboxSyncClient`.
    - Show `db_client.load_tool("books-by-author")`.
    - Explain: The Python code is clean. It doesn't know about SQL. It just
      imports a tool definition from the running MCP server.
- [agent-prompt.txt] Our instructions
    - Similarly, the instructions prompt doesn't make any reference to 
      either the MCP server or the database. It just needs to reference the 
      tools. 
- running the code
    - **Terminal 1**: Ensure the MCP server is running (`./toolbox ...`).
    - **Terminal 2**: Start `adk web` (`cd lesson-06-database-interaction` then
      `adk web`).
    - Navigate to the URL.
- demonstration
    - Prompt: "What books did Jane Austen write?"
    - **Walkthrough**:
        - Agent sends the question to the LLM, including what tools are 
          available.
        - LLM says to use the `books-by-author` tool with "Jane Austen" as 
          the author parameter.
        - Agent calls tool `books-by-author(author="Jane Austen")`.
        - Request goes to MCP Server.
        - MCP Server executes SQL on Cloud SQL.
        - Results returned to Agent.
        - Agent forwards results to the LLM.
        - LLM replies, and Agent sends to the customer: "Jane Austen wrote 
          'Pride and Prejudice' (1813)..."
- conclusion and summary
    - MCP enables safe, controlled database access.
    - No "Text-to-SQL" risks.
    - Configuration (`tools.yaml`) decouples the data layer from the agent code.
