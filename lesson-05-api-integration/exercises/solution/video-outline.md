# cd14768 - Lesson 5 - exercise
Using a Currency Exchange API

- In this solution walkthrough, we'll examine an agent that securely retrieves an
  API key from Secret Manager to perform currency conversions.
- [tools.py] Review `get_api_key`
  - Highlight the use of `secretmanager.SecretManagerServiceClient`.
  - Explain that this client uses **ADC** (Application Default Credentials) implicitly.
  - Show how it accesses the secret version and decodes the payload.
- [tools.py] Review `convert_currency`
  - Show how `get_api_key()` is called to get the credential.
  - Explain the URL construction: It injects the secret key into the ExchangeRate-API endpoint format.
  - Review the `requests.get()` call and JSON parsing.
- [agent.py] Review Agent Configuration
  - Confirm the `convert_currency` tool is registered.
- [Setup Check] ADC and Secrets
  - Remind learners that for this code to work, they must have:
    1. Created the `exchangerate-api-key` secret in Cloud Console.
    2. Run `gcloud auth application-default login` locally.
- running the code
  - start `adk web` in another window (`cd lesson-05-api-integration` then `adk web`)
  - navigate to the URL.
- demonstration
  - Prompt: "Convert 100 USD to EUR."
  - **Walkthrough**:
    - Agent calls `convert_currency`.
    - Code securely fetches the key (invisible to user/logs).
    - Code hits the API.
    - Agent responds with the converted amount.
- conclusion and summary
  - We've built a secure, API-integrated tool.
  - We avoided hardcoding secrets by using Secret Manager.
  - We simplified authentication using ADC.
