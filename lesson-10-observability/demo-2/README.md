# Module 10 Demo 2

## Environment

GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=<your project ID>
GOOGLE_CLOUD_LOCATION=us-central1

OTEL_SERVICE_NAME=adk-weather
OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true

Make sure you replace <your project ID> with the ID for your project.

Using a LOCATION of us-central1 is usually the best bet in the United States,
but consider other cloud data center locations for elsewhere.

## Instructions

Make sure the Telemetry API is
[enabled](https://console.developers.google.com/apis/api/telemetry.googleapis.com/overview)

Run this with `adk web --otel_to_cloud`

Visit Google Cloud Console Trace Explorer.
