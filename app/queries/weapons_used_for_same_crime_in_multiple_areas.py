from datetime import datetime

def get_weapons_used_for_same_crime_in_multiple_areas(db):
    """
    Find the types of weapons that have been used for the same crime code in more than one area,
    excluding entries with empty or missing weapon descriptions.
    
    Args:
        db: MongoDB database connection.
    
    Returns:
        A list of dictionaries containing crime codes, weapon types, and the areas where they were used.
    """
    try:
        # MongoDB aggregation pipeline
        pipeline = [
            # Unwind the 'crime' array to work with individual crime codes
            {
                "$unwind": "$crime"
            },
            # Filter out documents where weapon description is missing or empty
            {
                "$match": {
                    "weapon.description": {"$ne": "", "$exists": True}
                }
            },
            # Group by crime code and weapon type, and collect distinct areas
            {
                "$group": {
                    "_id": {
                        "crime_code": "$crime.code",
                        "weapon": "$weapon.description"
                    },
                    "areas": {"$addToSet": "$area.name"}
                }
            },
            # Filter for combinations used in more than one area
            {
                "$match": {
                    "$expr": {
                        "$gt": [{"$size": "$areas"}, 1]
                    }
                }
            },
            # Project the desired output format
            {
                "$project": {
                    "_id": 0,
                    "crime_code": "$_id.crime_code",
                    "weapon": "$_id.weapon",
                    "areas": 1
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

