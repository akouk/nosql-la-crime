from data.crimes.validation import validate_crime_data

def create_area_data(new_crime):
    """Create area data from the crime data."""
    return {
        "no": new_crime.get("area"),
        "name": new_crime.get("area_name"),
        "report_dist_no": new_crime.get("rpt_dist_no")
    }
    
def create_victim_data(new_crime):
    """Create victim data from the crime data."""
    return {
        "age": new_crime.get("vict_age"),
        "sex": new_crime.get("vict_sex"),
        "descent": new_crime.get("vict_descent")
    }
    
def create_weapon_data(new_crime):
    """Create weapon data from the crime data if it exists."""
    if new_crime.get("weapon_used_cd") and new_crime.get("weapon_desc"):
        return {
            "code": new_crime.get("weapon_used_cd"),
            "description": new_crime.get("weapon_desc")
        }
    return {}

def create_crime_codes(new_crime):
    """Create crime codes data from the crime data."""
    crime_codes = {
        new_crime.get("crm_cd"): 1,
        new_crime.get("crm_cd_2"): 2,
        new_crime.get("crm_cd_3"): 3,
        new_crime.get("crm_cd_4"): 4
    }
    description = new_crime.get("crm_cd_desc", None)

    crime_data = []
    for code, severity in crime_codes.items():
        if code:  # only add if the code is not None
            crime_data.append({
                "severity": severity,
                "code": code,
                "description": description if code == new_crime.get("crm_cd") else None
            })
            
    return crime_data
    
def create_location_data(new_crime):
    """Create location data from the crime data."""
    street = new_crime.get("cross_street") if new_crime.get("cross_street") else None

    return {
        "premis": {
            "code": new_crime.get("premis_cd"),
            "description": new_crime.get("premis_desc")
        },
        "location": new_crime.get("location"),
        "street": street,
        "coordinates": {
            "latitude": new_crime.get("lat"),
            "longitude": new_crime.get("lon")
        }
    }
    
def create_status_data(new_crime):
    """Create status data from the crime data."""
    status_code = new_crime.get("status", "IC")  # default to "IC" if not provided
    status_description = new_crime.get("status_desc", "Invest Cont")  # default to "Invest Cont" if not provided

    return {
        "code": status_code,
        "description": status_description
    }
    
def process_crime_data(new_crime):
    """Process and validate crime data to create a crime report."""
    validation_error, status_code = validate_crime_data(new_crime)
    if validation_error:
        return None, validation_error, status_code

    # create full crime report doc
    crime_report = {
        "dr_no": new_crime.get("dr_no"),
        "date_reported": new_crime.get("date_rptd"),
        "date_occurred": new_crime.get("date_occ"),
        "time_occurred": new_crime.get("time_occ"),
        "area": create_area_data(new_crime),
        "crime": create_crime_codes(new_crime),
        "mocodes": new_crime.get("mocodes"),
        "victim": create_victim_data(new_crime),
        "weapon": create_weapon_data(new_crime),
        "location": create_location_data(new_crime),
        "status": create_status_data(new_crime),
    }
    
    return crime_report, None, None