from google.adk.tools import ToolContext

def set_home_location(location: str, tool_context: ToolContext):
    """
    Sets the customer's home location.
    Only do this if they explicitly tell you to.
    """
    # TODO: Store the location in the user-scoped state
    # TODO: Also set a dynamic instruction for the prompt

    return f"Home location set to {location}."

def add_city(tool_context: ToolContext, city: str):
    """
    Adds a city to the itinerary.
    """
    # TODO: Get the current itinerary from the session state (default to empty list)
    
    # TODO: Append the new city to the list
    
    # TODO: Update the session state with the new itinerary
    
    return {"status": f"Added {city} to the itinerary."}

def create_itinerary(tool_context: ToolContext):
    """
    Creates the itinerary based on the cities in the session state.
    """
    # TODO: Get the itinerary from session state

    legs = []
    # TODO: Loop through the itinerary and create legs {"from": ..., "to": ...}
    
    return {"itinerary": legs}
