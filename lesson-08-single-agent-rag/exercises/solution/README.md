
# Module 08 Exercise

## Environment

GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=<your project ID>
GOOGLE_CLOUD_LOCATION=us-central1

DATASTORE_PROJECT_ID=<your project ID>
DATASTORE_LOCATION=global
DATASTORE_ENGINE_ID=<app id>


Make sure you replace <your project ID> with the ID for your project.

Using a LOCATION of us-central1 is usually the best bet in the United States,
but consider other cloud data center locations for elsewhere.

The Datastore location should be set to "global".
The Datastore Engine ID should be set to the AI Applications App ID.

## Additional setup

### Google Cloud Storage and AI Applications

There are a number of files in the "demo" folder to upload to GCS and then
index using AI Applications.

To create a Cloud Storage bucket and upload to it:
1. In the Google Cloud Console, go to the "Cloud Storage" configuration.
   (Hint: You can search for it in the search bar)
2. Select "Create bucket"
3. Enter the name you want for the bucket.
4. Select "Create"
5. If there is a pop-up about Public access, confirm that you want Enforce
   public access prevention enabled.
6. You'll be taken to an (empty) file listing. You can drag and drop the
   files from the "docs" directory here.

To create your Vertex AI Search Application and data store:
1. In the Google Cloud Console, go to the "Vertex AI Search" configuration. 
   (Hint: You can search for it in the search bar, you can also search for 
   "AI Application".)
2. Select "Create App"
3. Select "Custom search (general)"
4. Leave the app settings unchanged
5. Enter an App name
6. Enter a company name for the app
7. Select "Continue"
8. You'll be taken to the Data Stores page. Select "Create Data Store"
9. Select "Cloud Storage" to import the data from the bucket we created above
10. Select "Unstructured documents"
11. Set the Synchronization frequency to "One time"
12. Choose the GCS bucket you uploaded the files to above
13. Enter a Data store name. It is usually a good idea to have it a name
    based on the App name you chose
14. Select "Create"
15. You'll be taken back to the last step of the Create App. Select "Create"

The system will then begin to load and index the documents. You can see
the status of this by selecting the "Data" menu item on the left when
looking at the App information.

If you return to the list of AI Apps, you will see the ID that is used
for this AI App instance. This is the value of the "DATASTORE_ENGINE_ID" above.
