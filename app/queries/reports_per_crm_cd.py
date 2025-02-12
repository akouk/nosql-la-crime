from datetime import datetime

def get_reports_per_crime_code(db, start_date, end_date):
    """
    Count the number of reports per crime code within a specified date range.
    
    Args:
        db: MongoDB database connection.
        start_date: Start date in YYYY-MM-DD format.
        end_date: End date in YYYY-MM-DD format.
    
    Returns:
        A list of dictionaries containing crime codes and their report counts.
    """
    try:
        # Convert input strings to datetime objects (if they are not already)
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)
        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date)
            
        # print(f"Querying from {start_date} to {end_date}")  # Debug log

        # MongoDB aggregation pipeline
        pipeline = [
            # Match documents within the specified time range
            {
                "$match": {
                    "date_occurred": {
                        "$gte": start_date.isoformat(),
                        "$lte": end_date.isoformat()
                    }
                }
            },
            # Unwind the 'crime' array to work with individual crime codes
            {
                "$unwind": "$crime"
            },
            # Group by the 'code' field in the 'crime' array and count occurrences
            {
                "$group": {
                    "_id": "$crime.code",
                    "count": {"$sum": 1}
                }
            },
            # Sort the results in descending order by count
            {
                "$sort": {"count": -1}
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
        # print(f"Query result: {result}")  # Debug log
        return result
    except Exception as e:
        print(f"Error: {e}")
        raise e