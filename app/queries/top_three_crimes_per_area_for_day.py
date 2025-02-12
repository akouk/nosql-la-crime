from datetime import datetime, timedelta

def get_top_three_crimes_per_area_for_day(db, specific_date):
    """
    Find the three most common crimes committed per area for a specific day.
    
    Args:
        db: MongoDB database connection.
        specific_date: The specific date in YYYY-MM-DD format.
    
    Returns:
        A list of dictionaries containing areas and their top three crimes with counts.
    """
    try:
        # Convert input string to datetime object (if it is not already)
        if isinstance(specific_date, str):
            specific_date = datetime.fromisoformat(specific_date)
            
        # print(f"Querying for crimes on {specific_date}")  # Debug log

        # MongoDB aggregation pipeline
        pipeline = [
            # Match documents for the specific day
            {
                "$match": {
                    "date_occurred": {
                        "$gte": specific_date.isoformat(),  # Start of the day
                        "$lt": (specific_date + timedelta(days=1)).isoformat()  # Start of the next day
                    }
                }
            },
            # Unwind the 'crime' array to work with individual crime codes
            {
                "$unwind": "$crime"
            },
            # Group by area and crime code, and count occurrences
            {
                "$group": {
                    "_id": {
                        "area": "$area.name",
                        "crime_code": "$crime.code"
                    },
                    "count": {"$sum": 1}
                }
            },
            # Sort by area and count in descending order
            {
                "$sort": {
                    "_id.area": 1,
                    "count": -1
                }
            },
            # Group by area to collect top three crimes
            {
                "$group": {
                    "_id": "$_id.area",
                    "crimes": {
                        "$push": {
                            "crime_code": "$_id.crime_code",
                            "count": "$count"
                        }
                    }
                }
            },
            # Project to limit to top three crimes per area
            {
                "$project": {
                    "_id": 0,
                    "area": "$_id",
                    "top_crimes": {
                        "$slice": ["$crimes", 3]
                    }
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

