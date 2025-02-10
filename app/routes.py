from flask import Blueprint, jsonify, request
from data.crimes.validation import validate_crime_data
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
    updated_crime = request.json

    # validate the incoming crime data
    validation_error, status_code = validate_crime_data(updated_crime)
    if validation_error:
        return jsonify(validation_error), status_code

    # process the updated crime data
    crime_report, error, status_code = process_crime_data(updated_crime)
    if error:
        return jsonify(error), status_code

    # check if the crime report exists
    existing_crime = crime_routes.mongo.db.crime_reports.find_one({"dr_no": dr_no})
    if not existing_crime:
        return jsonify({"error": f"Crime report with DR_NO {dr_no} not found."}), 404

    try:
        # update the crime report in the database
        crime_routes.mongo.db.crime_reports.update_one({"dr_no": dr_no}, {"$set": crime_report})
        return jsonify({"message": f"Crime report with DR_NO {dr_no} updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500