from datetime import datetime

# function to execute MongoDB aggregation pipeline
def execute_pipeline(db, pipeline):
    try:
        result = list(db.upvotes.aggregate(pipeline))
        print(f"Query result: {result}")
        return result
    except Exception as e:
        print(f"Error: {e}")
        raise e
    
# query 6
def get_top_fifty_upvoted_reports_for_day(db, specific_date):
    print("specific_date: ", specific_date)
    
    # ensure the specific_date is in the correct format
    if isinstance(specific_date, str):
        # validate the date format 
        datetime.strptime(specific_date, '%Y-%m-%d')
    else:
        raise ValueError("specific_date must be a string in 'YYYY-MM-DD' format.")
        
    print(f"Querying for top fifty upvoted reports on {specific_date}")

    # MongoDB aggregation pipeline
    pipeline = [
        # match the upvote date
        {
            "$match": {
                "upvote_date": specific_date
            }
        },
        # group by the 'dr_no' and count the number of upvotes for each dr_no
        {
            
            "$group": {
                "_id": "$report.dr_no",
                "upvote_count": {"$sum": 1}
            }
        },
        # sort the results in descending order by upvote count
        {
            "$sort": {
                "upvote_count": -1
            }
        },
        # limit the results to the top 50
        {
            "$limit": 50
        },
        # format the output
        {
            "$project": {
                "_id": 0 ,
                "dr_no": "$_id",
                "upvote_count": 1,
            }
        }
    ]

    return execute_pipeline(db, pipeline)

# query 7
def get_top_fifty_active_officers(db):
    
    # MongoDB aggregation pipeline
    pipeline = [
        # group by officer badge number and count the total number of upvotes
        {
            "$group": {
                "_id": "$officer.badge_no",
                "name": { "$first": "$officer.name" },  # include the officer's name
                "total_upvotes": { "$sum": 1 }
            }
        },
        # sort the officers by the total upvotes in descending order
        {
            "$sort": { "total_upvotes": -1 }
        },
        # limit the result to the top 50 most active officers
        {
            "$limit": 50
        },
        # project to format the data
        {
            "$project": {
                "_id": 0,
                "badge_no": "$_id",
                "name": 1,
                "total_upvotes": 1 
            }
        }
    ]

    return execute_pipeline(db, pipeline)

# query 8
def get_top_50_officers_by_unique_areas(db):

    # MongoDB aggregation pipeline
    pipeline = [
        # group by officer's badge_no (include the officer's name) and collect unique area numbers from report.area.no
        {
            "$group": {
                "_id": "$officer.badge_no", 
                "name": { "$first": "$officer.name" },
                "unique_areas": { "$addToSet": "$report.area.no" }
            }
        },
        # add a field to calculate the total number of unique areas
        {
            "$addFields": {
                "total_unique_areas": { "$size": "$unique_areas" }
            }
        },
        # sort by total_unique_areas in descending order
        { 
            "$sort": { 
                "total_unique_areas": -1 
            } 
        },
        # limit to top 50 officers
        { 
            "$limit": 50 
        },
        # project to format output
        {
            "$project": {
               "_id": 0,
               "badge_no": "$_id",
               "name": 1,
                "total_unique_areas": 1  
            }
        }
    ]

    return execute_pipeline(db, pipeline)
    
# query 9
def get_reports_with_duplicate_email(db):
    # MongoDB aggregation pipeline
    pipeline = [
        # group by officer_email and collect unique badge numbers
        {
            "$group": {
                "_id": "$officer.email",  # group by email only
                "unique_badge_numbers": { "$addToSet": "$officer.badge_no" },
                "report_dr_nos": { "$addToSet": "$report.dr_no" }  # collect associated report dr_no 
            }
        },
        # add a field to calculate the number of unique badge numbers
        {
            "$addFields": {
                "badge_count": { "$size": "$unique_badge_numbers" }
            }
        },
        # match only documents where the same email is used for more than one badge number
        {
            "$match": {
                "badge_count": { "$gt": 1 }
            }
        },
        # project to format the output
        {
            "$project": {
                "_id": 0,
                "officer_email": "$_id",
                "unique_badge_numbers": 1,
                "report_dr_nos": 1
            }
        }
    ]

    return execute_pipeline(db, pipeline)
    
    
    
# query 10      
def get_areas_for_given_name(db, name):

    # MongoDB aggregation pipeline
    pipeline = [
        # filter for upvotes casted by the given name
        {
            "$match": {
                "officer.name": name
            }
        },
        # group the results by the report area
        {
            "$group": {
                "_id": "$report.area"
            }
        },
        # project to format the output
        {
            "$project": {
                "_id": 0,
                "area": "$_id"
            }
        }
    ]

    return execute_pipeline(db, pipeline)