# Module 10: Implementing Agent Evaluation with ADK and Google Cloud Tracing

This lesson demonstrates how to implement observability in your agents using
OpenTelemetry and Google Cloud Tracing.

---

## Overview

### What You'll Learn

You will learn how to instrument your agent to send telemetry data to Google
Cloud, allowing you to trace the execution flow, monitor tool usage, and
crucially, understand how users are actually interacting with your agent.

Learning objectives:

- Configure OpenTelemetry environment variables for ADK.
- Run the agent with telemetry enabled using `adk web --otel_to_cloud`.
- Visualize and analyze agent activity in the Google Cloud Log Explorer.

### Prerequisites

- A Google Cloud Project.
- The **Telemetry API** must be enabled in your project. [Enable it here](https://console.developers.google.com/apis/api/telemetry.googleapis.com/overview).
- Basic understanding of running ADK agents.

---

## Understanding the Concept

### The Problem

Building an agent is just the first step. To truly evaluate its performance and
improve it, you need to understand how it is being used in the real world.

- **What are people saying to the agent?**
- **Are there specific questions causing errors?**
- **Is the agent selecting the right tools?**

Without visibility into these interactions, you are flying blind, making it
difficult to identify where customers are having problems or where the agent's
logic is failing.

### The Solution

**Observability** is the practice of instrumenting your system to generate
data (logs, metrics, traces) that answers these questions. By integrating
OpenTelemetry (OTEL) with ADK and Google Cloud Tracing, you gain a robust
observability layer. This allows you to "see" inside the agent's execution,
tracking every step from the user's input to the final response, including tool
calls and model latency.

---

## CODE WALKTHROUGH

### Repository Structure

```
.
├── __init__.py
├── agent-prompt.txt    # System instructions
├── agent.py            # The weather agent implementation
├── README.md           # Configuration details
└── requirements.txt
```

### Step 1: Configuration

To enable observability, we need to set specific environment variables in our
`.env` file. These variables tell the ADK how to format and send the telemetry
data.

```bash
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=<your project ID>
GOOGLE_CLOUD_LOCATION=us-central1

# OpenTelemetry Configuration
OTEL_SERVICE_NAME=<name you assign>
OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true
```

**Key Configuration Details:**

- `OTEL_SERVICE_NAME`: Identifies your service in the traces.
- `OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED`: Automatically captures
  standard Python logs.
- `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`: **Crucial.** This
  captures the actual text content of prompts and responses, allowing you to see
  exactly what the user said and what the model replied.

**IMPORTANT**:
You should carefully consider if you want to capture all messages. Some 
agents may be handling sensitive information that requires special handling, 
and you may not be allowed to save it. 

### Step 2: The Agent Code

The `agent.py` defines a simple weather agent with multiple tools. While the
code itself doesn't have explicit tracing logic, the ADK framework handles the
instrumentation automatically when configured correctly.

```python
# ... tool definitions ...

tools = [
  get_temperature,
  get_precipitation,
  get_wind_speed,
]

root_agent = Agent(
  name="weather_tools",
  # ...
  tools=tools,
)
```

### Step 3: Running the Agent

This is the most critical step. To send data to Google Cloud Trace, we must run
the agent with a specific flag.

```bash
adk web --otel_to_cloud
```

**Why this flag?**
By default, `adk web` might run locally or without telemetry to save resources.
The `--otel_to_cloud` flag explicitly tells the ADK runtime to initialize the
OpenTelemetry exporter and send the captured traces to your Google Cloud
Project.

### Step 4: Viewing the Data

Once you have chatted with the agent (e.g., "What's the weather in Tokyo?"), you
can view the traces in the Cloud Console.

1. Visit the **[Google Cloud Logs Explorer](https://console.cloud.google.com/logs/query)**.
2. Select your project if not already selected.
3. You will see a list of log events. Click on one to view the details.

---

## Important Details

### Best Practices

1. **Enable Content Capture**: Always set
   `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true` during development
   and debugging to see the actual conversation. Be mindful of PII (Personally
   Identifiable Information) in production.
2. **Service Naming**: Use descriptive `OTEL_SERVICE_NAME`s to easily
   distinguish between different agents or environments (e.g., `adk-weather-dev`
   vs `adk-weather-prod`).

### Common Errors

**Error**: "I don't see any logs in the console."

- **Cause 1**: The Telemetry API is not enabled in your Google Cloud Project.
- **Cause 2**: You ran `adk web` without the `--otel_to_cloud` flag.
- **Cause 3**: There is a delay (usually 1-2 minutes) before logs appear in
  the UI. Wait a moment and refresh.
