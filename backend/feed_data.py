from pymongo import MongoClient
import json
from datetime import datetime
import os

client = MongoClient('mongodb+srv://test:w5GDUdfw6rrCrSbP@cluster0.eokpf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['map_routes']  # Replace with your database name
generated_search_collection = db['GeneratedSearch']  # Replace with your collection name

def insert_route_data(route_json_path):
    with open(route_json_path, 'r') as file:
        route_data = json.load(file)

    new_route_document = {
        "route_data": route_data,
        "created_at": datetime.utcnow()
    }

    result = generated_search_collection.insert_one(new_route_document)
    print(f"Route data inserted with ID: {result.inserted_id}")

insert_route_data('test_feed_data.json')
