# cd14768 - Lesson 10 - demo

Implementing Agent Evaluation with ADK and Google Cloud Observability

- In this demo, we're going to look at how to use observability tools with 
  Google Cloud Trace and Logging to help us understand what our agents are 
  doing, how well they are performing, and what our customers may be asking 
  our agents to we can setup good evaluation criteria.
  - Evaluation isn't just running pre-made test scripts.
  - True evaluation requires understanding **real-world usage**.
  - What are users actually asking? Where does the agent get confused? Which
    tools are failing?
  - Observability gives us the raw data (logs/traces) to answer these
    questions and continuously improve the agent.
- Observability is big and complicated
  - One could do an entire course on the subject!
  - Sometimes it requires detailed understanding of the internals of your 
    agent or how an agent works with an LLM.
  - We'll take a look at just a few features using a couple of agents as 
    examples.
  - I encourage you to test these principles in your own agents.
- Setup (Prerequisites)
  - Ensure the **Telemetry API** is enabled in your Google Cloud Project.
    - Go to APIs and services
    - If we don't see the Telemetry API listed, we can Enable it using the 
      link on top
    - Select Enable
    - Type name
    - Select it when it comes up
    - In my case it is already enabled, but this is where you can enable it.
  - Configure `.env`:
    - `OTEL_SERVICE_NAME`: Identify your agent (e.g., `adk-weather`).
    - `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true`: 
      **Critical** for seeing what was said.
    - **Warning**: Be careful with `CAPTURE_MESSAGE_CONTENT` in production
      if handling PII/sensitive data.
- [demo-1/agent.py] The Agent Code
  - Show `agent.py`
  - It defines three tools and a prompt.
  - **Key Point**: There is NO special tracing code here.
  - The ADK framework automatically instruments the agent when the environment
    variables are set.
- Running Demo 1
  - Command: `env $(cat demo-1/.env | xargs) adk web --otel_to_cloud`
  - Normally, running `adk web` loads the environment for each agent
  - In this case, the environment needs to be configured before adk starts 
    because it needs to setup open telemetry before an agent gets selected.
  - The flag tells ADK to initialize the OpenTelemetry exporter and send 
    data to Google Cloud.
- Demo 1
  - **Interact**:
    - Select demo 1
    - Ask: "What is the weather in Tokyo?"
    - We see that it invokes all three tools and returns a result.
    - We can click on each tool to see the details.
    - Ask: "Is it raining in New York?"
    - This time, it just makes one tool call.
  - **View in Cloud Console -> Logging -> Trace Explorer**
    - if this is your first time using Cloud Trace, it can take a few 
      minutes to setup the internal data structures for you. But after that, 
      traces should appear pretty quickly. 
    - For "OpenTelemetry service" select "adk-weather"
    - Select a time period that covers what you want to look at. You may 
      also want to have it auto-update for your testing.
    - For "Span name" select "invocation"
    - We see there are two invocations
    - Select one
    - Here we see a trace 
      - the full round of activities that are related to 
        each other
      - we also see how one activity triggers a nested activity
      - So invoking the agent `weather_tools` triggers two LLM calls
    - Select "generate_content" for the first one
    - Look at the Input/Output tab
      - This shows the components of the exchange with the LLM
      - We can expand a part to see it better formated 
      - See the conversational exchange with the LLM
      - In the next-to-last, asking our question
      - Eventually, the LLM instructs what tools to call with what parameters
    - It then does the "execute_tool"
      - Click on "Attributes"
      - We can see the tool_call_args and the tool_response
    - Looking at the next "generate_content" and select "Input/Output"
      - We see the whole conversation
      - Next-to-last part is the function response with what the function 
        call returned
      - The LLM then replies with it's formatting of the response from the 
        tools.
  - We can also then say "View in Logs" to see that span in the log
    - Entries are in reverse chronological order
    - The bottom one are the system instructions, the overall prompt, sent 
      to the LLM
    - The next one is what the customer sent. Let's expand it and expand 
      nested fields.
    - We can see the text of what we sent
    - We can add the text field to the summary line, so we can see them better.
    - But this gets us both the customer messages and the LLM responses.
      - We really want it where the role is "user"
      - Select on the `role: "user"` and select "Show Matching entries"
      - The "JSON payload" section on the left is now set as a Field it 
        filters on
      - It changes our query to include that as a requirement
    - We can then expand it for all of our spans by editing that query to 
      remove the trace limitation
    - This is better, but we get function call results too, so we should 
      exclude it when the text is null.
      - Select on the `text: null`
      - Select "Hide matching entries"
  - Now we can go to "Actions" and download these results or set up logging 
    so these are sent to BigQuery for further analysis.
  - You should experiment with the various filters and values to find other 
    information you may want to see
- Let's look at another example to see what it might look like in cloud 
  trace.
- [demo-2/agent.py]
  - In this agent, we have a number of tools including a `search_agent_tool`
- [demo-2/search_agent.py]
  - This has a number of `AgentTool` objects which wrap an Agent as a Tool 
    so they can be used as a Tool in another agent.
  - In this case, we have several such wraps. From the bottom up:
    - We have the built-in `google_search` tool that is used by our 
      `search_agent`
    - But we want structured output from our search results
    - So we wrap `search_agent` as a tool that we use with 
      `structured_search_agent` that also has an `output_schema` set.
    - This `structured_search_agent` is then wrapped to give the 
      `search_agent_tool` that the root agent uses
- But if we go to see how this is run...
  - Command: `env $(cat demo-2/.env | xargs) adk web --otel_to_cloud`
  - Note that we have to load the environment from demo-2 so we get the 
    service name
  - Select "demo-2" in the web
- Demo 2
  - **Interaction**
    - "What was the closing price of Google?"
    - We see it invokes the `search_agent_tool`
    - But it then takes a while to run
    - When it returns, we see the return of the `search_agent_tool`, but not 
      the invocation of the other agents and tools
    - This is because `adk web` is just showing us what is going on with 
      this agent, not any others.
  - **View in Trace Explorer**
    - But if we look at the trace explorer...
    - Select the service name and invocation...
    - And select the specific starter invocation...
    - We see that there was a lot more activity
    - (Widen the Name field to see it all)
    - There was an execute_tool of structured_search_agent
    - Which invokes that agent
    - Which calls an LLM that determines it should execute the search_agent
    - Which invokes that agent
    - Which calls the llm which executes the internal google search tool
    - The `call_llm` has, hiding in the value, the tool call
- Conclusion
    - Observability closes the feedback loop. By seeing what users say and how
      the agent reacts, you can make data-driven decisions to improve your
      prompts and tools.
