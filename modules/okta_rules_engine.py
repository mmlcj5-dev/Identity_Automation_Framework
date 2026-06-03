def evaluate_access_rules(new_hire: dict) -> dict:
    """
    Attribute-Based Access Control (ABAC) rules engine.
    Determines which Azure AD groups a user should be assigned to
    based on department, title, location, and job level.
    """

    department = new_hire.get("department", "").lower()
    title = new_hire.get("title", "").lower()
    location = new_hire.get("location", "").lower()
    job_level = new_hire.get("jobLevel", "").lower()

    groups = []

    # -----------------------------
    # Department-based access
    # -----------------------------
    if department == "pharmacy":
        groups.append("GROUPID_PHARMA_USERS")

    if department == "it":
        groups.append("GROUPID_IT_USERS")

    if department == "hr":
        groups.append("GROUPID_HR_USERS")

    # -----------------------------
    # Title-based access
    # -----------------------------
    if "manager" in title:
        groups.append("GROUPID_MANAGERS")

    if "director" in title:
        groups.append("GROUPID_DIRECTORS")

    if "engineer" in title:
        groups.append("GROUPID_ENGINEERS")

    # -----------------------------
    # Location-based access
    # -----------------------------
    if location == "tx":
        groups.append("GROUPID_TEXAS_EMPLOYEES")

    if location == "ca":
        groups.append("GROUPID_CALIFORNIA_EMPLOYEES")

    # -----------------------------
    # Job level-based access
    # -----------------------------
    if job_level in ["l3", "senior"]:
        groups.append("GROUPID_SENIOR_STAFF")

    if job_level in ["l1", "entry"]:
        groups.append("GROUPID_ENTRY_LEVEL")

    # -----------------------------
    # Always-on baseline access
    # -----------------------------
    groups.append("GROUPID_ALL_EMPLOYEES")

    return {
        "groups": groups
    }
