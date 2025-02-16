import re

# helper functions for validation
def validate_dr_no(dr_no):
    """Validate that 'dr_no' is a 9-digit number."""
    return dr_no and re.match(r'^\d{9}$', str(dr_no))

def validate_age(age):
    """Validate that age is a 1-2 digit number between 0 and 99."""
    return age and re.match(r'^\d{1,2}$', age) and (0 <= int(age) <= 99)

def validate_sex(sex):
    """Validate that sex is one of 'F', 'M', or 'X'."""
    return sex in ['F', 'M', 'X']

def validate_descent(descent):
    """Validate that descent is one of the valid codes."""
    valid_descents = ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'O', 'P', 'S', 'U', 'V', 'W', 'X', 'Z']
    return descent in valid_descents

def validate_coordinates(lat, lon):
    """Validate that latitude and longitude are non-zero."""
    return lat != 0 and lon != 0

def validate_new_crime_data(new_crime):
    """Validate the incoming crime data."""
    if not new_crime:
        return {"error": "No data provided"}, 400

    dr_no = new_crime.get("dr_no")
    if not validate_dr_no(dr_no):
        return {"error": "Invalid 'dr_no'. It must be a 9-digit number."}, 400

    age = new_crime.get("vict_age")
    sex = new_crime.get("vict_sex")
    descent = new_crime.get("vict_descent")

    if not validate_age(age):
        return {"error": "Invalid victim age."}, 400
    if not validate_sex(sex):
        return {"error": "Invalid victim sex."}, 400
    if not validate_descent(descent):
        return {"error": "Invalid victim descent."}, 400

    lat = new_crime.get("lat")
    lon = new_crime.get("lon")
    if not validate_coordinates(lat, lon):
        return {"error": "Invalid Latitude or/and longitude"}, 400
    
    return None, None

# dictionary to map fields to their validation functions and error messages
VALIDATION_RULES = {
    "dr_no": (validate_dr_no, "Invalid 'dr_no'. It must be a 9-digit number."),
    "vict_age": (validate_age, "Invalid victim age."),
    "vict_sex": (validate_sex, "Invalid victim sex."),
    "vict_descent": (validate_descent, "Invalid victim descent."),
    "coordinates": (validate_coordinates, "Invalid Latitude or/and longitude."),
}

def validate_field(field_name, value, existing_data=None):
    """Validate a single field based on the validation rules."""
    if field_name == "coordinates":
        lat = value.get("lat") if isinstance(value, dict) else existing_data.get("lat")
        lon = value.get("lon") if isinstance(value, dict) else existing_data.get("lon")
        validation_func, error_message = VALIDATION_RULES[field_name]
        return validation_func(lat, lon), error_message
    else:
        validation_func, error_message = VALIDATION_RULES[field_name]
        return validation_func(value), error_message
    
def validate_new_crime_data(new_crime):
    """Validate the incoming crime data."""
    if not new_crime:
        return {"error": "No data provided"}, 400

    errors = {}
    for field, (validation_func, error_message) in VALIDATION_RULES.items():
        if field == "coordinates":
            lat = new_crime.get("lat")
            lon = new_crime.get("lon")
            if not validation_func(lat, lon):
                errors[field] = error_message
        else:
            value = new_crime.get(field)
            if value is not None and not validation_func(value):
                errors[field] = error_message

    if errors:
        return {"error": errors}, 400
    return None, None

def validate_partial_crime_data(updated_fields, existing_crime):
    """Validate only the fields that are being updated."""
    errors = {}
    
    for field in updated_fields:
        if field in VALIDATION_RULES:
            validation_func, error_message = VALIDATION_RULES[field]
            value = updated_fields[field]
            if field == "coordinates":
                lat = updated_fields.get("lat", existing_crime.get("lat"))
                lon = updated_fields.get("lon", existing_crime.get("lon"))
                if not validation_func(lat, lon):
                    errors[field] = error_message
            else:
                if not validation_func(value):
                    errors[field] = error_message

    if errors:
        return {"error": errors}, 400
    return None, None