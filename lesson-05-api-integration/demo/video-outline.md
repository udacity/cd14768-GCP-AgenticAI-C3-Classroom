# cd14768 - Lesson 5 - demo

Implementing API Integration for Agents

- In this demo, we'll see how to integrate external APIs (Google Places and
  Routes) securely using Google Cloud Secret Manager.
- [Setup Walkthrough] Google Cloud Console
    - **Enable APIs**: Explicitly walk through enabling "Google Places API
      (New)", "Google Routes API", and "Secret Manager API" in the API Library.
      Emphasize finding the "New" version of Places.
    - **Credentials**: Show where the API Key is created (APIs & Services >
      Credentials).
    - **Secret Manager**:
        - Navigate to Secret Manager.
        - Show the creation of the `places-api-key` secret.
        - Explain: "We pasted our API key here so we don't have to put it in our
          code."
- [Setup Walkthrough] Local Authentication (ADC)
    - Explain Application Default Credentials (ADC).
    - Show the command `gcloud auth application-default login`.
    - Explain that this command downloads a key file that the Google Cloud
      libraries use automatically to verify your identity.
- [tools.py] Secure Key Retrieval
    - Walk through `get_api_key`.
    - Explain `secretmanager.SecretManagerServiceClient`.
    - Highlight that it uses `os.environ.get("GOOGLE_CLOUD_PROJECT")` and the
      ADC credentials we just set up to find and access the secret securely.
- [tools.py] Places API Call (`get_place_details`)
    - Show how the retrieved `api_key` is passed to the `PlacesClient`.
    - Explain that this tool converts fuzzy names (like "Eiffel Tower") into
      precise coordinates (`lat`, `lng`).
- [tools.py] Routes API Call (`get_route_between_places`)
    - Show the HTTP POST request construction using the `requests` library.
    - Point out the `X-Goog-Api-Key` header injecting the secret.
    - Explain the `X-Goog-FieldMask`: "We only ask for distance and duration to
      save bandwidth and money."
- running the code
    - start `adk web` in another window (`cd lesson-05-api-integration` then
      `adk web`)
    - navigate to the URL.
- demonstration
    - Prompt: "How far is it from the Eiffel Tower to the Louvre?"
    - **Walkthrough**:
        - **Step 1**: Agent calls `get_place_details("Eiffel Tower", "Louvre")`.
        - **Step 2**: Tool fetches API Key from Secret Manager (using ADC
          authentication).
        - **Step 3**: Tool calls Places API, gets coordinates.
        - **Step 4**: Agent (or Tool logic) uses coordinates to call
          `get_route_between_places`.
        - **Step 5**: Tool calls Routes API, gets distance/duration.
        - **Result**: Agent answers: "It is about 3.5 km and takes 10 minutes to
          drive."
- conclusion and summary
    - Integrating APIs gives agents access to real-time, real-world data.
    - Security is paramount: Never hardcode keys. Use Secret Manager + ADC.
    - Field masks allow for efficient, cost-effective API usage.