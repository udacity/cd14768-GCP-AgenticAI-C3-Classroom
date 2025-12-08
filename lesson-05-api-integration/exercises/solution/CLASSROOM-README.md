# Module 5 Exercise Solution: Using a Currency Exchange API

This solution demonstrates how to securely integrate an external currency
exchange API into an ADK agent using Google Cloud Secret Manager.

---

## Overview

### What You'll Learn

This solution shows an implementation of secure API integration. You
will see how to retrieve sensitive keys at runtime without hardcoding them and
how to construct API requests based on retrieved secrets.

Learning objectives:

- Implementing `SecretManagerServiceClient` to access API keys.
- Constructing dynamic API URLs with `requests`.
- Processing JSON API responses within an ADK tool.

### Prerequisites

- Google Cloud Secret Manager API enabled.
- A secret named `exchangerate-api-key` created in Secret Manager.
- Application Default Credentials (ADC) configured locally.

### Setup Instructions

To run this solution, ensure you have completed the following setup steps:

1. **Obtain API Key and Understand API**: Before interacting with the
   ExchangeRate-API, you need to:
    *   Get an API key from [https://www.exchangerate-api.com/](https://www.exchangerate-api.com/).
    *   Review their **Documentation**, specifically the "Pair Conversion" endpoint
        (`GET https://v6.exchangerate-api.com/v6/YOUR-API-KEY/pair/FROM/TO/AMOUNT`).
        Understanding this structure is crucial for building the tool.

2. **Enable APIs**:
    * Go to the **Google Cloud Console**.
    * Navigate to **APIs & Services > Library**.
    * Enable **Secret Manager API**.

3. **Create Secret**:
    * Go to **Security > Secret Manager**.
    * Create a secret named `exchangerate-api-key`.
    * Paste your ExchangeRate-API key as the secret value.

4. **Authenticate Locally (ADC)**:
    * Run `gcloud auth application-default login` in your terminal.
    * Run `gcloud config set project <YOUR_PROJECT_ID>`.
    * Run `gcloud auth application-default set-quota-project <YOUR_PROJECT_ID>`.

---

## Understanding the Concept

### The Problem

We need to access live currency data from ExchangeRate-API, which requires an
API key. Storing this key in code is insecure. Additionally, we need a way for
our code to authenticate with Google Cloud services to retrieve this key without
managing yet another set of long-lived credentials manually.

### The Solution

1. **Secret Manager**: We store the API key in Google Cloud Secret Manager.
2. **ADC**: We use Application Default Credentials. This allows the Google Cloud
   client library to automatically find credentials (from
   `gcloud auth application-default login` locally or the metadata server in the
   cloud) to authenticate our request to Secret Manager.
3. **Runtime Retrieval**: The code fetches the key only when needed to make the
   API call.

---

## CODE WALKTHROUGH

### Repository Structure

```
.
├── __init__.py           # Package initialization.
├── agent-prompt.txt      # Agent instructions.
├── agent.py              # Agent configuration.
├── tools.py              # Secure key retrieval and API implementation.
├── README.md             # Overview.
└── requirements.txt      # Dependencies.
```

### Step 1: Secure Key Retrieval (`tools.py`)

The `get_api_key` function uses the `secretmanager` client library.

```python
def get_api_key():
  """Gets the API key from Secret Manager."""
  client = secretmanager.SecretManagerServiceClient()
  name = f"projects/{PROJECT_ID}/secrets/{SECRET_ID}/versions/latest"
  response = client.access_secret_version(name=name)
  return response.payload.data.decode("UTF-8")
```

**Key Detail**: The `client = ...` line relies on ADC. It doesn't need a path to
a key file because `gcloud` already set that up for us.

### Step 2: API Call (`tools.py`)

The `convert_currency` function uses the retrieved key to call the API.

```python
def convert_currency(source_currency: str, target_currency: str, amount: float):
  api_key = get_api_key()
  url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{source_currency}/{target_currency}/{amount}"
  response = requests.get(url)
  response.raise_for_status()
  data = response.json()

  if data and "conversion_result" in data:
    return {"converted_amount": data["conversion_result"]}
  return None
```

**Key Detail**: We construct the URL dynamically. The API key is injected into
the path as required by ExchangeRate-API's documentation.

### Step 3: Agent Configuration (`agent.py`)

The agent is simple, with just one tool.

```python
root_agent = Agent(
  name="currency_converter",
  # ...
  tools=[convert_currency]
)
```

---

## Important Details

### Setup Verification

If the solution code isn't working, verify these setup steps (crucial for ADC):

1. **Enable APIs**: Ensure "Secret Manager API" is enabled in your Google Cloud
   Project.
2. **Create Secret**: Confirm you have a secret named `exchangerate-api-key`
   containing your actual API key string.
3. **Authenticate**: Run `gcloud auth application-default login` and follow the
   browser prompt.
4. **Set Project**: Run `gcloud config set project <YOUR_PROJECT_ID>` to ensure
   the library knows which project to look in.

### Best Practices

- **Error Handling**: The solution uses `response.raise_for_status()` to catch
  HTTP errors (like 404 or 403) immediately.
- **Decoding**: Secrets are stored as bytes. Always `.decode("UTF-8")` the
  payload before using it in a string.
