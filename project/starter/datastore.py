import os

from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1 as discoveryengine

# Definition of a tool that accesses a Vertex AI Search Datastore

#
# This is based on code provided by Google at
# https://cloud.google.com/generative-ai-app-builder/docs/samples/genappbuilder-search
#
# The object definitions aren't available to all IDEs because of Google's ProtoBuf
# implementation, so the IDE may generate a warning, but work fine. I've used
# dicts here instead, but indicated the Class that could be used instead.
# You can see the definitions at
# https://cloud.google.com/python/docs/reference/discoveryengine/latest/google.cloud.discoveryengine_v1.types
#
def search(
    project_id: str,
    location: str,
    engine_id: str,
    search_query: str,
) -> list[str]:
  #  For more information, refer to:
  # https://cloud.google.com/generative-ai-app-builder/docs/locations#specify_a_multi-region_for_your_data_store
  client_options = (
    ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
    if location != "global"
    else None
  )

  # Create a client
  client = discoveryengine.SearchServiceClient(client_options=client_options)

  # The full resource name of the search app serving config
  serving_config = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/servingConfigs/default_config"

  # discoveryengine.SearchRequest
  request = {
    "serving_config": serving_config,
    "query": search_query,
    "page_size": 10,
    "content_search_spec": {
      "search_result_mode":
        discoveryengine.SearchRequest.ContentSearchSpec.SearchResultMode.CHUNKS
    },
    "query_expansion_spec": {
      "condition":
        discoveryengine.SearchRequest.QueryExpansionSpec.Condition.AUTO,
    },
    "spell_correction_spec": {
      "mode":
        discoveryengine.SearchRequest.SpellCorrectionSpec.Mode.AUTO,
    },
  }

  page_result = client.search(request)

  results = []
  for result in page_result:
    if result.chunk and result.chunk.content:
      results.append(result.chunk.content)
  return results


def datastore_search_tool(search_query: str) -> str | list[str]:
  """
  Searches Betty's store documents for history, staff, and working hours.

  Args:
    search_query: The store topic or question to search for.
  """
  try:
    project_id = os.environ.get("DATASTORE_PROJECT_ID")
    engine_id = os.environ.get("DATASTORE_ENGINE_ID")
    if not project_id or not engine_id:
      return "Datastore configuration is missing. Set DATASTORE_PROJECT_ID and DATASTORE_ENGINE_ID."

    results = search(
      project_id=project_id,
      engine_id=engine_id,
      location=os.environ.get("DATASTORE_LOCATION", "global"),
      search_query=search_query,
    )
    return results if results else "No results found."
  except Exception as e:
    return f"A problem occurred: {e}"