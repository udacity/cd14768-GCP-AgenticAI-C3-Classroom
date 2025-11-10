from google.adk.tools import ToolContext

def set_home_location(location: str, tool_context: ToolContext):
    """
    Sets the customer's home location.
    Only do this if they explicitly tell you to.
    """
    tool_context.state["user:home_location"] = location
    tool_context.state["user:home_location_instruction"] = f"""
      The customer's home location is: {location}.
      If they do not specify a different starting location, you should 
      add this home location as the first airport of the itinerary.
    """
    return f"Home location set to {location}."

def add_airport(tool_context: ToolContext, airport: str):
    """
    Adds an airport to the itinerary.
    """
    itinerary = tool_context.state.get("itinerary", [])
    itinerary.append(airport)
    tool_context.state["itinerary"] = itinerary
    return {"status": f"Added {airport} to the itinerary."}

def create_itinerary(tool_context: ToolContext):
    """
    Creates the itinerary based on the airports in the session state.
    """
    itinerary = tool_context.state.get("itinerary", [])
    home_location = tool_context.state.get("user:home_location")

    if not itinerary:
        return {"itinerary": []}

    legs = []
    for i in range(len(itinerary) - 1):
        legs.append({"from": itinerary[i], "to": itinerary[i+1]})

    return {"itinerary": legs}