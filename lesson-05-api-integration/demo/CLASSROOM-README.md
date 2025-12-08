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
2. **Authentication**: 
   * You run `gcloud auth application-default login` on your
     machine. This saves your user credentials to a well-known location on your
     file system.
   * When you are running this on a Google Cloud service, such as Cloud Run 
     or Agent Engine, it will use the service account credentials for that 
     service.
3. **Tool Execution**: When the agent needs to check a route, the
   `get_api_key()` function uses the Google Cloud client library, which
   automatically finds your credentials and authenticates you, to fetch the
   key from Secret Manager.
   * Note that this means that the account you have credentials for (either 
     you or the service account) needs to be permitted to access the Secret 
     Manager. 
4. **API Call**: The tool uses this key to authenticate requests to the Places
   and Routes APIs.
5. **Result**: The APIs return JSON data (coordinates, distance, duration),
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

You need to explicitly enable the services we are going to use.

1. Open the **Google Cloud Console** and use the search bar at the top or
   navigate to **APIs & Services > Library**.
2. Search for and enable **Google Places API (New)**. (Important: Make sure it
   says "(New)" or "v1").
3. Search for and enable **Google Routes API**.
4. Search for and enable **Secret Manager API**.

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

### 4. Authenticate Locally (Set up ADC)

To allow your local Python script to access the Secret Manager in the cloud, you
must establish Application Default Credentials. Run the following commands in
your terminal:

```bash
# 1. Login and create the ADC file
gcloud auth application-default login

# 2. Ensure your gcloud config points to the correct project
gcloud config set project <YOUR_PROJECT_ID>

# 3. Set the quota project for billing/quota purposes (often same as your project)
gcloud auth application-default set-quota-project <YOUR_PROJECT_ID>
```

**Why do we do this?** The `gcloud auth application-default login` command opens
a browser window for you to log in. Once authenticated, it creates a JSON
credential file at `~/.config/gcloud/application_default_credentials.json` (or
similar). The Google Cloud Python libraries automatically detect this file and
use it to authorize requests.

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
  # The client library automatically looks for ADC here!
  client = secretmanager.SecretManagerServiceClient()
  name = f"projects/{PROJECT_ID}/secrets/{SECRET_ID}/versions/latest"
  response = client.access_secret_version(name=name)
  return response.payload.data.decode("UTF-8")
```

**Why it matters**: The sensitive key is never in the source code. ADC handles
the authentication to fetch it from the Secret Manager.

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

**Error**: `google.auth.exceptions.DefaultCredentialsError`.

- **Cause**: ADC is not set up. The code cannot find credentials to talk to
  Secret Manager.
- **Solution**: Run `gcloud auth application-default login`.

**Error**: `403 Forbidden` from Routes/Places API.

- **Cause**: The API Key is invalid, deleted, or restricted to the wrong APIs/IP
  addresses.
- **Solution**: Verify the API Key restrictions in APIs & Services >
  Credentials.

**Error**: `google.api_core.exceptions.NotFound: 404 Secret not found`.

- **Cause**: The secret name in `tools.py` (`places-api-key`) does not match the
  name created in the Cloud Console.
- **Solution**: Ensure the names match exactly.