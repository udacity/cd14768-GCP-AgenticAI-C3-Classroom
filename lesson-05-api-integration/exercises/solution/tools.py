import os
from google.cloud import secretmanager
import requests

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
SECRET_ID = "exchangerate-api-key"

def get_api_key():
    """Gets the API key from Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{SECRET_ID}/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode("UTF-8")

def convert_currency(source_currency: str, target_currency: str, amount: float):
    """Converts an amount from one currency to another."""
    api_key = get_api_key()
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{source_currency}/{target_currency}/{amount}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    data = response.json()

    if data and "conversion_result" in data:
        return {"converted_amount": data["conversion_result"]}

    return None
