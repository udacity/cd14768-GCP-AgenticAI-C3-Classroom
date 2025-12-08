# Module 5: Implementing API Integration for Agents with ADK, Python, and Google Cloud Secret Manager

This demo illustrates how to expand an agent's capabilities by integrating
external APIs. Specifically, we will build an agent that can calculate the
driving distance and duration between two places using the Google Places API and
the Google Routes API. Crucially, we will demonstrate how to securely manage the
required API keys using Google Cloud Secret Manager.

---

## Overview

### What You'll Learn

You will learn the end-to-end process of integrating a third-party or Google
Cloud API into an ADK agent. This covers secure key storage, making HTTP
requests from within a tool, and processing the API response for the LLM.

Learning objectives:

- Integrate external APIs (Google Places and Routes) into ADK tools.
- Securely retrieve API keys from Google Cloud Secret Manager using Application
  Default Credentials (ADC).
- Perform HTTP requests (POST) to interact with RESTful APIs.
- Construct complex tools that combine data from multiple API endpoints.

### Prerequisites

- Basic understanding of Python and REST APIs.
- A Google Cloud Project with billing enabled.
- The `gcloud` CLI installed and authenticated.

---

## Understanding the Concept

### The Problem

Agents often need real-world data that isn't in their training set—like current
traffic, specific location coordinates, or driving distances. While APIs exist
for this, they require authentication (API Keys). Hardcoding these keys in your
code is a major security risk. If you commit your code to GitHub, your key could
be stolen and used to run up your bill.

### The Solution

1. **External APIs**: We use the **Google Places API** to convert names (e.g.,
   "Eiffel Tower") into coordinates and the **Google Routes API** to calculate
   the path between those coordinates.
2. **Google Cloud Secret Manager**: Instead of hardcoding keys, we store them in
   a secure, encrypted vault in the cloud.
3. **Application Default Credentials (ADC)**: Our code uses the identity of the
   environment (your local user via `gcloud auth application-default login` or
   the service account in production) to securely request the key from Secret
   Manager at runtime.

### How It Works

1. **Setup**: You create an API Key in Google Cloud Console and save it as a
   "Secret" in Secret Manager.
2. **Tool Execution**: When the agent needs to check a route, the
   `get_api_key()` function uses the Google Cloud client library to fetch the
   key from Secret Manager.
3. **API Call**: The tool uses this key to authenticate requests to the Places
   and Routes APIs.
4. **Result**: The APIs return JSON data (coordinates, distance, duration),
   which the tool parses and returns to the agent.

### Key Terms

**Google Cloud Secret Manager**: A secure and convenient storage system for API
keys, passwords, certificates, and other sensitive data.

**Application Default Credentials (ADC)**: A strategy used by Google Cloud
client libraries to automatically find credentials. In a local environment, it
uses your user credentials that you have configured using the `gcloud` command;
in Google Cloud, it uses the attached Service Account for the service you 
are running on.

**Google Routes API**: A Google Maps Platform API that provides comprehensive
routing data, including distance, duration, and traffic conditions, succeeding
the older Distance Matrix API features.

---

## SETUP INSTRUCTIONS

To run this demo, you must set up your Google Cloud environment.

### 1. Enable APIs

In your Google Cloud Project, enable the following APIs:

* **Google Places API (New)** (Note: Ensure you select the "New" version if
  prompted).
* **Google Routes API**
* **Secret Manager API**

### 2. Create an API Key

1. Go to **APIs & Services > Credentials** in the Google Cloud Console.
2. Click **Create Credentials** -> **API key**.
3. (Optional but Recommended) Restrict the key to only the "Places API (New)"
   and "Routes API".
4. Copy the key string.

### 3. Store Key in Secret Manager

1. Go to **Security > Secret Manager** in the Google Cloud Console.
2. Click **Create Secret**.
3. Name: `places-api-key` (This exact name is used in the code).
4. Secret value: Paste the API key you copied.
5. Click **Create Secret**.

### 4. Authenticate Locally

Ensure your local environment can access the project and the secret:

```bash
gcloud auth application-default login
gcloud config set project <YOUR_PROJECT_ID>
```

---

## CODE WALKTHROUGH

### Repository Structure

```
.
├── __init__.py           # Package initialization.
├── agent-prompt.txt      # Agent instructions.
├── agent.py              # Agent configuration.
├── tools.py              # Implementation of API integration and Secret Manager retrieval.
├── README.md             # Overview.
└── requirements.txt      # Dependencies (google-cloud-secret-manager, google-maps-places, requests).
```

### Step 1: Secure Key Retrieval (`tools.py`)

The `get_api_key` function retrieves the secret. Notice it doesn't take any
arguments; it relies on `PROJECT_ID` (from env vars) and the hardcoded
`SECRET_ID`.

```python
import os
from google.cloud import secretmanager

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
SECRET_ID = "places-api-key"


def get_api_key():
  """Gets the API key from Secret Manager."""
  client = secretmanager.SecretManagerServiceClient()
  name = f"projects/{PROJECT_ID}/secrets/{SECRET_ID}/versions/latest"
  response = client.access_secret_version(name=name)
  return response.payload.data.decode("UTF-8")
```

**Why it matters**: The sensitive key is never in the source code.

### Step 2: Places API Integration (`tools.py`)

The `get_place_details` function converts place names to coordinates using the
Places API client library.

```python
from google.maps.places_v1 import PlacesClient

# ...
client = PlacesClient(client_options={"api_key": api_key})
request = SearchTextRequest(text_query=place_name)
response = client.search_text(request=request,
                              metadata=[('x-goog-fieldmask', field_mask)])
```

### Step 3: Routes API Integration (`tools.py`)

The `get_route_between_places` function calculates the trip. It constructs a raw
HTTP POST request because we are using the `requests` library for this example.

```python
    headers = {
  "Content-Type": "application/json",
  "X-Goog-Api-Key": api_key,
  "X-Goog-FieldMask": "routes.distanceMeters,routes.duration",
}

# ... payload with origin and destination coordinates ...

url = "https://routes.googleapis.com/directions/v2:computeRoutes"
response = requests.post(url=url, headers=headers, json=request_body)
```

**Key Detail**: We use the `X-Goog-FieldMask` header to request *only* the
distance and duration, keeping the response small and cost-effective.

---

## Important Details

### Best Practices

- **Minimal Permissions**: When creating the API Key, restrict it to *only* the
  APIs it needs. When assigning IAM roles to the Service Account accessing the
  Secret, give it *only* the "Secret Manager Secret Accessor" role.
- **Field Masks**: Always use Field Masks (in both Places and Routes APIs) to
  request only the data you need. This reduces latency and billing costs.
- **Error Handling**: Real-world API integration needs robust error handling.
  Note the `response.raise_for_status()` in the Routes code—this ensures the
  agent knows if the API call failed (e.g., due to quota limits).

### Common Errors

**Error**: `403 Permission Denied` when accessing Secret Manager.

- **Cause**: The user or service account running the code does not have the
  `Secret Manager Secret Accessor` role on the specific secret or the project.
- **Solution**: Check IAM permissions in the Cloud Console.

**Error**: `403 Forbidden` from Routes/Places API.

- **Cause**: The API Key is invalid, deleted, or restricted to the wrong APIs/IP
  addresses.
- **Solution**: Verify the API Key restrictions in APIs & Services >
  Credentials.

**Error**: `google.api_core.exceptions.NotFound: 404 Secret not found`.

- **Cause**: The secret name in `tools.py` (`places-api-key`) does not match the
  name created in the Cloud Console.
- **Solution**: Ensure the names match exactly.
