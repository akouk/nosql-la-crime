from pymongo import MongoClient

# connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')  
db = client['la_crime_db'] 
crimes_collection = db['crime_reports']
upvotes_collection = db['upvotes']

# create indexes for crimes_collection
try:
    crimes_collection.create_index([("date_occurred", 1), ("crime.code", 1)])
    crimes_collection.create_index([("date_occurred", 1), ("area.name", 1), ("crime.code", 1)])
    crimes_collection.create_index([("crime.code", 1), ("weapon.description", 1), ("area.name", 1)])
    print("Indexes created successfully for crimes_collection.")
except Exception as e:
    print(f"Error creating indexes for crimes_collection: {e}")

# create indexes for upvotes_collection
try:
    upvotes_collection.create_index([("upvote_date", 1), ("report.dr_no", 1)])
    upvotes_collection.create_index([("officer.badge_no", 1), ("officer.name", 1)])
    upvotes_collection.create_index([("officer.badge_no", 1), ("report.area.no", 1)])
    upvotes_collection.create_index([("officer.email", 1), ("officer.badge_no", 1)])
    upvotes_collection.create_index([("officer.name", 1), ("report.area", 1)])
    print("Indexes created successfully for upvotes_collection.")
except Exception as e:
    print(f"Error creating indexes for upvotes_collection: {e}")