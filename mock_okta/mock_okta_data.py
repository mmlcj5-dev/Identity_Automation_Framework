# mock_okta_data.py

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import uuid


@dataclass
class MockUser:
    id: str
    first_name: str
    last_name: str
    email: str
    department: str
    title: Optional[str] = None
    manager_email: Optional[str] = None
    groups: List[str] = field(default_factory=list)


@dataclass
class MockGroup:
    id: str
    name: str
    description: str = ""


class MockOktaDirectory:
    def __init__(self):
        self.users: Dict[str, MockUser] = {}
        self.groups: Dict[str, MockGroup] = {}

    # ---------- User helpers ----------

    def create_user(self, first_name: str, last_name: str, email: str,
                    department: str, title: str = "", manager_email: str = "") -> MockUser:
        user_id = str(uuid.uuid4())
        user = MockUser(
            id=user_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            department=department,
            title=title or None,
            manager_email=manager_email or None,
        )
        self.users[user_id] = user
        return user

    def get_user(self, user_id: str) -> Optional[MockUser]:
        return self.users.get(user_id)

    def list_users(self) -> List[MockUser]:
        return list(self.users.values())

    # ---------- Group helpers ----------

    def create_group(self, name: str, description: str = "") -> MockGroup:
        group_id = str(uuid.uuid4())
        group = MockGroup(id=group_id, name=name, description=description)
        self.groups[group_id] = group
        return group

    def get_group(self, group_id: str) -> Optional[MockGroup]:
        return self.groups.get(group_id)

    def list_groups(self) -> List[MockGroup]:
        return list(self.groups.values())


# Convenience factory for demos/tests
def create_sample_directory() -> MockOktaDirectory:
    directory = MockOktaDirectory()

    # Sample groups
    finance_group = directory.create_group("Finance", "Finance department access")
    it_group = directory.create_group("IT", "IT department access")
    hr_group = directory.create_group("HR", "HR department access")

    # Sample users
    directory.create_user(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        department="Finance",
        title="Analyst",
        manager_email="manager.finance@example.com",
    )
    directory.create_user(
        first_name="Jane",
        last_name="Smith",
        email="jane.smith@example.com",
        department="IT",
        title="Systems Engineer",
        manager_email="manager.it@example.com",
    )
    directory.create_user(
        first_name="Emily",
        last_name="Clark",
        email="emily.clark@example.com",
        department="HR",
        title="HR Generalist",
        manager_email="manager.hr@example.com",
    )

    return directory