# Module 5 Exercise: Using a Currency Exchange API

In this exercise, you will build an agent that can convert currencies using a
real-world API. You will practice securing your API key using Google Cloud
Secret Manager and integrating the API into an ADK tool.

---

## Overview

### What You'll Learn

You will learn how to:

- Obtain an API key from a third-party service.
- Store that key securely in Google Cloud Secret Manager.
- Write Python code to retrieve the key at runtime using Application Default
  Credentials (ADC).
- Implement an ADK tool that calls the API to perform currency conversion.

Learning objectives:

- Securely manage API keys using Google Cloud Secret Manager.
- Integrate a RESTful API (ExchangeRate-API) into an agent tool.
- Use `requests` library to make HTTP calls.
- Configure an ADK agent to use the new tool.

### Prerequisites

- Basic Python knowledge, including making HTTP requests.
- Google Cloud Project with billing enabled.
- `gcloud` CLI installed and authenticated.
- The `requests` and `google-cloud-secret-manager` libraries installed.

---

## Understanding the Concept

### The Problem

We want our agent to provide accurate currency conversion rates. We cannot
hardcode these rates because they change constantly. We need to use an external
API like ExchangeRate-API. However, this API requires an API key. Hardcoding
this key in our source code is a security vulnerability.

### The Solution

We will use **Google Cloud Secret Manager** to store the API key. Our agent's
code will request the key from Secret Manager only when it needs to call the
API. This keeps the key out of our codebase and source control. 

This poses a chicken-and-egg problem, however. To keep our secrets safe, the 
Secret Manager requires credentials to access. But how do we keep *those* 
credentials secure?

To solve this, we will use **Application Default Credentials (ADC)** to 
authenticate our code with Google Cloud, eliminating the need for hardcoded 
service account keys.

### How It Works

1. **Get Key**: You sign up for a free key at `exchangerate-api.com`.
2. **Store Secret**: You save this key in Google Cloud Secret Manager as
   `exchangerate-api-key`.
3. **Retrieve Secret**: Your Python code uses the `SecretManagerServiceClient`
   to fetch the key.
4. **Call API**: Your code constructs a URL with the key and currency pair,
   sends a request, and parses the JSON response.

---

## SETUP INSTRUCTIONS

### 1. Get an API Key

1. Go to [https://www.exchangerate-api.com/](https://www.exchangerate-api.com/).
2. Sign up for a free account.
3. Copy your API Key from the dashboard.
4. Read the **Documentation** (specifically the "Standard Request" or "Pair
   Conversion" endpoints) to understand how to construct the URL.
    * Hint: We want to convert a specific amount, so look for the "Pair
      Conversion" format:
      `GET https://v6.exchangerate-api.com/v6/YOUR-API-KEY/pair/FROM/TO/AMOUNT`.

### 2. Enable Secret Manager API

1. Go to the Google Cloud Console.
2. Navigate to **APIs & Services > Library**.
3. Search for "Secret Manager API" and enable it.

### 3. Store Key in Secret Manager

1. Go to **Security > Secret Manager**.
2. Click **Create Secret**.
3. Name: `exchangerate-api-key`.
4. Secret value: Paste your ExchangeRate-API key.
5. Click **Create Secret**.

### 4. Authenticate Locally (ADC)

Run these commands in your terminal:

```bash
gcloud auth application-default login
gcloud config set project <YOUR_PROJECT_ID>
gcloud auth application-default set-quota-project <YOUR_PROJECT_ID>
```

---

## EXERCISE INSTRUCTIONS

### Your Task

Complete the `currency_converter` agent by implementing the secure key retrieval
and the API call logic.

1. **Implement `get_api_key` in `tools.py`**:
    * Use `secretmanager.SecretManagerServiceClient` to access the secret
      version.
    * The secret name is `exchangerate-api-key`.
    * Return the decoded string.
2. **Implement `convert_currency` in `tools.py`**:
    * Call `get_api_key()` to get the credential.
    * Construct the API URL using the format found in the documentation.
    * Use `requests.get()` to call the API.
    * Return a dictionary with the converted amount (e.g.,
      `{"converted_amount": 123.45}`).
3. **Configure Agent**:
    * In `agent.py`, import `convert_currency`.
    * Add it to the `tools` list.
    * Write a simple instruction in `agent-prompt.txt`. Remember that 
      the API Keys and the `get_api_key()` should be invisible to the LLM. 

### Requirements

1. Do **not** hardcode the API key in `tools.py`.
2. Use the `requests` library for the API call.
3. Handle the API response correctly (extract the result).

### Repository Structure

```
.
├── __init__.py           # Package initialization.
├── agent-prompt.txt      # (Your task) Agent instructions.
├── agent.py              # (Your task) Agent configuration.
├── tools.py              # (Your task) Key retrieval and API logic.
├── .env-sample           # Environment variables.
├── README.md             # Overview.
└── requirements.txt      # Dependencies.
```

### Starter Code

`tools.py`

```python
import os
from google.cloud import secretmanager
import requests

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
SECRET_ID = "exchangerate-api-key"


def get_api_key():
  # TODO: Implement secure retrieval


def convert_currency(source_currency: str, target_currency: str, amount: float):
  # TODO: Implement API call
```

### Expected Behavior

**Running the agent:**

```bash
adk web
```

**Example usage:**

```text
Human: "Convert 100 USD to EUR."
Agent: "100 USD is approximately 92.50 EUR." (Exact value depends on current rates)
```

### Implementation Hints

1. The resource name for the secret is:
   `projects/{PROJECT_ID}/secrets/{SECRET_ID}/versions/latest`.
2. The API response JSON usually contains a `conversion_result` field for pair
   conversions.
3. Make sure your `PROJECT_ID` environment variable is set correctly in your
   `.env` file.

---

## Important Details

### Best Practices

- **Review Docs**: Always read the API documentation first. Knowing the endpoint
  structure and response format is half the battle.
- **Secure by Design**: Start with Secret Manager integration immediately.
  Don't "hardcode for now, fix later"—that's how keys get leaked.
- **Quota Management**: Be aware of API limits (the free tier of
  ExchangeRate-API has a monthly request limit).

### Common Errors

**Error**: `403 Permission Denied` on Secret Manager.

- **Solution**: Ensure your user (locally) or service account (cloud) has the
  `Secret Manager Secret Accessor` role.

**Error**: `KeyError: 'conversion_result'`.

- **Solution**: Print `data` to debug. You might be using the wrong endpoint or
  the API returned an error (e.g., invalid currency code).
