from pymongo import MongoClient

# Replace these with your actual MongoDB connection details
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "your_database_name"
COLLECTION_NAME = "your_collection_name"

# Connect to MongoDB
# client = MongoClient(MONGO_URI)
# db = client[DATABASE_NAME]
# collection = db[COLLECTION_NAME]

client = MongoClient('mongodb://localhost:27017/')  
db = client['la_crime_db'] 
collection = db['crime_reports']

# Create index on date_reported field
collection.create_index([("date_occurred", 1)])
print("Index created on 'date_occurred' field.")

# Create index on crime.code field within the crime array
collection.create_index([("crime.code", 1)])
print("Index created on 'crime.code' field within the 'crime' array.")

# Create index on area.name field within the crime array
collection.create_index([("area.name", 1)])
print("Index created on 'area.name' field within the 'crime' array.")

# Close the connection
client.close()