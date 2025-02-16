import json
from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["la_crime_db"]

# retrieve all officers from the police_officers collection
officers_collection = db['police_officers']
all_officers = list(officers_collection.find({}))

# retrieve all crime reports from the crime_reports collection
crime_reports_collection = db['crime_reports']
all_reports = list(crime_reports_collection.find({}))

# function to generate a random date between 01/01/2020 and now
def generate_random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    random_number_of_days = random.randrange(time_between_dates.days)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date.strftime("%Y-%m-%d")

# generate fake upvotes
upvotes = []
start_date = datetime(2020, 1, 1)
end_date = datetime.now()

# track upvoted combinations of officer badge_no and report dr_no
upvoted_combinations = set()

# track the number of upvotes per officer
officer_upvote_counts = {officer["badge_no"]: 0 for officer in all_officers}

# number of upvotes to generate 
num_upvotes = max(1, len(all_reports) // 3)

# pre-generate a pool of random dates for each report
report_dates = {}
for report in all_reports:
    # generate a small pool of random dates for this report
    num_dates = random.randint(1, 5)  
    dates = [generate_random_date(start_date, end_date) for _ in range(num_dates)]
    report_dates[report["dr_no"]] = dates

# loop to generate upvotes
for _ in range(num_upvotes):
    # randomly pick an officer and a report
    officer = random.choice(all_officers)
    report = random.choice(all_reports)
    
    # check if the officer has already made 1000 upvotes
    if officer_upvote_counts[officer["badge_no"]] >= 1000:
        continue  # Skip this officer
    
    # create a unique key for the combination of officer and report
    combination_key = (officer["badge_no"], report["dr_no"])
    
    # check if this combination has already been upvoted
    if combination_key in upvoted_combinations:
        continue  # Skip this combination
    
    # get the pre-generated dates for this report
    dates_for_report = report_dates[report["dr_no"]]
    
    # randomly pick one of the pre-generated dates for this upvote
    upvote_date = random.choice(dates_for_report)
    
    # create the upvote document
    upvote = {
        "officer": {
            "badge_no": officer["badge_no"],
            "name": officer["name"],
            "email": officer["email"]
        },
        "report": {
            "dr_no": report["dr_no"],
            "area": report["area"]
        },
        "upvote_date": upvote_date
    }
    
    # add the upvote to the list
    upvotes.append(upvote)
    
    # add the combination to the set to prevent duplicate upvotes
    upvoted_combinations.add(combination_key)
    
    # increment the upvote count for the officer
    officer_upvote_counts[officer["badge_no"]] += 1


# save the upvote data to a JSON file, locally, in the same directory
output_file = 'data/upvotes/upvotes_data.json'
with open(output_file, 'w') as f:
    json.dump(upvotes, f, indent=4)

print(f"Upvote data generated and saved to {output_file}.")

