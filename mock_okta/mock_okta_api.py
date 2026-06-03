# mock_okta_api.py

from typing import List, Optional
from .mock_okta_data import MockOktaDirectory, MockUser, MockGroup


class MockOktaAPI:
    """
    Simulates a subset of the Okta Management API:
    - Create/list users
    - Create/list groups
    - Add/remove user from group
    """

    def __init__(self, directory: Optional[MockOktaDirectory] = None):
        self.directory = directory or MockOktaDirectory()

    # ---------- User "endpoints" ----------

    def create_user(self, **user_kwargs) -> MockUser:
        """
        Simulates POST /api/v1/users
        """
        return self.directory.create_user(**user_kwargs)

    def list_users(self) -> List[MockUser]:
        """
        Simulates GET /api/v1/users
        """
        return self.directory.list_users()

    def get_user(self, user_id: str) -> Optional[MockUser]:
        """
        Simulates GET /api/v1/users/{id}
        """
        return self.directory.get_user(user_id)

    # ---------- Group "endpoints" ----------

    def create_group(self, name: str, description: str = "") -> MockGroup:
        """
        Simulates POST /api/v1/groups
        """
        return self.directory.create_group(name=name, description=description)

    def list_groups(self) -> List[MockGroup]:
        """
        Simulates GET /api/v1/groups
        """
        return self.directory.list_groups()

    def get_group(self, group_id: str) -> Optional[MockGroup]:
        """
        Simulates GET /api/v1/groups/{id}
        """
        return self.directory.get_group(group_id)

    # ---------- Group membership "endpoints" ----------

    def add_user_to_group(self, group_id: str, user_id: str) -> bool:
        """
        Simulates PUT /api/v1/groups/{groupId}/users/{userId}
        """
        user = self.directory.get_user(user_id)
        group = self.directory.get_group(group_id)

        if not user or not group:
            return False

        if group_id not in user.groups:
            user.groups.append(group_id)
        return True

    def remove_user_from_group(self, group_id: str, user_id: str) -> bool:
        """
        Simulates DELETE /api/v1/groups/{groupId}/users/{userId}
        """
        user = self.directory.get_user(user_id)
        group = self.directory.get_group(group_id)

        if not user or not group:
            return False

        if group_id in user.groups:
            user.groups.remove(group_id)
        return True

    def list_group_members(self, group_id: str) -> List[MockUser]:
        """
        Simulates GET /api/v1/groups/{groupId}/users
        """
        return [
            user for user in self.directory.list_users()
            if group_id in user.groups
        ]
    