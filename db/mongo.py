from flask_pymongo import PyMongo
from flask import Flask
from pymongo import MongoClient

# Create the MongoDB client and set the connection URI\
def init_db( app: Flask ):
    app.config["MONGO_URI"] = "mongodb://localhost:27017/la_crime_db"
    mongo = PyMongo(app)
    return mongo
    # client = MongoClient("mongodb://localhost:27017/")
    # db = client["NoSQL-LA-CRIME"]   
    # return db