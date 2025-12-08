import os
from google.cloud import secretmanager
import requests

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
# TODO: Set the SECRET_ID to the name of the secret you created in Secret Manager
SECRET_ID = "exchangerate-api-key"

def get_api_key():
    """Gets the API key from Secret Manager."""
    # TODO: Implement

def convert_currency(source_currency: str, target_currency: str, amount: float):
    """Converts an amount from one currency to another."""
    # TODO: Get the API key
    # TODO: Construct the API URL (https://v6.exchangerate-api.com/v6/...)
    # TODO: Make a GET request to the API
    # TODO: Parse the response and return the conversion result
