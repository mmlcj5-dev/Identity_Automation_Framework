import json
import os
import sys
from datetime import datetime

# --- Path setup ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODULES_DIR = os.path.join(ROOT_DIR, "modules")
for path in (MODULES_DIR, ROOT_DIR):
    if path not in sys.path:
        sys.path.insert(0, path)

# --- Imports ---
from modules.okta_rules_engine import evaluate_access_rules
from modules.graph_users import create_user_in_azure
from modules.graph_groups import assign_user_to_groups
import importlib.util

# Load logger module from project root to avoid import resolution issues in different
# runtime/static-analysis environments.
logger_path = os.path.join(ROOT_DIR, "logger.py")
spec = importlib.util.spec_from_file_location("logger", logger_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load logger module from {logger_path}")
logger = importlib.util.module_from_spec(spec)
spec.loader.exec_module(logger)
write_audit_log = logger.write_audit_log


def run_identity_workflow(new_hire_file: str):
    """
    Main orchestrator for the identity lifecycle workflow.
    Reads new hire data → evaluates access rules → provisions Azure AD user → assigns groups → logs results.
    """

    print("\n🚀 Starting Identity Workflow...\n")

    # 1. Load new hire data
    with open(new_hire_file, "r") as f:
        new_hire = json.load(f)

    print(f"📄 Loaded new hire file: {new_hire_file}")
    print(f"👤 Processing: {new_hire['firstName']} {new_hire['lastName']}")

    # 2. Evaluate access rules (ABAC)
    print("\n🔎 Evaluating access rules...")
    access_result = evaluate_access_rules(new_hire)
    groups_to_assign = access_result["groups"]

    print(f"📌 Groups determined by rules engine: {groups_to_assign}")

    # 3. Provision user in Azure AD
    print("\n🧩 Creating user in Azure AD...")
    user_object_id = create_user_in_azure(new_hire)
    print(f"✅ User created in Azure AD with objectId: {user_object_id}")

    # 4. Assign groups
    print("\n👥 Assigning groups...")
    assign_user_to_groups(user_object_id, groups_to_assign)
    print("✅ Group assignments complete.")

    # 5. Write audit log
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "userPrincipalName": new_hire["userPrincipalName"],
        "provisionedObjectId": user_object_id,
        "groupsAssigned": groups_to_assign,
        "department": new_hire.get("department"),
        "title": new_hire.get("title"),
        "location": new_hire.get("location"),
        "onboardingCost": new_hire.get("onboardingCost", 0),
        "status": "Success"
    }

    write_audit_log(log_entry)
    print("\n📝 Audit log written.")
    print("\n🎉 Identity workflow completed successfully!\n")


def run_all_new_hires():
    """
    Batch processor for all new hire JSON files.
    Iterates through /new_hires folder and runs the identity workflow for each file.
    """
    folder = os.path.join(ROOT_DIR, "new_hires")
    print(f"\n📂 Scanning folder: {folder}")

    for file_name in os.listdir(folder):
        if file_name.endswith(".json"):
            file_path = os.path.join(folder, file_name)
            print(f"\n🚀 Starting workflow for {file_name}")
            try:
                run_identity_workflow(file_path)
                write_audit_log({
                    "timestamp": datetime.utcnow().isoformat(),
                    "fileProcessed": file_name,
                    "status": "BatchSuccess"
                })
            except Exception as e:
                write_audit_log({
                    "timestamp": datetime.utcnow().isoformat(),
                    "fileProcessed": file_name,
                    "status": "BatchError",
                    "error": str(e)
                })
                print(f"❌ Error processing {file_name}: {e}")


if __name__ == "__main__":
    # Run all new hires automatically
    run_all_new_hires()
