## Module 1: Implementing Agent Tool Usage with ADK and Vertex AI Gemini Function Calling

### Core Module Primary Learning Objective

Explain how LLM-based agents use external tools (e.g.; Web Search; Database;
APIs; Calculators) to expand their capabilities and interact with real-world
systems; including concepts like function calling and the role of prompt/output
parsing.

### Core Topics or Exercises

Why Tools? Sample Scenario; Common Tools: Web Search; Database; APIs;
Calculators; Functions: Prompt & Output Parsing; Functions: Fine-tuning
Process & Serving layer; Function Calling (FC); Gemini Function Calling
mechanism.

### Google Module Primary Learning Objective

Apply tool usage for LLM-based agents by demonstrating Gemini's function calling
capabilities and integrating pre-built or custom tools within the Agent
Development Kit (ADK).

### Google Additional Learning Objectives

Learn ADK's \`Tool\` interface; Register and use tools with ADK agents; Parse
tool responses.

### Google Topics or Exercises

Demo: Using Vertex AI Gemini function calling with the Vertex AI SDK; Create and
use a custom ADK \`Tool\` (e.g., a simple calculator or API call); Integrate
pre-built ADK tools if available.

### Demo: Weather Tools

#### Summary

Multiple tools to illustrate different weather conditions to return and how the
ADK will use multiple tools to derive an answer

#### Features:

* Tool function definitions
* Synthetic results (we are not doing API calls)
* Loop through relevant tools to collect the answer

#### Google Specific Features:

* Examine how the different models perform to handle tools

### Exercise: Calculator Tools

#### Summary

Build multiple tools to do different mathematical calculations

#### Features:

* Tool function definitions for each major operation (addition, subtraction,
  multiplication, division)
* Multiple parameters
* ADK loops through relevant tools to build the answer

#### Google Specific Features:

* Explore how the different models perform to handle tools

---

## Module 2: Implementing Structured Outputs with Vertex AI Gemini and Pydantic

### Core Module Primary Learning Objective

Understand the importance and methods for developing prompts that produce
structured; machine-readable outputs (e.g.; JSON; complex objects); including
the use of Pydantic models for type enforcement and fail-safe design, focusing
on Gemini's capabilities.

### Core Topics or Exercises

Why output structure? Sample Scenario; Prompt & Output Parser (naive); Gemini's
native JSON mode and function calling for structured data; Types: Int; Bool;
Datetime; Complex Objects; Pydantic Models for schema definition and validation
with Gemini outputs; Fail-safe design.

### Google Module Primary Learning Objective

Develop prompts and leverage Vertex AI Gemini's capabilities (JSON mode or
function calling with schema) to produce structured JSON outputs, validated with
Pydantic models, for downstream processing.

### Google Additional Learning Objectives

Use Pydantic to define the desired output schema for Gemini; Configure Gemini
calls to return structured JSON.

### Google Topics or Exercises

Demo: Using Gemini's JSON mode; Defining a Pydantic model and using it with
Gemini's function calling to enforce a structured JSON response; Parsing and
validating the output.

### Demo: Named Entity Recognition (NER)

#### Summary

We’ll use features of Gemini and ADK to take a human, fuzzy, plain text input
and turn it into structured output as part of a tool to identify instructions
for a hypothetical robot.

#### Features:

* Pydanitc structures
* Required and optional attributes
* Different attribute types
* Enumerated values

#### Google Specific Features:

* ADK output\_schema

### Exercise: Information summarizer

#### Summary

You will use features of Gemini and ADK to summarize a customer service feedback
paragraph, identifying specific information that was provided

#### Features:

* Pydantic structures
* Required and optional attributes
* Different attribute types
* Enumerated values

#### Google Specific Features:

* ADK output\_schema

---

## Module 3: Implementing Agent State Management with ADK (In-Memory and Persistent)

### Core Module Primary Learning Objective

Understand state management techniques to track agent context and progress
across interactions; including the concept of state machines; execution loops (
tracking task progress; inputs/outputs; tool usage); and state schemas; and how
ADK supports this.

### Core Topics or Exercises

Difference between stateless and stateful systems. LLMs are stateless; ADK
\`Session\` and \`State\` objects for managing conversational and task-specific
state; State Machines: Process runs \-\> carries local state \-\> ends \-\>
state gone; Execution Loop. During execution: Task progress; Current inputs;
outputs; Tool usage; State Schemas.

### Google Module Primary Learning Objective

Apply state management techniques using ADK's \`Session\` and \`State\` services
to track agent context and progress, demonstrating both in-memory and persistent
state using Google Cloud databases.

### Google Additional Learning Objectives

Explore \`InMemorySessionService\` and \`DatabaseSessionService\` (e.g., with
Firestore or Cloud SQL) in ADK.

### Google Topics or Exercises

Demo: Design a mini state machine within an ADK agent; Use ADK \`Session\` and
\`State\` for in-memory state tracking; Configure and use ADK's
\`DatabaseSessionService\` with Firestore or Cloud SQL for persistent state
management across agent interactions.

### Demo: State Machines with Transitions

#### Summary

We will explore state machines in general and see how the ADK can manage state
in a single request with a straightforward state machine that transitions
between various colors.

#### Features:

* Reading and writing request state inside a tool with \`Session\` and \`State\`

#### Google Specific Features:

* Working with the \`InMemorySessionService\`
* Observing how state is shown in the \`adk web\` tool

### Exercise: Implement Agent State

#### Summary

By default, if your agent executes a tool, and that tool call fails, the agent
will give up. You will implement a state machine inside ADK to help an agent
manage tool calls that may generate errors. Tool call retry is an important
feature when implementing robust production agents

#### Features:

* Reading and writing request state inside a tool with \`Session\` and \`State\`
* Handling error conditions

#### Google Specific Features:

* Working with the \`InMemorySessionService\`
* Observing how state is shown in the \`adk web\` tool

---

## Module 4: Implementing Short-Term Agent Memory with ADK and Google Cloud Memorystore

### Core Module Primary Learning Objective

Explain how agent memory (short-term vs. long-term; in-application vs.
persisted) supports consistency across multiple interactions; discuss various
strategies (Conversation History; Sliding Window; Simple Summarization) and
their limitations; and how ADK's \`MemoryService\` addresses this.

### Core Topics or Exercises

“Memory” as an abstraction; Types of memory: In-application (ephemeral) vs
persisted (durable); Short-term vs Long-term memory supported by ADK's
\`MemoryService\`; Strategies: Conversation History; Sliding Window; Simple
Summarization; Limitations: context windows; token costs; performance; State vs
Session memory.

### Google Module Primary Learning Objective

Implement basic short-term agent memory mechanisms; such as conversation history
or a sliding window; using ADK's in-memory capabilities or integrating with
Google Cloud Memorystore (Redis) for low-latency session memory.

### Google Additional Learning Objectives

Utilize ADK \`Session\` for conversational history; Explore custom integration
with Memorystore for more complex short-term memory needs.

### Google Topics or Exercises

Demo: Building short-term memory using ADK's \`Session\` data; Implement a
sliding window mechanism within an ADK agent; (Optional) Example of connecting
an ADK agent to Memorystore for session data storage and retrieval.

### Demo: Using Session and User-based memory

#### Summary

We will build an agent that takes user commands to set preferences for the
maximum number of questions to ask, and then asks questions that many times. The
preferences will be saved between sessions (using “user:property” state names),
while the task itself is session based (using regular “property” state names).
We’ll discuss the difference between these state property names and the “temp:”
state property name we used in the previous module.

#### Features:

* Using \`Session\` and \`State\` inside a tool
* Using user: and session scoped state

#### Google Specific Features:

* Working with \`InMemorySessionService\`, \`DatabaseSessionService\`, or
  \`VertexAISessionService\`

### Exercise: Using Session state for trip planning

#### Summary

You will build a travel agent that specializes in multi-step travel planning.
Your agent will have a conversation with the customer to determine each stage
where they want to go to, adding it to the itinerary in state each step. When
the customer says it is done, it creates an itinerary. The customer can set
their “home” location in their preferences and, if they do not specify a default
starting location, it will use this home location.

#### Features:

* Using \`Session\` and \`State\` inside a tool
* Using user: and session scoped state
* Including state in instructions

#### Google Specific Features:

* DatabaseSessionService or VertexAiSessionService

####  

---

## Module 5: Implementing API Integration for Agents with ADK, Python, and Google Cloud Secret Manager

### Core Module Primary Learning Objective

Understand how external API integrations expand agent functionality and
incorporate live data into agent workflows; including concepts of tool
selection; function calling; and attaching LLM results to external data, with
examples like weather or finance APIs. Focus on secure API key management.

### Core Topics or Exercises

API integration in Python; Attaching LLM results to external data; Gemini
Function Calling for API interaction; Tool Selection; API Integration for
agentic workflows; weather/finance API examples; Secure handling of API keys
using services like Google Cloud Secret Manager.

### Google Module Primary Learning Objective

Apply external API integrations to expand agent functionality by integrating a
simple public API into an ADK agent using Python and ADK Tools, managing API
keys securely with Google Cloud Secret Manager.

### Google Additional Learning Objectives

Store and retrieve API keys from Secret Manager; Make API calls from an ADK
Tool; Process and use API data in agent responses.

### Google Topics or Exercises

Integrate a simple public API (e.g., weather, currency conversion) as an ADK
Tool; Securely manage its API key using Google Cloud Secret Manager; Incorporate
the data into a final answer or piece of code generated by the agent.

### Demo:

#### Summary

We will look at how we can use the Google Places API to convert place names into
addresses and lat-long coordinates, and then use this data and the Google ~~
Distance Matrix~~ Routes API to get the distance between these locations. Since
these APIs require an API Key, we’ll get the key and store it in the Google
Cloud Secret Manager.

#### Features:

* Multiple tools, including one that uses an API

#### Google Specific Features:

* Google Cloud Secret Manager
* Using Application Default Credentials
* Google Places API
* Google ~~Distance Matrix~~ Routes API

### Exercise: Using a Currency Exchange API

#### Summary

You will get an API Key at exchangerate-api.com, save it in the Google Cloud
Secret Manager, and use it in a tool. The agent built around the tool will let
the customer convert the value of one currency to another.

#### Features:

* Tools that use API keys

#### Google Specific Features:

* Google Cloud Secret Manager
* Using Application Default Credentials

---

## Module 6: Implementing Database Interaction for AI Agents with ADK and Google Cloud Databases

### Core Module Primary Learning Objective

Understand how agents can query and update databases (e.g., Google Cloud SQL,
Spanner, Firestore, BigQuery, Vector Search) in retrieval-augmented tasks or for
persistent storage, including generating SQL/NoSQL queries and using retrieved
data.

### Core Topics or Exercises

Generating SQL or NoSQL commands (potentially with LLM assistance); Retrieving
data and using it in conversation or agent logic; Storing agent state or
knowledge in databases; Overview of Google Cloud database options suitable for
agents (Cloud SQL, Spanner, Firestore, BigQuery for analytics, Vertex AI Vector
Search for RAG).

### Google Module Primary Learning Objective

Configure ADK agents to query and update Google Cloud databases (e.g., Cloud SQL
for relational data, Firestore for NoSQL document data) for various agentic
tasks like data retrieval or state persistence.

### Google Additional Learning Objectives

Use ADK tools or custom Python code within agents to interact with databases;
Handle connection management and data parsing.

### Google Topics or Exercises

Build an ADK agent that queries a sample Cloud SQL (PostgreSQL/MySQL) database
to retrieve information; Implement an ADK agent that reads/writes data to
Firestore for storing user preferences or agent state; Show how relevant data is
stored or retrieved for further usage by the agent.

### Demo: Accessing Data from Databases

#### Summary

We will see how we can use the Google MCP Database Toolkit to access a Google
Cloud SQL for MySQL database. We’ll explore the security implications of using
an MCP server to access the database and why this is an important feature for
both authorization and limiting how data is controlled.

#### Features:

* Using MCP servers
* MCP server configuration via environment variables
* Database access that prevents data injection and why this is important

#### Google Specific Features:

* Google Cloud SQL for MySQL
* Using MCP Database Toolkit to access data

### Exercise: Creating Warehouse Management Agent

#### Summary

You will create an agent that manages the inventory database for a warehouse.
Due to the value of the products, there needs to be an audit trail for all
transactions, and this audit database cannot be altered. You will need to create
tools that reflect the CRUD nature of database operations, but with
restrictions.

#### Features:

* Using MCP servers
* Database access that enforces security constraints
* Using tools to create audit logs

#### Google Specific Features:

* Google Cloud SQL for MySQL
* Using MCP Database Toolkit to access and update data

---

## Module 7: Implementing Web Search Agents with ADK and ~~Google Custom Search
API~~ Grounding with Google Search Tool

### Core Module Primary Learning Objective

Understand how to develop an agent that performs web searches via an API (e.g.,
Google Custom Search JSON API), filters and merges external search results, and
integrates them into LLM responses.

### Core Topics or Exercises

Calling a web API from an agent loop; Filtering and merging external search
results; Example using Google Custom Search JSON API; Ethical considerations and
limitations of web scraping/searching.

### Google Module Primary Learning Objective

Develop an ADK agent that performs web searches via the Google Custom Search
JSON API, integrates results into LLM responses generated by Vertex AI Gemini,
and uses ADK tools for implementation.

### Google Additional Learning Objectives

Implement an ADK tool for Google Search; Process search results and provide them
as context to Gemini for summarization or answering questions.

### Google Topics or Exercises

Set up a Google Custom Search Engine and API key; Create an ADK tool to call the
Google Custom Search JSON API; Collect the results and pass them to Gemini via
an ADK agent for summary or analysis.

### Demo: Grounding data with Google Search

#### Summary

We’ll look at why we need to ground our results in factual data, not just the
training data for an LLM model, and how we can prompt Gemini and the ADK to do
so almost automatically.

#### Features:

* Google Search

#### Google Specific Features:

* Grounding with Google Search tool

### Exercise: Using other tools with Google Search

#### Summary

Just getting data isn’t always enough \- sometimes it depends what you can do
with it. After we have gotten data from Google Search, how can we use other
tools. You will use the Grounding with Google Search tool to retrieve current
financial information and then a custom tool you create to do some calculations
and return it in a structured format.

#### Features:

* Google Search

#### Google Specific Features:

* ADK \`AgentTool\` class
* Google Search

---

## Module 8: Implementing Single-Agent RAG with ADK and Vertex AI Search/RAG Engine

### Core Module Primary Learning Objective

Understand how a single RAG agent parses a query; forms retrieval requests to a
vector database (e.g., Vertex AI Vector Search via RAG Engine or ADK's
MemoryService); integrates results; produces an answer with an LLM; and handles
re-retrieval if the first result is suboptimal.

### Core Topics or Exercises

Combining retrieval and generation in a single agent loop; Handling re-retrieval
if the first result is suboptimal; Show how a single agent can do everything:
parse the query; form retrieval requests; integrate results; produce an answer
using Vertex AI Search/RAG Engine components.

### Google Module Primary Learning Objective

Build a RAG agent using ADK's \`VertexAiRagMemoryService\` or by directly
integrating with Vertex AI RAG Engine/Search. The agent will retrieve relevant
documents and produce an answer using Vertex AI Gemini.

### Google Additional Learning Objectives

Ingest data into Vertex AI Search/RAG Engine; Configure ADK agent to query the
RAG setup; Confirm agent can re-check if initial retrieval is insufficient.

### Google Topics or Exercises

Develop a Python script using ADK that leverages \`VertexAiRagMemoryService\` (
backed by Vertex AI RAG Engine/Search) for context retrieval from a sample
document set; Use Gemini for generating answers based on retrieved context; Test
re-retrieval logic.

### Demo: Using Vertex AI Search with Unstructured Data

#### Summary

We will explore how to load data into Vertex AI Search from a Google Cloud
Storage bucket and then the various options for accessing this data through a
tool in ADK and the Google Cloud Platform library.

#### Features:

* Answers grounded by documents (In this case, public financial documents.)

#### Google Specific Features:

* Loading and updating corpus data from Google Cloud Storage
* Querying through the Vertex AI Search “discoveryengine” library

### Exercise: A Simple Superhero FAQ Agent

#### Summary

You’ll use Gemini to create several documents about various (brand new, non
trademarked) superheroes. After uploading these documents to GCS, you’ll load
them into Vertex AI Search and build an agent to answer questions about them.

#### Features:

* Answers grounded by documents that have been created by the student to make
  sure they do not exist in Gemini’s training data.

#### Google Specific Features:

* Google Cloud Storage
* Vertex AI Search
* GCP “discoveryengine” library

---

## Module 9: Implementing Long-Term Agent Memory with ADK and VertexAI Agent Engine Memory Bank
~~Google Cloud Databases/Vertex AI~~

### Core Module Primary Learning Objective

Understand methods for updating; pruning; and managing an agent’s long-term
memory (e.g., using ADK's MemoryService with Vertex AI RAG Engine for vector
data, or Cloud SQL/Spanner for structured data) to maintain context over
extended sessions while balancing performance and context length; including
techniques like time-based removal and relevance filtering.

### Core Topics or Exercises

Integrate memory management (updates; pruning; and weighting) so that the agent
stays relevant; Techniques for memory updating; pruning; and optimization with
ADK MemoryService; Balancing performance and context length; Time-based removal;
relevance filtering; size limitations.

### Google Module Primary Learning Objective

Develop methods for updating and managing an agent’s long-term memory using
ADK's \`MemoryService\` (with Vertex AI RAG Engine for knowledge/vector memory,
or Google Cloud SQL/Spanner for structured persistent memory) to maintain
context over extended sessions.

### Google Additional Learning Objectives

Demonstrate how to prune or reorder memory for better performance; Implement
storage and retrieval strategies for different types of long-term memory.

### Google Topics or Exercises

Experiment with storing conversation summaries or key facts in Cloud SQL/Spanner
via ADK; Use \`VertexAiRagMemoryService\` for managing and querying a knowledge
base in Vertex AI RAG Engine; Demonstrate techniques for updating or refreshing
this long-term memory.

### Demo: Saving Conversations with Memory Bank

#### Summary

We’ll explore the hooks necessary to save a copy of each session with Vertex AI
Agent Engine Memory Bank and why we might want to do so. We’ll see how Memory
Bank summarizes our conversations and how they get incorporated into future
conversations.

#### Features:

#### Google Specific Features:

* Vertex AI Agent Engine Memory Bank
* ADK session event hooks

### Exercise: Searching Conversations with Memory Bank

#### Summary

How can we use the Memory Bank in conjunction with other tools, such as the
Google Search tool? Combine Grounding with Google Search and Memory bank to
create a research assistant that keeps track of what you’re talking about in
between sessions.

#### Features:

* Research assistant

#### Google Specific Features:

* Grounding with Google Search
* Vertex AI Agent Engine Memory Bank

---

## Module 10: Implementing Agent Evaluation with ADK and Google Cloud Tracing

### Core Module Primary Learning Objective

Understand how to evaluate the performance of AI agents across different
dimensions (final response; single step; trajectory) and the metrics used for
iterative evaluation, with a view towards Google Cloud tools.

### Core Topics or Exercises

Metrics: final response; single step; trajectory; Iterative evaluation of
agents; Introduction to Vertex AI Model Evaluation Service for custom models and
potential application to agent components.

### Google Module Primary Learning Objective

Evaluate the performance of AI agents across different dimensions by
implementing evaluation scripts using ADK's evaluation utilities and potentially
integrating with Vertex AI Model Evaluation Service for more complex evaluations
or tracking.

### Google Additional Learning Objectives

Define metrics for agent performance; Write Python scripts using ADK to run
agents against test cases and compute metrics; Explore logging evaluation data
to Vertex AI.

### Google Topics or Exercises

Implement evaluation scripts in Python using ADK's built-in evaluation
utilities (if available) or custom scripts; Define metrics (e.g., task
completion rate, response accuracy, tool usage correctness); (Optional) Log
evaluation results for analysis, potentially using Vertex AI Model Evaluation
Service for components that can be framed as models.

### Demo: Observability with the ADK

#### Summary

As part of evaluating any production service, we need to be able to capture that
information. While we can explore this during testing using the \`adk web\`
visual interface, in production we’ll need to use more sophisticated
observability tools. We’ll see how to configure our ADK applications to send
telemetry data to these tools and how we can use the Google Cloud Console to
explore them.

#### Features:

* Observability

#### Google Specific Features:

* Google Cloud Tracing
* Google Cloud Logging

---

