
from flask import Flask
from db.mongo import init_db
from app.routes import crime_routes

app = Flask(__name__)

# Initialize MongoDB connection
mongo = init_db(app=app)

# Pass the `mongo` object to the Blueprint
crime_routes.mongo = mongo

# Register routes
app.register_blueprint(crime_routes)

if __name__ == '__main__':
    app.run(debug=True)