import os
import json
from pymongo import MongoClient


file_path = os.path.join(os.path.dirname(__file__), 'upvotes_data.json')

# load upvote data from JSON file
try:
    with open(file_path, 'r') as f:
        upvote_data = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{file_path}' contains invalid JSON.")
    exit(1)
    
# connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['la_crime_db']
upvotes_collection = db['upvotes']

# insert upvote data into the database
try:
    upvotes_collection.insert_many(upvote_data)
    print(f"Inserted {len(upvote_data)} upvotes into the database.")
except Exception as e:
    print(f"Failed to insert upvotes: {e}")