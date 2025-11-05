import os
from google.cloud import secretmanager
from google.maps.places_v1 import PlacesClient
from google.maps.places_v1.types import SearchTextRequest
from google.maps.routing_v2 import RoutesClient
from google.maps.routing_v2.types import ComputeRoutesRequest, Waypoint, Location
from google.type import latlng_pb2

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

def get_waypoint( location: dict ):
    latlng = latlng_pb2.LatLng(
        latitude=location["latitude"],
        longitude=location["longitude"],
    )
    location = Location(lat_lng = latlng)
    return Waypoint( location=location )

def get_route_between_places(location1: dict, location2: dict):
    """Gets the distance and duration of the route between two places."""
    api_key = get_api_key()

    # Use the routing_v2 library to get the distance between location1 and location2
    origin = get_waypoint( location1 )
    destination = get_waypoint( location2 )
    request = ComputeRoutesRequest(
        origin=origin,
        destination=destination,
        travel_mode="DRIVE",
    )

    client = RoutesClient(client_options={"api_key": api_key})
    fields = ['routes.distance_meters', 'routes.duration']
    field_mask = ",".join(fields)
    response = client.compute_routes( request=request, metadata=[('x-goog-fieldmask', field_mask)] )

    if response and response.routes:
        route = response.routes[0]
        return {
            "distance_meters": route.distance_meters,
            "duration_seconds": route.duration.seconds,
        }

    return None
