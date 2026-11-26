
# Module 05 Demo

## Environment

GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=<your project ID>
GOOGLE_CLOUD_LOCATION=global


Make sure you replace <your project ID> with the ID for your project.

Use a LOCATION of global: the Gemini models these exercises use are served
there. In the course's lab projects, a regional location such as
us-central1 answers 404 NOT_FOUND.

## Additional configuration

Ensure both required APIs are enabled:

 ```bash                                                                              
 # Enable Places API (for location search)                                            
 gcloud services enable places.googleapis.com                                         
                                                                                      
 # Enable Routes API (for distance/duration calculations)                             
 gcloud services enable routes.googleapis.com                                         
                                                                                      
 You can verify they're enabled:                                                      
 gcloud services list --enabled | grep -E "places|routes"