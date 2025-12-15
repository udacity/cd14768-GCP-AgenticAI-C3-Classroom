# Module 09 Exercise

## Environment

GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=<your project ID>
GOOGLE_CLOUD_LOCATION=us-central1


Make sure you replace <your project ID> with the ID for your project.

Using a LOCATION of us-central1 is usually the best bet in the United States,
but consider other cloud data center locations for elsewhere.

## Additional Setup

### Agent Engine Memory Bank

To create an Agent Engine instance:

1. Make sure you have the .env file setup as above.
2. In the same directory as the .env file, run the `create_agent_engine.py` 
   script that is in the `notes` folder. 
3. It will print out the resource name, which we need to start `adk web`.

If you forget the resource name, you can visit the Google Cloud Console and 
go to the Agent Engine configuration page (Hint: Search for it) to get the 
resource name.



