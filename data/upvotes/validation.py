def validate_upvote_data(upvote_data):

    if not upvote_data:
        return False, "Upvote data is missing."
    
    required_fields = ["officer", "report", "upvote_date"]
    if not all(key in upvote_data for key in required_fields):
        return False, f"Missing required fields: {', '.join(required_fields)}"
    
    return True, ""

def validate_officer_data(officer_data):

    if not officer_data:
        return False, "Officer data is missing."
    
    required_fields = ["badge_no", "name", "email"]
    if not all(key in officer_data for key in required_fields):
        return False, f"Missing required officer fields: {', '.join(required_fields)}"
    
    return True, ""

def validate_report_data(report_data):

    if not report_data:
        return False, "Report data is missing."
    
    required_fields = ["dr_no", "area"]
    if not all(key in report_data for key in required_fields):
        return False, f"Missing required report fields: {', '.join(required_fields)}"
    
    return True, ""