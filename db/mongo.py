from flask_pymongo import PyMongo
from flask import Flask
from pymongo import MongoClient

# create the MongoDB client and set the connection URI\
def init_db( app: Flask ):
    app.config["MONGO_URI"] = "mongodb://localhost:27017/la_crime_db"
    mongo = PyMongo(app)
    return mongo
