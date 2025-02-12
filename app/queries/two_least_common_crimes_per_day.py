from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta

crime_routes = Blueprint('crime_routes', __name__)

def get_two_least_common_crimes_per_day(db, start_date, end_date):
    """
    Find the two least common crimes committed within a specified time range.
    
    Args:
        db: MongoDB database connection.
        start_date: Start date in YYYY-MM-DD format.
        end_date: End date in YYYY-MM-DD format.
    
    Returns:
        A list of dictionaries containing crime codes and their counts.
    """
    try:
        # Convert input strings to datetime objects (if they are not already)
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)
        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date)
            
        print(f"Querying from {start_date} to {end_date}")  # Debug log

        # MongoDB aggregation pipeline
        pipeline = [
            # Match documents within the specified time range
            {
                "$match": {
                    "date_occurred": {
                        "$gte": start_date.isoformat(),  # Ensure the format matches
                        "$lte": end_date.isoformat()    # Ensure the format matches
                    }
                }
            },
            # Unwind the 'crime' array to work with individual crime codes
            {
                "$unwind": "$crime"
            },
            # Group by crime code and count occurrences
            {
                "$group": {
                    "_id": "$crime.code",
                    "count": {"$sum": 1}
                }
            },
            # Sort by count in ascending order
            {
                "$sort": {"count": 1}
            },
            # Limit to the two least common crimes
            {
                "$limit": 2
            },
            # Optionally, format the output to include only 'code' and 'count'
            {
                "$project": {
                    "_id": 0,
                    "code": "$_id",
                    "count": 1
                }
            }
        ]

        # Execute the aggregation pipeline
        result = list(db.crime_reports.aggregate(pipeline))
        print(f"Query result: {result}")  # Debug log
        return result
    except Exception as e:
        print(f"Error: {e}")  # Debug log
        raise e

