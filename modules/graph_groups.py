import requests
import os
from modules.graph_users import get_graph_token

GRAPH_API_URL = "https://graph.microsoft.com/v1.0"

def assign_user_to_groups(user_object_id: str, groups: list):
    """
    Assigns a user to one or more Azure AD groups.
    Accepts:
        user_object_id (str): The Azure AD objectId of the user
        groups (list): A list of Azure AD group objectIds
    """

    if not groups:
        print("⚠️ No groups to assign. Skipping group assignment.")
        return

    token = get_graph_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    for group_id in groups:
        url = f"{GRAPH_API_URL}/groups/{group_id}/members/$ref"

        payload = {
            "@odata.id": f"{GRAPH_API_URL}/directoryObjects/{user_object_id}"
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code not in (200, 204):
            print(f"❌ Failed to add user to group {group_id}: {response.text}")
        else:
            print(f"✅ Added user to group: {group_id}")
