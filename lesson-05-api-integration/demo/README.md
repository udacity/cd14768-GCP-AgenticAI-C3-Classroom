
# Module 05 Demo

## Environment

GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=<your project ID>
GOOGLE_CLOUD_LOCATION=us-central1


Make sure you replace <your project ID> with the ID for your project.

Using a LOCATION of us-central1 is usually the best bet in the United States,
but consider other cloud data center locations for elsewhere.

## Additional configuration

Ensure both required APIs are enabled:

 ```bash                                                                              
 # Enable Places API (for location search)                                            
 gcloud services enable places.googleapis.com                                         
                                                                                      
 # Enable Routes API (for distance/duration calculations)                             
 gcloud services enable routes.googleapis.com                                         
                                                                                      
 You can verify they're enabled:                                                      
 gcloud services list --enabled | grep -E "places|routes"