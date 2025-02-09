from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

# Assuming SQLAlchemy is initialized
db = SQLAlchemy()

class GeneratedSearch(db.Model):
    __tablename__ = 'generated_searches'
    id = db.Column(db.Integer, primary_key=True)
    route_data = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


def insert_route_data(route_json_path):
    # Read the JSON file containing the route data
    with open(route_json_path, 'r') as file:
        route_data = json.load(file)

    # Create a new GeneratedSearch object
    new_generated_search = GeneratedSearch(
        route_data=route_data
    )

    # Add and commit the new entry to the database
    db.session.add(new_generated_search)
    db.session.commit()

    print("Route data inserted successfully.")

insert_route_data('test_feed_data.json')