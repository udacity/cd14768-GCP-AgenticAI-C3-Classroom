# cd14768 - Lesson 5 - exercise
Using a Currency Exchange API

- In this exercise you were asked to create an agent that calls an 
  API to do currency conversions. You needed to create an API Key with a 
  service that would provide this information and then write a tool that 
  would access this API 
- The API Key needed to be securely stored, preferably using the Google 
  Cloud Secret Manager.
  - Since the Secret Manager also needs credentials to access, we used the 
    Google Cloud Application Default Credentials (ADC) to do so.
    - A secure way from our local machine to authenticate ourselves to the
      service.
    - On Google Cloud resources (Cloud Run or Agent Engine), there is a
      service account that we can permit to access the Secret Manager.
- [Setup Walkthrough] Prerequisites
    - **ExchangeRate-API Key & Docs**: Go
      to [exchangerate-api.com](https://www.exchangerate-api.com/), sign up for
      a key, and specifically review their "Pair Conversion" documentation for
      the URL format.
    - **Google Cloud Console**: Review:
        - Enabling "Secret Manager API".
        - The `exchangerate-api-key` in the Cloud Console Secret Manager.
- [Setup Walkthrough] Local Authentication (ADC)
    - Explain Application Default Credentials (ADC).
    - Show the command `gcloud auth application-default login`.
    - Explain that this command downloads a key file that the Google Cloud
      libraries use automatically to verify your identity.
- [agent.py] Review Agent Configuration
    - Confirm the `convert_currency` tool is registered.
- [agent-prompt.txt] Review instructions
  - Format for data, both to tool and to customer
  - What tool is available
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
