from flask import Blueprint, jsonify, request
from data.crimes.validation import (
    validate_new_crime_data,
    validate_partial_crime_data
)
from data.crimes.process import process_crime_data
from app.queries.crimes import (
    get_reports_per_crime_code,
    get_reports_per_day_for_crime_code,
    get_top_three_crimes_per_area_for_day,
    get_two_least_common_crimes_per_day,
    get_weapons_used_for_same_crime_in_multiple_areas
)
from app.queries.upvotes import (
    get_top_fifty_upvoted_reports_for_day,
    get_top_fifty_active_officers,
    get_top_50_officers_by_unique_areas,
    get_reports_with_duplicate_email,
    get_areas_for_given_name
)
from data.upvotes.validation import (
    validate_upvote_data, 
    validate_officer_data, 
    validate_report_data   
)

crime_routes = Blueprint('crime_routes', __name__)

@crime_routes.route("/test", methods=["GET"])
def test_route():
    return jsonify({"message": "Test route works!"}), 200

# post a crime
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
    

# update a crime
@crime_routes.route("/crimes/<dr_no>", methods=["PUT"])
def update_crime(dr_no):
    updated_fields = request.json
    
    # check if the crime report exists
    existing_crime = crime_routes.mongo.db.crime_reports.find_one({"dr_no": dr_no})
    if not existing_crime:
        return jsonify({"error": f"Crime report with DR_NO {dr_no} not found."}), 404

    # validate only the fields that are being updated
    validation_error, status_code = validate_partial_crime_data(updated_fields, existing_crime)
    if validation_error:
        return jsonify(validation_error), status_code

    try:
        # update only the fields provided in the request
        crime_routes.mongo.db.crime_reports.update_one({"dr_no": dr_no}, {"$set": updated_fields})
        return jsonify({"message": f"Crime report with DR_NO {dr_no} updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# query 1
@crime_routes.route("/reports-per-crime-code", methods=["GET"])
def reports_per_crime_code():
    # extract date range from query parameters
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if not start_date or not end_date:
        return jsonify({"error": "Both start_date and end_date are required."}), 400

    try:
        # call the query function
        result = get_reports_per_crime_code(crime_routes.mongo.db, start_date, end_date)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# query 2
@crime_routes.route("/reports-per-day-for-crime-code", methods=["GET"])
def reports_per_day_for_crime_code():
    # extract parameters from query parameters
    crime_code = request.args.get("crime_code")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if not crime_code or not start_date or not end_date:
        return jsonify({"error": "crime_code, start_date, and end_date are required."}), 400

    try:
        # call the query function
        result = get_reports_per_day_for_crime_code(crime_routes.mongo.db, crime_code, start_date, end_date)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# query 3
@crime_routes.route("/top-three-crimes-per-area-for-day", methods=["GET"])
def top_three_crimes_per_area_for_day():
    # extract specific date from query parameters
    specific_date = request.args.get("specific_date")

    if not specific_date:
        return jsonify({"error": "specific_date is required."}), 400

    try:
        # call the query function
        result = get_top_three_crimes_per_area_for_day(crime_routes.mongo.db, specific_date)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# query 4
@crime_routes.route("/two-least-common-crimes-in-time-range", methods=["GET"])
def two_least_common_crimes_in_time_range():
    # extract date range from query parameters
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if not start_date or not end_date:
        return jsonify({"error": "Both start_date and end_date are required."}), 400

    try:
        # call the query function
        result = get_two_least_common_crimes_per_day(crime_routes.mongo.db, start_date, end_date)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# query 5
@crime_routes.route("/weapons-used-for-same-crime-in-multiple-areas", methods=["GET"])
def weapons_used_for_same_crime_in_multiple_areas():
    try:
        # call the query function
        result = get_weapons_used_for_same_crime_in_multiple_areas(crime_routes.mongo.db)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


 # query 6   
@crime_routes.route("/top-fifty-upvoted-reports-for-day", methods=["GET"])
def top_fifty_upvoted_reports_for_day():
    # extract specific date from query parameters
    specific_date = request.args.get("specific_date")

    if not specific_date:
        return jsonify({"error": "specific_date is required."}), 400

    try:
        # call the query function
        result = get_top_fifty_upvoted_reports_for_day(crime_routes.mongo.db, specific_date)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# query 7
@crime_routes.route("/top-fifty-active-officers", methods=["GET"])
def top_fifty_active_officers():

    try:
        # call the query function
        result = get_top_fifty_active_officers(crime_routes.mongo.db)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# query 8
@crime_routes.route("/top-fifty-officers-by-areas", methods=["GET"])
def top_fifty_officers_by_areas():

    try:
        # call the query function
        result = get_top_50_officers_by_unique_areas(crime_routes.mongo.db)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# query 9
@crime_routes.route("/reports-with-duplicate-email", methods=["GET"])
def reports_with_duplicate_email():

    try:
        # call the query function
        result = get_reports_with_duplicate_email(crime_routes.mongo.db)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# query 10
@crime_routes.route("/areas-for-given-name", methods=["GET"])
def areas_for_given_name():
    # extract specific date from query parameters
    name = request.args.get("name")

    if not name:
        return jsonify({"error": "name is required."}), 400

    try:
        # call the query function
        result = get_areas_for_given_name(crime_routes.mongo.db, name)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@crime_routes.route("/upvotes", methods=["POST"])
def create_upvote():
    # extract the upvote data from the request body
    upvote_data = request.json

    # validate the upvote data
    is_valid, error_message = validate_upvote_data(upvote_data)
    if not is_valid:
        return jsonify({"error": error_message}), 400

    # validate the officer data
    is_valid, error_message = validate_officer_data(upvote_data["officer"])
    if not is_valid:
        return jsonify({"error": error_message}), 400

    # validate the report data
    is_valid, error_message = validate_report_data(upvote_data["report"])
    if not is_valid:
        return jsonify({"error": error_message}), 400

    # check if the officer exists
    officer = crime_routes.mongo.db.police_officers.find_one({"badge_no": upvote_data["officer"]["badge_no"]})
    if not officer:
        return jsonify({"error": f"Officer with badge_no {upvote_data['officer']['badge_no']} not found."}), 404

    # check if the report exists
    report = crime_routes.mongo.db.crime_reports.find_one({"dr_no": upvote_data["report"]["dr_no"]})
    if not report:
        return jsonify({"error": f"Report with DR_NO {upvote_data['report']['dr_no']} not found."}), 404

    # check if the upvote already exists
    existing_upvote = crime_routes.mongo.db.upvotes.find_one({
        "officer.badge_no": upvote_data["officer"]["badge_no"],
        "report.dr_no": upvote_data["report"]["dr_no"]
    })
    if existing_upvote:
        return jsonify({"error": "Upvote already exists for this officer and report."}), 409

    try:
        # insert the new upvote record
        crime_routes.mongo.db.upvotes.insert_one(upvote_data)
        return jsonify({"message": "Upvote created successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500