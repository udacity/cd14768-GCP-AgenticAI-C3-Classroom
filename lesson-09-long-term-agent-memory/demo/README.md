# Module 09 Demo

## Environment

GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=<your project ID>
GOOGLE_CLOUD_LOCATION=global


Make sure you replace <your project ID> with the ID for your project.

Use a LOCATION of global: the Gemini models these exercises use are served
there. In the course's lab projects, a regional location such as
us-central1 answers 404 NOT_FOUND.

## Additional Setup

### Agent Engine Memory Bank

To create an Agent Engine instance:

1. Make sure you have the .env file setup as above.
2. In the same directory as the .env file, run the `create_agent_engine.py` 
   script that is in the `notes` folder. 
3. It will print out the resource name, which we'll be setting in the .env file.

If you forget the resource name, you can visit the Google Cloud Console and 
go to the Agent Engine configuration page (Hint: Search for it) to get the 
resource name.



