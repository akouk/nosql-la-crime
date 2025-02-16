import json
import os
from pymongo import MongoClient


file_path = os.path.join(os.path.dirname(__file__), 'officers_data.json')

# load officers data from JSON file
try:
    with open(file_path, 'r') as f:
        officers_data = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{file_path}' contains invalid JSON.")
    exit(1)
    
    
# connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["la_crime_db"]
collection = db['police_officers']

try:
    # insert the data into the MongoDB collection
    collection.insert_many(officers_data)
except Exception as e:
        print(f"Failed to insert officers data: {e}")

print("Police officers inserted successfully into MongoDB!")
