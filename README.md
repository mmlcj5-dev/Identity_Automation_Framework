# 🛩️ Identity Automation Framework
### NTX Aerial · ntxaerial.com

![Version](https://img.shields.io/badge/version-2.0.0-blue?style=flat-square)
![Status](https://img.shields.io/badge/status-active-brightgreen?style=flat-square)
![Domain](https://img.shields.io/badge/domain-ntxaerial.com-0078D4?style=flat-square)
![Python](https://img.shields.io/badge/python-3.11%2B-yellow?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square)

---

> **Automated identity lifecycle management for NTX Aerial.**  
> Provisions user accounts in Azure AD / Microsoft Entra ID and on-premises Active Directory via the Microsoft Graph API — triggered by role-specific JSON payloads and logged to a structured audit trail.

---

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [Architecture Diagram](#-architecture-diagram)
3. [Technology Stack](#-technology-stack)
4. [Repository Structure](#-repository-structure)
5. [Prerequisites](#-prerequisites)
6. [Setup & Installation](#-setup--installation)
7. [Environment Configuration (.env)](#-environment-configuration-env)
8. [Workflow Steps](#-workflow-steps)
9. [Module Explanations](#-module-explanations)
10. [New Hire JSON Payloads](#-new-hire-json-payloads)
11. [Audit Log Examples](#-audit-log-examples)
12. [Running the Framework](#-running-the-framework)
13. [Error Handling](#-error-handling)
14. [Security Notes](#-security-notes)
15. [Roadmap](#-roadmap)
16. [License](#-license)

---

## 🎯 Project Overview

The **Identity Automation Framework** is a Python-based CLI tool built for NTX Aerial's IT operations. It reads structured new hire JSON payloads and executes a deterministic provisioning workflow — creating user accounts in Azure AD / Entra ID, assigning the correct security groups, and sending onboarding notifications via Outlook/SMTP.

A local **Okta rules engine** (`okta_rules_engine.py`) simulates Okta-style policy logic for role-to-group mapping and access-tier assignment without requiring an active Okta subscription — enabling consistent policy enforcement and full testability via the `mock_okta` layer.

### Core Capabilities

| Capability | Description |
|---|---|
| **New Hire Provisioning** | Creates Entra ID / Azure AD accounts from role-specific JSON payloads |
| **Role-Based Group Assignment** | Maps NTX Aerial job roles to Azure AD security groups via rules engine |
| **On-Prem AD Sync** | Provisions accounts into local Active Directory for facility/network access |
| **Email Notifications** | Sends onboarding confirmation via SMTP / Microsoft 365 Outlook |
| **Audit Logging** | Structured JSON log entry written per provisioning event |
| **Mock Okta Testing** | Local Okta simulation layer for dry-run and development testing |

---

## 🏗️ Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│              IDENTITY AUTOMATION FRAMEWORK                   │
│                    ntxaerial.com                             │
└──────────────────────────┬───────────────────────────────────┘
                           │
          ┌────────────────▼───────────────┐
          │         TRIGGER (CLI)          │
          │  python identity_workflow.py   │
          │  --payload new_hires/*.json    │
          └────────────────┬───────────────┘
                           │
          ┌────────────────▼───────────────┐
          │      PAYLOAD INGESTION         │
          │  • Load & validate JSON        │
          │  • Normalize fields            │
          │  • Detect duplicates           │
          └────────────────┬───────────────┘
                           │
          ┌────────────────▼───────────────┐
          │      OKTA RULES ENGINE         │
          │  (modules/okta_rules_engine.py)│
          │  • Map role → AD groups        │
          │  • Evaluate access tier        │
          │  • Apply shift-based conditons │
          └──────┬─────────────────┬───────┘
                 │                 │
   ┌─────────────▼──┐       ┌──────▼──────────────┐
   │  GRAPH USERS   │       │   GRAPH GROUPS       │
   │  (Entra ID)    │       │   (Entra ID)         │
   │                │       │                      │
   │ • Create user  │       │ • Add to dept group  │
   │ • Set UPN      │       │ • Add to role group  │
   │ • Assign mgr   │       │ • Add to all-staff   │
   │ • Set password │       └──────────────────────┘
   └────────┬───────┘
            │
   ┌────────▼───────────────────────────┐
   │     ON-PREM ACTIVE DIRECTORY       │
   │  • Sync account for facility/VPN   │
   │  • Apply OU placement              │
   └────────┬───────────────────────────┘
            │
   ┌────────▼───────────────────────────┐
   │       NOTIFICATIONS & AUDIT        │
   │  • SMTP/Outlook welcome email      │
   │  • JSON audit log append           │
   └────────────────────────────────────┘
```

---

## 🧰 Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| Identity Platform | Azure AD / Microsoft Entra ID |
| Directory (on-prem) | Active Directory (Windows Server) |
| Graph API Client | `msal`, `requests` (Microsoft Graph v1.0) |
| Rules Engine | Local `okta_rules_engine.py` (Okta-style policy, no subscription required) |
| Mock Layer | `mock_okta/` (dry-run and dev testing) |
| Email | SMTP via Microsoft 365 / Outlook |
| Logging | Python `logging` + custom `logger.py` → JSON output |
| Config | `python-dotenv` |

---

## 📁 Repository Structure

```
Identity_Automation_Framework/
│
├── .env                        # Active environment variables (gitignored)
├── .env.example                # Safe template — commit this, not .env
├── .gitignore
├── README.md
├── requirements.txt
├── __init__.py
│
├── modules/                    # Core processing modules
│   ├── graph_users.py          # Microsoft Graph API — user lifecycle operations
│   ├── graph_groups.py         # Microsoft Graph API — group membership operations
│   ├── logger.py               # Structured JSON audit logger
│   ├── okta_rules_engine.py    # Local role-to-group policy rules engine
│   └── __init__.py
│
├── mock_okta/                  # Mock Okta layer for dev/dry-run testing
│   ├── mock_okta_api.py        # Simulated Okta API responses
│   ├── mock_okta_data.py       # Static mock user/group data fixtures
│   └── __init__.py
│
├── workflows/
│   ├── identity_workflow.py    # Main provisioning orchestrator (CLI entrypoint)
│   └── __init__.py
│
├── new_hires/                  # Role-specific JSON provisioning payloads
│   ├── newhire_admin.json
│   ├── newhire_asst_manager.json
│   ├── newhire_clerk_day.json
│   ├── newhire_clerk_night.json
│   ├── newhire_drone_pilot.json
│   ├── newhire_manager.json
│   ├── newhire_robotics_tech.json
│   └── newhire_warehouse.json
│
├── azure/          # [Planned] ARM templates / Bicep / Azure config
├── docs/           # [Planned] Extended documentation
├── logs/           # Runtime audit logs (gitignored)
├── runbooks/       # [Planned] IT operational runbooks
├── servicenow/     # [Planned] ServiceNow integration module
└── tests/          # [Planned] pytest unit & integration tests
```

---

## ✅ Prerequisites

- **Python 3.11 or higher**
- **Azure AD / Entra ID App Registration** with the following Graph API permissions (Application type, admin-consented):
  - `User.ReadWrite.All`
  - `Group.ReadWrite.All`
  - `Directory.ReadWrite.All`
- **On-premises Active Directory** accessible from the host machine
- **Microsoft 365 / Outlook** SMTP relay credentials (`smtp.office365.com`)
- A dedicated **service account** for on-prem AD writes (`svc_provisioner@ntxaerial.local`)

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```powershell
git clone https://github.com/ntxaerial/identity-automation-framework.git
cd Identity_Automation_Framework
```

### 2. Create a Virtual Environment

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```powershell
copy .env.example .env
# Edit .env with your tenant credentials — see section below
```

### 5. Verify Graph API Connectivity

```powershell
python -c "from modules.graph_users import get_access_token; print(get_access_token())"
```

Expected output:
```
✅ Token acquired — Tenant: ntxaerial.onmicrosoft.com
```

---

## 🔐 Environment Configuration (.env)

Copy `.env.example` → `.env`. **Never commit `.env` to source control — it is gitignored.**

```dotenv
# ─────────────────────────────────────────────────────────
#  NTX AERIAL — IDENTITY AUTOMATION FRAMEWORK
#  Environment Configuration · ntxaerial.com
# ─────────────────────────────────────────────────────────

# ── Application ───────────────────────────────────────────
APP_ENV=production
APP_NAME=NTX Aerial Identity Automation
PRIMARY_DOMAIN=ntxaerial.com
LOG_LEVEL=INFO
AUDIT_LOG_PATH=logs/audit.jsonl
DRY_RUN=false

# ── Azure AD / Microsoft Entra ID ─────────────────────────
AZURE_TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
AZURE_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
AZURE_CLIENT_SECRET=your-client-secret-here
AZURE_AUTHORITY=https://login.microsoftonline.com/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
AZURE_GRAPH_ENDPOINT=https://graph.microsoft.com/v1.0
AZURE_UPN_DOMAIN=ntxaerial.com

# ── On-Premises Active Directory ──────────────────────────
AD_SERVER=dc01.ntxaerial.local
AD_DOMAIN=ntxaerial.local
AD_BIND_USER=svc_provisioner@ntxaerial.local
AD_BIND_PASSWORD=your-ad-service-account-password
AD_BASE_DN=DC=ntxaerial,DC=local
AD_USERS_OU=OU=NTXStaff,DC=ntxaerial,DC=local

# ── SMTP / Microsoft 365 Email ────────────────────────────
SMTP_HOST=smtp.office365.com
SMTP_PORT=587
SMTP_USE_TLS=true
SMTP_USER=noreply@ntxaerial.com
SMTP_PASSWORD=your-smtp-password-here
SMTP_FROM_NAME=NTX Aerial IT Operations
SMTP_FROM_ADDRESS=noreply@ntxaerial.com

# ── Mock Okta (Dev / Dry-Run Only) ────────────────────────
USE_MOCK_OKTA=false
MOCK_OKTA_BASE_URL=http://localhost:8080
```

> ⚠️ Set `DRY_RUN=true` to run the full workflow through the `mock_okta` layer with zero live API calls — safe for dev and demos.

---

## 🔄 Workflow Steps

Executed sequentially by `workflows/identity_workflow.py`.

```
STEP 01  ─  Load Payload
           └─ Read and parse the target new hire JSON from new_hires/

STEP 02  ─  Validate Fields
           └─ Enforce required fields, normalize name casing, verify start_date

STEP 03  ─  Run Okta Rules Engine
           └─ Map job_title + department + shift → Azure AD group list + access tier
              Uses mock_okta layer when DRY_RUN=true

STEP 04  ─  Create Entra ID / Azure AD User
           └─ graph_users.py — POST /users
              UPN format: firstname.lastname@ntxaerial.com

STEP 05  ─  Assign Azure AD Group Memberships
           └─ graph_groups.py — POST /groups/{id}/members for each resolved group

STEP 06  ─  Provision On-Prem Active Directory Account
           └─ Create AD user in correct OU, set department + manager + password policy

STEP 07  ─  Send Welcome Email
           └─ SMTP via smtp.office365.com → employee's personal_email on record

STEP 08  ─  Write Audit Log Entry
           └─ logger.py — Append structured JSON record to logs/audit.jsonl
```

---

## 🧩 Module Explanations

### `modules/graph_users.py`
Handles all Microsoft Graph API user object operations. Acquires an MSAL access token using client credentials flow, then calls Graph v1.0 endpoints to create users, set UPNs in the `@ntxaerial.com` domain, assign managers, and configure initial password policies. Also supports suspension and deletion for future offboarding use.

### `modules/graph_groups.py`
Manages Azure AD security group membership via the Graph API. Accepts the list of group IDs resolved by the rules engine and adds the new user as a member of each. Handles de-duplication and Graph pagination for group lookups.

### `modules/okta_rules_engine.py`
A **local policy rules engine** that replicates Okta-style logic without requiring an Okta subscription. Takes `job_title`, `department`, and `shift` as inputs and returns the correct Azure AD group IDs, access tier, and any conditional flags — for example, routing day vs. night clerks into separate shift-scoped groups. This is the policy brain of the framework. Edit this file to add or modify role-to-group mappings.

### `modules/logger.py`
Wraps Python's `logging` module with a JSON formatter. Writes structured audit entries to `logs/audit.jsonl` with ISO 8601 timestamps, event type, outcome, groups assigned, and target identity. Appends to the log on each run rather than overwriting.

### `mock_okta/mock_okta_api.py`
Simulates Okta REST API responses locally. When `DRY_RUN=true`, the workflow routes through this module instead of making live Graph API calls — safe for development, CI testing, and demonstrations without touching production credentials.

### `mock_okta/mock_okta_data.py`
Static fixture data used by `mock_okta_api.py` — includes pre-defined mock users, groups, and policy outcomes covering the full NTX Aerial role catalog.

### `workflows/identity_workflow.py`
The CLI entrypoint and main orchestrator. Imports all modules, reads the specified JSON payload, and executes Steps 1–8 in sequence. Catches and logs per-step exceptions, continues where possible on non-critical failures, and exits with a non-zero code on critical errors for CI/CD pipeline compatibility.

---

## 📄 New Hire JSON Payloads

All payload files live in `new_hires/`. Each role has its own template pre-configured with the correct department, shift, and access tier.

### `newhire_drone_pilot.json`

```json
{
  "trigger": "new_hire",
  "submitted_at": "2026-06-03T09:00:00-05:00",
  "submitted_by": "hr@ntxaerial.com",
  "employee": {
    "first_name": "Jordan",
    "last_name": "Reyes",
    "preferred_name": "Jordan",
    "personal_email": "jordan.reyes.personal@email.com",
    "personal_phone": "+1-972-555-0147",
    "job_title": "Drone Pilot",
    "department": "Flight Operations",
    "shift": "day",
    "location": "Frisco, TX",
    "employment_type": "full_time",
    "start_date": "2026-06-16",
    "reports_to_email": "ops.manager@ntxaerial.com",
    "certifications": ["FAA Part 107"],
    "access_tier": "field_operations"
  }
}
```

> **Generated UPN:** `jordan.reyes@ntxaerial.com`  
> **Groups:** `grp-flight-ops`, `grp-field-staff`, `grp-all-staff`

---

### `newhire_robotics_tech.json`

```json
{
  "trigger": "new_hire",
  "submitted_at": "2026-06-03T10:00:00-05:00",
  "submitted_by": "hr@ntxaerial.com",
  "employee": {
    "first_name": "Marcus",
    "last_name": "Tillman",
    "preferred_name": "Marc",
    "personal_email": "m.tillman@email.com",
    "personal_phone": "+1-214-555-0391",
    "job_title": "Robotics Technician",
    "department": "Engineering",
    "shift": "day",
    "location": "Frisco, TX",
    "employment_type": "full_time",
    "start_date": "2026-06-16",
    "reports_to_email": "engineering.lead@ntxaerial.com",
    "certifications": [],
    "access_tier": "engineering"
  }
}
```

> **Generated UPN:** `marcus.tillman@ntxaerial.com`  
> **Groups:** `grp-engineering`, `grp-tech-staff`, `grp-all-staff`

---

### `newhire_warehouse.json`

```json
{
  "trigger": "new_hire",
  "submitted_at": "2026-06-03T11:00:00-05:00",
  "submitted_by": "hr@ntxaerial.com",
  "employee": {
    "first_name": "Denise",
    "last_name": "Okafor",
    "preferred_name": "Denise",
    "personal_email": "denise.okafor@email.com",
    "personal_phone": "+1-469-555-0827",
    "job_title": "Warehouse Associate",
    "department": "Logistics",
    "shift": "day",
    "location": "Frisco, TX",
    "employment_type": "full_time",
    "start_date": "2026-06-16",
    "reports_to_email": "warehouse.supervisor@ntxaerial.com",
    "certifications": [],
    "access_tier": "logistics_standard"
  }
}
```

> **Generated UPN:** `denise.okafor@ntxaerial.com`  
> **Groups:** `grp-logistics`, `grp-warehouse`, `grp-all-staff`

---

### `newhire_clerk_night.json` — Shift-Aware Access

```json
{
  "trigger": "new_hire",
  "submitted_at": "2026-06-03T11:30:00-05:00",
  "submitted_by": "hr@ntxaerial.com",
  "employee": {
    "first_name": "Anthony",
    "last_name": "Cruz",
    "preferred_name": "Tony",
    "personal_email": "a.cruz@email.com",
    "personal_phone": "+1-972-555-0044",
    "job_title": "Operations Clerk",
    "department": "Logistics",
    "shift": "night",
    "location": "Frisco, TX",
    "employment_type": "full_time",
    "start_date": "2026-06-23",
    "reports_to_email": "night.supervisor@ntxaerial.com",
    "certifications": [],
    "access_tier": "logistics_limited"
  }
}
```

> **Generated UPN:** `anthony.cruz@ntxaerial.com`  
> **Groups:** `grp-logistics`, `grp-clerks-night`, `grp-all-staff`  
> The `shift: "night"` field triggers a conditional branch in `okta_rules_engine.py` that assigns `grp-clerks-night` instead of `grp-clerks-day`.

---

## 📋 Audit Log Examples

`logs/audit.jsonl` — newline-delimited JSON, one record per provisioning event. Gitignored at runtime.

### Successful Provisioning

```json
{
  "timestamp": "2026-06-03T09:47:22.341-05:00",
  "event_type": "USER_PROVISIONED",
  "outcome": "SUCCESS",
  "triggered_by": "hr@ntxaerial.com",
  "target": {
    "display_name": "Jordan Reyes",
    "upn": "jordan.reyes@ntxaerial.com",
    "job_title": "Drone Pilot",
    "department": "Flight Operations",
    "access_tier": "field_operations"
  },
  "steps_completed": [
    "LOAD_PAYLOAD", "VALIDATE_FIELDS", "RUN_RULES_ENGINE",
    "CREATE_ENTRA_USER", "ASSIGN_AD_GROUPS",
    "PROVISION_ONPREM_AD", "SEND_WELCOME_EMAIL"
  ],
  "groups_assigned": ["grp-flight-ops", "grp-field-staff", "grp-all-staff"],
  "dry_run": false,
  "duration_ms": 5214
}
```

### Partial Failure — Graph API Error

```json
{
  "timestamp": "2026-06-03T10:52:11.907-05:00",
  "event_type": "USER_PROVISIONED",
  "outcome": "PARTIAL_FAILURE",
  "triggered_by": "hr@ntxaerial.com",
  "target": {
    "display_name": "Marcus Tillman",
    "upn": "marcus.tillman@ntxaerial.com",
    "job_title": "Robotics Technician",
    "department": "Engineering"
  },
  "steps_completed": [
    "LOAD_PAYLOAD", "VALIDATE_FIELDS",
    "RUN_RULES_ENGINE", "CREATE_ENTRA_USER"
  ],
  "steps_failed": [
    {
      "step": "ASSIGN_AD_GROUPS",
      "error": "GraphAPIError: 403 Forbidden — insufficient privileges for group write",
      "manual_action_required": true
    }
  ],
  "dry_run": false,
  "duration_ms": 18340
}
```

### Dry-Run Entry (Mock Okta Layer)

```json
{
  "timestamp": "2026-06-03T14:10:00.000-05:00",
  "event_type": "USER_PROVISIONED",
  "outcome": "SUCCESS",
  "triggered_by": "it-dev@ntxaerial.com",
  "target": {
    "display_name": "Denise Okafor",
    "upn": "denise.okafor@ntxaerial.com",
    "job_title": "Warehouse Associate",
    "department": "Logistics"
  },
  "steps_completed": [
    "LOAD_PAYLOAD", "VALIDATE_FIELDS", "RUN_RULES_ENGINE",
    "CREATE_ENTRA_USER", "ASSIGN_AD_GROUPS",
    "PROVISION_ONPREM_AD", "SEND_WELCOME_EMAIL"
  ],
  "groups_assigned": ["grp-logistics", "grp-warehouse", "grp-all-staff"],
  "dry_run": true,
  "mock_okta_used": true,
  "duration_ms": 312
}
```

---

## 🚀 Running the Framework

```powershell
# Activate virtual environment
.venv\Scripts\activate

# Provision a single role payload
python workflows/identity_workflow.py --payload new_hires/newhire_drone_pilot.json

# Dry-run using mock Okta layer (no live API calls)
python workflows/identity_workflow.py --payload new_hires/newhire_drone_pilot.json --dry-run

# Batch provision all new hire payloads
for %f in (new_hires\*.json) do python workflows/identity_workflow.py --payload %f
```

**Expected console output:**

```
[2026-06-03 09:47:18] INFO    Loading payload: newhire_drone_pilot.json
[2026-06-03 09:47:18] INFO    Validated: Jordan Reyes | Drone Pilot | Flight Operations
[2026-06-03 09:47:18] INFO    Rules engine resolved 3 groups: grp-flight-ops, grp-field-staff, grp-all-staff
[2026-06-03 09:47:19] INFO    Entra ID user created: jordan.reyes@ntxaerial.com
[2026-06-03 09:47:20] INFO    Group memberships assigned (3/3)
[2026-06-03 09:47:21] INFO    On-prem AD account provisioned
[2026-06-03 09:47:22] INFO    Welcome email sent → jordan.reyes.personal@email.com
[2026-06-03 09:47:22] INFO    Audit log entry written
[2026-06-03 09:47:22] SUCCESS Provisioning complete in 4.1s
```

---

## ⚠️ Error Handling

| Failure Point | Behavior |
|---|---|
| Invalid or missing JSON field | Exits at validation; no API calls made |
| Graph API 401 Unauthorized | Token refresh attempted once; exits on second failure |
| Graph API 403 Forbidden | Step logged as `PARTIAL_FAILURE`; remaining steps continue |
| Graph API 429 Rate Limited | Auto-retry with 30s backoff (max 3 retries) |
| On-prem AD unreachable | Step skipped and flagged in audit log |
| SMTP send failure | Logged as warning; provisioning not rolled back |

---

## 🔒 Security Notes

- `.env` is gitignored — **never commit live credentials**
- Use a **dedicated service account** (`svc_provisioner@ntxaerial.local`) with least-privilege AD write permissions
- The **App Registration** should hold only the three Graph API permissions listed in Prerequisites — avoid Global Admin assignment
- `DRY_RUN=true` is safe for demos and CI — uses mock layer, zero live API calls
- **Rotate `AZURE_CLIENT_SECRET` every 90 days** — add a calendar reminder

---

## 🗺️ Roadmap

- [x] Microsoft Graph API user provisioning (Entra ID)
- [x] Azure AD group assignment via rules engine
- [x] On-prem Active Directory provisioning
- [x] Local Okta rules engine (no subscription required)
- [x] Mock Okta dry-run layer
- [x] Role-specific JSON payload templates (8 roles)
- [x] Structured JSON audit logging
- [ ] `tests/` — pytest unit tests for all modules
- [ ] `runbooks/` — step-by-step IT operational runbooks
- [ ] `azure/` — ARM / Bicep templates for Entra ID App Registration setup
- [ ] `servicenow/` — Auto-create incident on provisioning failure
- [ ] `docs/` — Extended architecture and operations documentation
- [ ] Offboarding workflow (account suspension + AD disable)

---

## 📄 License

MIT License — see [`LICENSE`](LICENSE) for details.

---

<div align="center">

**Built for NTX Aerial · [ntxaerial.com](https://ntxaerial.com)**  
IT Operations & Infrastructure · Frisco, TX

*Automating identity. Empowering teams.*

</div>
