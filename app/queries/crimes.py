from datetime import datetime, timedelta

# function to convert date strings to datetime
def convert_to_datetime(date):
    if isinstance(date, str):
        return datetime.fromisoformat(date)
    return date

# function to execute MongoDB aggregation pipeline
def execute_pipeline(db, pipeline):
    try:
        result = list(db.crime_reports.aggregate(pipeline))
        # print(f"Query result: {result}")
        return result
    except Exception as e:
        print(f"Error: {e}")
        raise e
    
# query 1
def get_reports_per_crime_code(db, start_date, end_date):

    # convert input strings to datetime objects
    start_date = convert_to_datetime(start_date)
    end_date = convert_to_datetime(end_date)
        
    # print(f"Querying from {start_date} to {end_date}")

    # MongoDB aggregation pipeline
    pipeline = [
        # match documents within the specified time range
        {
            "$match": {
                "date_occurred": {
                    "$gte": start_date.isoformat(), # ensure the format matches
                    "$lte": end_date.isoformat() # ensure the format matches
                }
            }
        },
        # unwind the 'crime' array to work with individual crime codes
        {
            "$unwind": "$crime"
        },
        # group by the 'code' field in the 'crime' array and count occurrences
        {
            "$group": {
                "_id": "$crime.code",
                "count": {"$sum": 1}
            }
        },
        # sort the results in descending order by count
        {
            "$sort": {"count": -1}
        },
        # format the output to include only 'code' and 'count'
        {
            "$project": {
                "_id": 0,
                "code": "$_id",
                "count": 1
            }
        }
    ]

    return execute_pipeline(db, pipeline)
    
# query 2
def get_reports_per_day_for_crime_code(db, crime_code, start_date, end_date):

    # convert input strings to datetime objects
    if isinstance(start_date, str):
        start_date = datetime.fromisoformat(start_date)
    if isinstance(end_date, str):
        end_date = datetime.fromisoformat(end_date)
        
    # print(f"Querying for crime code {crime_code} from {start_date} to {end_date}")

    # MongoDB aggregation pipeline
    pipeline = [
        # match documents within the specified time range and crime code
        {
            "$match": {
                "date_occurred": {
                    "$gte": start_date.isoformat(), # ensure the format matches
                    "$lte": end_date.isoformat() # ensure the format matches
                },
                "crime.code": crime_code
            }
        },
        # unwind the 'crime' array to work with individual crime codes
        {
            "$unwind": "$crime"
        },
        # match again to ensure we only count the specific crime code
        {
            "$match": {
                "crime.code": crime_code
            }
        },
        # group by the day part of the date_occurred field and count occurrences
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
        # sort the results by date
        {
            "$sort": {"_id": 1}
        },
        # format the output to include only 'date' and 'count'
        {
            "$project": {
                "_id": 0,
                "date": "$_id",
                "count": 1
            }
        }
    ]

    # execute the aggregation pipeline
    return execute_pipeline(db, pipeline)

# quey 3 
def get_top_three_crimes_per_area_for_day(db, specific_date):

    # convert input string to datetime object
    if isinstance(specific_date, str):
        specific_date = datetime.fromisoformat(specific_date)
        
    # print(f"Querying for crimes on {specific_date}")

    # MongoDB aggregation pipeline
    pipeline = [
        # match documents for the specific day
        {
            "$match": {
                "date_occurred": {
                    "$gte": specific_date.isoformat(),  # start of the day
                    "$lt": (specific_date + timedelta(days=1)).isoformat()  # start of the next day
                }
            }
        },
        # unwind the 'crime' array to work with individual crime codes
        {
            "$unwind": "$crime"
        },
        # group by area and crime code, and count occurrences
        {
            "$group": {
                "_id": {
                    "area": "$area.name",
                    "crime_code": "$crime.code"
                },
                "count": {"$sum": 1}
            }
        },
        # sort by area and count in descending order
        {
            "$sort": {
                "_id.area": 1,
                "count": -1
            }
        },
        # group by area to collect top three crimes
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
        # project to limit to top three crimes per area
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

    # execute the aggregation pipeline
    return execute_pipeline(db, pipeline)

# query 4
def get_two_least_common_crimes_per_day(db, start_date, end_date):

    # convert input strings to datetime objects
    if isinstance(start_date, str):
        start_date = datetime.fromisoformat(start_date)
    if isinstance(end_date, str):
        end_date = datetime.fromisoformat(end_date)
        
    # print(f"Querying from {start_date} to {end_date}")

    # MongoDB aggregation pipeline
    pipeline = [
        # match documents within the specified time range
        {
            "$match": {
                "date_occurred": {
                    "$gte": start_date.isoformat(),  # ensure the format matches
                    "$lte": end_date.isoformat()    # ensure the format matches
                }
            }
        },
        # unwind the 'crime' array to work with individual crime codes
        {
            "$unwind": "$crime"
        },
        # group by crime code and count occurrences
        {
            "$group": {
                "_id": "$crime.code",
                "count": {"$sum": 1}
            }
        },
        # sort by count in ascending order
        {
            "$sort": {"count": 1}
        },
        # limit to the two least common crimes
        {
            "$limit": 2
        },
        # format the output to include only 'code' and 'count'
        {
            "$project": {
                "_id": 0,
                "code": "$_id",
                "count": 1
            }
        }
    ]

    return execute_pipeline(db, pipeline)

# query 5
def get_weapons_used_for_same_crime_in_multiple_areas(db):

    # MongoDB aggregation pipeline
    pipeline = [
        # unwind the 'crime' array to work with individual crime codes
        {
            "$unwind": "$crime"
        },
        # filter out documents where weapon description is missing or empty
        {
            "$match": {
                "weapon.description": {"$ne": "", "$exists": True}
            }
        },
        # group by crime code and weapon type, and collect distinct areas
        {
            "$group": {
                "_id": {
                    "crime_code": "$crime.code",
                    "weapon": "$weapon.description"
                },
                "areas": {"$addToSet": "$area.name"}
            }
        },
        # filter for combinations used in more than one area
        {
            "$match": {
                "$expr": {
                    "$gt": [{"$size": "$areas"}, 1]
                }
            }
        },
        # project to format the output
        {
            "$project": {
                "_id": 0,
                "crime_code": "$_id.crime_code",
                "weapon": "$_id.weapon",
                "areas": 1
            }
        }
    ]

    # execute the aggregation pipeline
    return execute_pipeline(db, pipeline)

