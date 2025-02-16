import json
import os
from pymongo import MongoClient
from .process import process_crime_data

file_path = os.path.join(os.path.dirname(__file__), 'crime_data.json')

# load crime data from JSON file
try:
    with open(file_path, 'r') as f:
        crime_data = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{file_path}' contains invalid JSON.")
    exit(1)

# connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')  
db = client['la_crime_db'] 
collection = db['crime_reports']

# process and insert each crime record
for crime in crime_data:
    # process the crime data
    processed_crime, error, status_code = process_crime_data(crime)
    
    if error:
        # print the DR_NO of the record that failed validation
        dr_no = crime.get("dr_no", "Unknown DR_NO")
        print(f"Skipping record with DR_NO: {dr_no} due to validation error: {error}")
        continue  # skip this record if there's an error
    
    # insert the processed crime data into the database
    try:
        collection.insert_one(processed_crime)
        print(f"Inserted crime report with DR_NO: {processed_crime['dr_no']}")
    except Exception as e:
        print(f"Failed to insert crime report: {e}")

print("Data insertion completed.")