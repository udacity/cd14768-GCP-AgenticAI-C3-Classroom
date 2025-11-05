import os
from google.cloud import secretmanager
from google.maps.places_v1 import PlacesClient
from google.maps.places_v1.types import SearchTextRequest

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
SECRET_ID = "places-api-key"

def get_api_key():
    """Gets the API key from Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{SECRET_ID}/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode("UTF-8")

def get_place_details(place1: str, place2: str):
    """Gets the address and coordinates for two places."""
    api_key = get_api_key()
    client = PlacesClient(client_options={
        "api_key": api_key,
    })

    def get_details(place_name):
        fields = ['places.displayName', 'places.formattedAddress', 'places.location']
        field_mask = ",".join(fields)
        request = SearchTextRequest(
            text_query = place_name,
        )
        response = client.search_text( request=request, metadata=[('x-goog-fieldmask', field_mask)] )
        if response and response.places:
            info = response.places[0]
            name = info.display_name.text
            address = info.formatted_address
            location = info.location
            latitude = location.latitude
            longitude = location.longitude

            return {
                "name": name,
                "address": address,
                "location": {
                    "latitude": latitude,
                    "longitude": longitude,
                }
            }

        return None

    details1 = get_details(place1)
    details2 = get_details(place2)

    return {"place1": details1, "place2": details2}
