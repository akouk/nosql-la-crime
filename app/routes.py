from flask import Blueprint, jsonify, request
from data.crimes.validation import (
    validate_new_crime_data,
    validate_partial_crime_data
)
from data.crimes.process import process_crime_data
from app.queries.reports_per_crm_cd import get_reports_per_crime_code
from app.queries.reports_per_day_for_crm_cd import get_reports_per_day_for_crime_code
from app.queries.top_three_crimes_per_area_for_day import get_top_three_crimes_per_area_for_day
from app.queries.two_least_common_crimes_per_day import get_two_least_common_crimes_per_day
from app.queries.weapons_used_for_same_crime_in_multiple_areas import get_weapons_used_for_same_crime_in_multiple_areas

crime_routes = Blueprint('crime_routes', __name__)

@crime_routes.route("/test", methods=["GET"])
def test_route():
    return jsonify({"message": "Test route works!"}), 200

@crime_routes.route("/crimes", methods=["POST"])
def insert_crime():
    new_crime = request.json
    
    # validate the incoming crime data
    validation_error, status_code = validate_new_crime_data(new_crime)
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

# query 1
@crime_routes.route("/reports-per-crime-code", methods=["GET"])
def reports_per_crime_code():
    # Extract date range from query parameters
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if not start_date or not end_date:
        return jsonify({"error": "Both start_date and end_date are required."}), 400

    try:
        # Call the query function
        result = get_reports_per_crime_code(crime_routes.mongo.db, start_date, end_date)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# query 2
@crime_routes.route("/reports-per-day-for-crime-code", methods=["GET"])
def reports_per_day_for_crime_code():
    # Extract parameters from query parameters
    crime_code = request.args.get("crime_code")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if not crime_code or not start_date or not end_date:
        return jsonify({"error": "crime_code, start_date, and end_date are required."}), 400

    try:
        # Call the query function
        result = get_reports_per_day_for_crime_code(crime_routes.mongo.db, crime_code, start_date, end_date)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# query 3
@crime_routes.route("/top-three-crimes-per-area-for-day", methods=["GET"])
def top_three_crimes_per_area_for_day():
    # Extract specific date from query parameters
    specific_date = request.args.get("specific_date")

    if not specific_date:
        return jsonify({"error": "specific_date is required."}), 400

    try:
        # Call the query function
        result = get_top_three_crimes_per_area_for_day(crime_routes.mongo.db, specific_date)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# query 4
@crime_routes.route("/two-least-common-crimes-in-time-range", methods=["GET"])
def two_least_common_crimes_in_time_range():
    # Extract date range from query parameters
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if not start_date or not end_date:
        return jsonify({"error": "Both start_date and end_date are required."}), 400

    try:
        # Call the query function
        result = get_two_least_common_crimes_per_day(crime_routes.mongo.db, start_date, end_date)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# query 5
@crime_routes.route("/weapons-used-for-same-crime-in-multiple-areas", methods=["GET"])
def weapons_used_for_same_crime_in_multiple_areas():
    try:
        # Call the query function
        result = get_weapons_used_for_same_crime_in_multiple_areas(crime_routes.mongo.db)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500