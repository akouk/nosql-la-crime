from datetime import datetime

def get_reports_per_day_for_crime_code(db, crime_code, start_date, end_date):
    """
    Count the number of reports per day for a specific crime code within a specified date range.
    
    Args:
        db: MongoDB database connection.
        crime_code: The crime code to filter by.
        start_date: Start date in YYYY-MM-DD format.
        end_date: End date in YYYY-MM-DD format.
    
    Returns:
        A list of dictionaries containing dates and their report counts.
    """
    try:
        # Convert input strings to datetime objects (if they are not already)
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)
        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date)
            
        # print(f"Querying for crime code {crime_code} from {start_date} to {end_date}")  # Debug log

        # MongoDB aggregation pipeline
        pipeline = [
            # Match documents within the specified time range and crime code
            {
                "$match": {
                    "date_occurred": {
                        "$gte": start_date.isoformat(),  # Ensure the format matches
                        "$lte": end_date.isoformat()    # Ensure the format matches
                    },
                    "crime.code": crime_code
                }
            },
            # Unwind the 'crime' array to work with individual crime codes
            {
                "$unwind": "$crime"
            },
            # Match again to ensure we only count the specific crime code
            {
                "$match": {
                    "crime.code": crime_code
                }
            },
            # Group by the day part of the date_occurred field and count occurrences
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": {
                                "$dateFromString": {
                                    "dateString": "$date_occurred"
                                }
                            }
                        }
                    },
                    "count": {"$sum": 1}
                }
            },
            # Sort the results by date
            {
                "$sort": {"_id": 1}
            },
            # Optionally, format the output to include only 'date' and 'count'
            {
                "$project": {
                    "_id": 0,
                    "date": "$_id",
                    "count": 1
                }
            }
        ]

        # Execute the aggregation pipeline
        result = list(db.crime_reports.aggregate(pipeline))
        # print(f"Query result: {result}")  # Debug log
        return result
    except Exception as e:
        print(f"Error: {e}")  # Debug log
        raise e
