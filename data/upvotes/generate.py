import json
import random
from datetime import datetime, timedelta
from pymongo import MongoClient

# connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["la_crime_db"]
crime_collection = db['crime_reports']
officers_collection = db['police_officers']

# get all crime reports
all_crimes = list(crime_collection.find({}, {'dr_no': 1}))
total_crimes = len(all_crimes)

# calculate the number of crimes to upvote (at least 1/3 of all crimes)
num_crimes_to_upvote = max(1, total_crimes // 3)

# randomly select crimes to upvote
selected_crimes = random.sample(all_crimes, num_crimes_to_upvote)

# get all police officers
all_officers = list(officers_collection.find({}, {'badge_no': 1, 'name': 1, 'email': 1, 'area': 1}))
total_officers = len(all_officers)

# track upvotes per officer
officer_upvotes_count = {officer['badge_no']: 0 for officer in all_officers}


# function to generate a random date between two dates
def get_random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

# define start and end dates for random upvote date
start_date = datetime(2020, 1, 1)
end_date = datetime.now()

# generate upvote data
upvote_data = []
for crime in selected_crimes:
    dr_no = crime['dr_no']
    
    # randomly select an officer
    officer = random.choice(all_officers)
    officer_badge_no = officer['badge_no']
    
    # check if the officer has less than 1000 upvotes
    if officer_upvotes_count[officer_badge_no] >= 1000:
        continue  # Skip if the officer has already 1000 upvotes
    
    # generate a random upvote date
    upvote_date = get_random_date(start_date, end_date).strftime('%Y-%m-%d')
    
    # add upvote to the list
    upvote_data.append({
        "dr_no": dr_no,
        "officer": {
            "badge_no": officer_badge_no,
            "name": officer['name'],
            "email": officer['email'],
            "area": officer['area']
            
        },
        "upvote_date": upvote_date
    })
    
    # Increment the officer's upvote count
    officer_upvotes_count[officer_badge_no] += 1
    
# save the upvote data to a JSON file
output_file = 'data/upvotes/upvotes_data.json'
with open(output_file, 'w') as f:
    json.dump(upvote_data, f, indent=4)

print(f"Upvote data generated and saved to {output_file}.")