import requests
import json
import os
from dotenv import load_dotenv 

# Load environment variables (client ID, secret, tenant ID)
load_dotenv()

CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
TENANT_ID = os.getenv("AZURE_TENANT_ID")

GRAPH_TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
GRAPH_API_URL = "https://graph.microsoft.com/v1.0"


def get_graph_token():
    """
    Retrieves an OAuth2 token using client credentials.
    """
    data = {
        "client_id": CLIENT_ID,
        "scope": "https://graph.microsoft.com/.default",
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }

    response = requests.post(GRAPH_TOKEN_URL, data=data)
    response.raise_for_status()

    token = response.json()["access_token"]
    return token


def create_user_in_azure(new_hire: dict) -> str:
    """
    Creates a new Azure AD user using Microsoft Graph.
    Returns the user's objectId.
    """

    token = get_graph_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Build the user payload
    user_payload = {
        "accountEnabled": True,
        "displayName": f"{new_hire['firstName']} {new_hire['lastName']}",
        "mailNickname": new_hire["mailNickname"],
        "userPrincipalName": new_hire["userPrincipalName"],
        "usageLocation": new_hire.get("usageLocation", "US"),
        "passwordProfile": {
            "forceChangePasswordNextSignIn": True,
            "password": new_hire["temporaryPassword"]
        }
    }

    response = requests.post(
        f"{GRAPH_API_URL}/users",
        headers=headers,
        data=json.dumps(user_payload)
    )

    if response.status_code not in (200, 201):
        raise Exception(
            f"❌ Failed to create user: {response.status_code} - {response.text}"
        )

    user_object_id = response.json()["id"]
    return user_object_id
