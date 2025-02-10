from flask import Blueprint, jsonify, request
from data.crimes.validation import (
    validate_crime_data,
    validate_dr_no,
    validate_age,
    validate_sex,
    validate_descent,
    validate_coordinates
)
from data.crimes.process import process_crime_data

crime_routes = Blueprint('crime_routes', __name__)

@crime_routes.route("/test", methods=["GET"])
def test_route():
    return jsonify({"message": "Test route works!"}), 200

@crime_routes.route("/crimes", methods=["POST"])
def insert_crime():
    new_crime = request.json
    
    # validate the incoming crime data
    validation_error, status_code = validate_crime_data(new_crime)
    if validation_error:
        return jsonify(validation_error), status_code
    
    # process the crime data
    crime_report, error, status_code = process_crime_data(new_crime)
    if error:
        return jsonify(error), status_code
    
    try:
        crime_routes.mongo.db.crime_reports.insert_one(crime_report)
        return jsonify({"message": "Crime report added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@crime_routes.route("/crimes/<dr_no>", methods=["PUT"])
def update_crime(dr_no):
    updated_fields = request.json
    
    # check if the crime report exists
    existing_crime = crime_routes.mongo.db.crime_reports.find_one({"dr_no": dr_no})
    if not existing_crime:
        return jsonify({"error": f"Crime report with DR_NO {dr_no} not found."}), 404

    # Validate only the fields that are being updated
    validation_error, status_code = validate_partial_crime_data(updated_fields, existing_crime)
    if validation_error:
        return jsonify(validation_error), status_code

    try:
        # Update only the fields provided in the request
        crime_routes.mongo.db.crime_reports.update_one({"dr_no": dr_no}, {"$set": updated_fields})
        return jsonify({"message": f"Crime report with DR_NO {dr_no} updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
def validate_partial_crime_data(updated_fields, existing_crime):
    """
    Validate only the fields that are being updated.
    """
    errors = {}
    
    # validate 'dr_no' if it's being updated
    if "dr_no" in updated_fields:
        if not validate_dr_no(updated_fields["dr_no"]):
            errors["dr_no"] = "Invalid 'dr_no'. It must be a 9-digit number."

    # validate 'vict_age' if it's being updated
    if "vict_age" in updated_fields:
        if not validate_age(updated_fields["vict_age"]):
            errors["vict_age"] = "Invalid victim age."

    # validate 'vict_sex' if it's being updated
    if "vict_sex" in updated_fields:
        if not validate_sex(updated_fields["vict_sex"]):
            errors["vict_sex"] = "Invalid victim sex."

    # validate 'vict_descent' if it's being updated
    if "vict_descent" in updated_fields:
        if not validate_descent(updated_fields["vict_descent"]):
            errors["vict_descent"] = "Invalid victim descent."

    # validate 'lat' and 'lon' if they're being updated
    if "lat" in updated_fields or "lon" in updated_fields:
        lat = updated_fields.get("lat", existing_crime.get("lat"))
        lon = updated_fields.get("lon", existing_crime.get("lon"))
        if not validate_coordinates(lat, lon):
            errors["coordinates"] = "Invalid Latitude or/and longitude."

    if errors:
        return {"error": errors}, 400
    return None, None