# cd14768 - Lesson 5 - exercise
Using a Currency Exchange API

- In this solution walkthrough, we'll examine an agent that securely retrieves
  an API key from Secret Manager to perform currency conversions.
- [Setup Walkthrough] Prerequisites
    - **ExchangeRate-API Key & Docs**: Go
      to [exchangerate-api.com](https://www.exchangerate-api.com/), sign up for
      a key, and specifically review their "Pair Conversion" documentation for
      the URL format.
    - **Google Cloud Console**: Review:
        - Enabling "Secret Manager API".
        - The `exchangerate-api-key` in the Cloud Console Secret Manager.
    - **Local Setup**: Mention the need for
      `gcloud auth application-default login` to set up ADC.
- [tools.py] Review `get_api_key`
    - Highlight the use of `secretmanager.SecretManagerServiceClient`.
    - Explain that this client uses **ADC** (Application Default Credentials)
      implicitly to authenticate.
    - Show how it accesses the secret version and decodes the payload.
- [tools.py] Review `convert_currency`
    - Show how `get_api_key()` is called to get the credential.
    - Explain the URL construction based on the ExchangeRate-API
      documentation's "Pair Conversion" endpoint.
    - Review the `requests.get()` call and robust JSON parsing with
      `response.raise_for_status()`.
- [agent.py] Review Agent Configuration
    - Confirm the `convert_currency` tool is registered.
- running the code
    - start `adk web` in another window (`cd lesson-05-api-integration` then
      `adk web`)
    - navigate to the URL.
- demonstration
    - Prompt: "Convert 100 USD to EUR."
    - **Walkthrough**:
        - Agent calls `convert_currency`.
        - Code securely fetches the key (invisible to user/logs).
        - Code hits the API using the constructed URL.
        - Agent responds with the converted amount.
- conclusion and summary
    - We've built a secure, API-integrated tool capable of real-time currency
      conversions.
    - Emphasize the importance of consulting API documentation for correct
      endpoint usage.
    - Reiterate that API keys are stored securely in Secret Manager and accessed
      via ADC, enhancing security.
