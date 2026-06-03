Identity Automation Framework (Okta → Azure AD Provisioning Workflow)
A modular, end‑to‑end Identity Lifecycle Automation Framework that simulates an HR → Okta → Azure AD provisioning pipeline using:

Attribute‑Based Access Control (ABAC)

Microsoft Graph API

Automated group assignment

Audit logging

Mock Okta directory + rules engine

Modular Python architecture

This project is designed as a portfolio‑ready IAM engineering showcase, demonstrating real‑world identity workflows used in enterprise environments.

📌 Features
✔ End‑to‑End Identity Workflow
Processes a new hire from HR → Okta → Azure AD:

Load new hire JSON

Evaluate ABAC rules

Provision user in Azure AD

Assign groups

Write audit logs

✔ Attribute‑Based Access Control (ABAC)
Rules engine assigns access based on:

Department

Title

Location

Job level

✔ Azure AD Provisioning
Uses Microsoft Graph API to:

Create users

Set usage location

Assign temporary password

Return objectId

✔ Group Assignment
Automatically assigns Azure AD groups based on rules engine output.

✔ Audit Logging
Writes structured JSON logs to daily rotating log files.

✔ Mock Okta Directory
Simulates Okta user data + API behavior for testing.

📁 Project Structure
Code
.
│   .env.example
│   README.md
│   requirements.txt
│
├───azure
├───docs
├───mock_okta
│       mock_okta_api.py
│       mock_okta_data.py
│       __init__.py
│
├───Modules
│       graph_groups.py
│       graph_users.py
│       logger.py
│       okta_rules_engine.py
│
├───new_hires
│       newhire_engineer_tx.json
│       newhire_it_manager.json
│       newhire_pharmacy.json
│
├───runbooks
├───servicenow
├───tests
└───workflows
        identity_workflow.py
🧠 Architecture Overview
Code
          ┌────────────────────┐
          │   HR System (JSON) │
          └─────────┬──────────┘
                    │
                    ▼
        ┌──────────────────────────┐
        │   Mock Okta Directory    │
        │  (mock_okta_data/api)    │
        └─────────┬───────────────┘
                  │
                  ▼
        ┌──────────────────────────┐
        │   ABAC Rules Engine      │
        │ (okta_rules_engine.py)   │
        └─────────┬───────────────┘
                  │ groups[]
                  ▼
        ┌──────────────────────────┐
        │ Azure AD Provisioning    │
        │  (graph_users.py)        │
        └─────────┬───────────────┘
                  │ objectId
                  ▼
        ┌──────────────────────────┐
        │ Group Assignment          │
        │  (graph_groups.py)        │
        └─────────┬───────────────┘
                  │
                  ▼
        ┌──────────────────────────┐
        │   Audit Logging           │
        │    (logger.py)            │
        └──────────────────────────┘
🚀 Running the Workflow
1. Install dependencies
Code
pip install -r requirements.txt
2. Create your .env file
Copy .env.example → .env and fill in:

Code
AZURE_CLIENT_ID=
AZURE_CLIENT_SECRET=
AZURE_TENANT_ID=
3. Run the identity workflow
Code
python workflows/identity_workflow.py
The workflow will:

Load a new hire JSON

Evaluate access rules

Create the user in Azure AD

Assign groups

Write an audit log

🧪 Sample New Hire Files
Located in new_hires/:

newhire_pharmacy.json

newhire_it_manager.json

newhire_engineer_tx.json

Each file triggers different ABAC rule paths.

📜 Example Audit Log Entry
Code
{
    "timestamp": "2026-05-20T21:14:22.123Z",
    "userPrincipalName": "sarah.lopez@ledronesandrobotics.com",
    "provisionedObjectId": "a1b2c3d4-e5f6-7890",
    "groupsAssigned": [
        "GROUPID_PHARMA_USERS",
        "GROUPID_TEXAS_EMPLOYEES",
        "GROUPID_ALL_EMPLOYEES"
    ],
    "department": "Pharmacy",
    "title": "Pharmacy Technician",
    "location": "TX",
    "status": "Success"
}
🧩 Modules Overview
Modules/graph_users.py
Creates Azure AD users via Microsoft Graph.

Modules/graph_groups.py
Assigns users to Azure AD groups.

Modules/okta_rules_engine.py
Attribute‑based access control logic.

Modules/logger.py
Writes structured audit logs.

🛠 Skills Demonstrated
Identity Lifecycle Automation

Azure AD / Microsoft Graph API

Okta‑style rules engine

Attribute‑Based Access Control (ABAC)

Python modular architecture

Audit logging & compliance

Enterprise IAM patterns

Workflow orchestration

JSON‑based HRIS integration

This project is designed to be interview‑ready and demonstrates real‑world IAM engineering capabilities.