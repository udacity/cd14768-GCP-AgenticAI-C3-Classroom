# cd14768 - Lesson 10 - demo

Implementing Agent Evaluation with ADK and Google Cloud Observability

- Objective: Learn to implement observability to evaluate agent performance
  using OpenTelemetry and Google Cloud Logging.
- Why Observability for Evaluation?
    - Evaluation isn't just running pre-made test scripts.
    - True evaluation requires understanding **real-world usage**.
    - What are users actually asking? Where does the agent get confused? Which
      tools are failing?
    - Observability gives us the raw data (logs/traces) to answer these
      questions and continuously improve the agent.
- Setup (Prerequisites)
    - Ensure the **Telemetry API** is enabled in your Google Cloud Project.
    - Configure `.env`:
        - `OTEL_SERVICE_NAME`: Identify your agent (e.g., `adk-weather`).
        - `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true`: 
          **Critical** for seeing what was said.
        - **Warning**: Be careful with `CAPTURE_MESSAGE_CONTENT` in production
          if handling PII/sensitive data.
- [agent.py] The Agent Code
    - Show `agent.py`.
    - **Key Point**: There is NO special tracing code here.
    - The ADK framework automatically instruments the agent when the environment
      variables are set.
- Running the Agent
    - Command: `adk web --otel_to_cloud`
    - **Explanation**: This flag tells ADK to initialize the OpenTelemetry
      exporter and send data to Google Cloud. Without it, traces stay local or
      are dropped.
- Demonstration
    - **Interact**:
        - Start the agent.
        - Ask: "What is the weather in Tokyo?"
        - Agent calls tools and responds.
    - **Verify in Cloud Console**:
        - Go to **Google Cloud Logs Explorer**.
        - Select your project.
        - Look for the recent log entries (you might need to filter by
          `OTEL_SERVICE_NAME`).
        - **Drill Down**: Click a log entry to expand it.
        - Show the `jsonPayload` or `textPayload` to find the captured prompt
          and response.
        - Explain how this visibility allows you to debug "why did the agent say
          that?"
- Conclusion
    - Observability closes the feedback loop. By seeing what users say and how
      the agent reacts, you can make data-driven decisions to improve your
      prompts and tools.
