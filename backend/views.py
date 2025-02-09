import os
from flask import request, Blueprint, send_from_directory, render_template, request, jsonify
import os
from flask_login import login_required, current_user
from bson import ObjectId 
from datetime import datetime
import requests
from services.GroqImage import GroqImage
from services.MapAPI import MapAPI
from services.RoutePlanner import RoutePlanner
import json

views = Blueprint('views', __name__)

#root 
@views.route('/', methods=['GET', 'POST'])
def serve_react(path):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    react_build_dir = os.path.join(base_dir, "../frontend/build")
    if path != "" and os.path.exists(os.path.join(react_build_dir, path)):
        return send_from_directory(react_build_dir, path)
    else:
        return send_from_directory(react_build_dir, "index.html")


#call the groq camera
@views.route('/get_closest_camera', methods=['POST'])
def get_closest_camera_endpoint():
    try:
        groq = GroqImage()
        data = request.get_json()
        if 'route' not in data or 'cameras' not in data:
            print("Missing required parameters")
            return jsonify({'error': 'Missing required parameters'}), 400

        route = data['route']
        cameras = data['cameras']
        closest_camera = groq.get_closest_camera(route, cameras)

        if closest_camera is None:
            return jsonify({'error': 'No camera found with latitude and longitude'}), 404

        url = closest_camera['url']
        description = groq.get_image_description(url)

        return jsonify({'url': url, 'description': description})
    except Exception as e:  
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred'}), 500
    

# Get routes from the Google API, generate a graph, and find the best routes using A* search
@views.route('/get_routes', methods=['POST'])
def get_routes():
    try:
        map_api = MapAPI(url='https://routes.googleapis.com/directions/v2:computeRoutes')
        data = request.get_json()

        if 'origin' not in data or 'destination' not in data:
            return jsonify({'error': 'Invalid input data'}), 400

        api_key = os.getenv('GOOGLE_API_KEY')
        if api_key is None:
            return jsonify({'error': 'Google API key is not defined in the .env file'}), 500

        # Call the Google API to get public transit routes
        route_info = map_api.get_public_transit_route(data['origin'], data['destination'], api_key)
        if route_info is None:
            return jsonify({'error': 'Failed to retrieve route information'}), 500

        with open('database/crime_data.json', 'r') as file:
            crime_data = json.load(file)

        # find the best routes
        planner = RoutePlanner(crime_data)
        best_routes = planner.find_best_routes(route_info)

        # Save best routes to the database 
        best_route_results = []
        for route_index, path, f_score in best_routes:
            route_entry = {
                "route_index": route_index + 1,
                "f_score": f_score,
                "path": path
            }
            views.generated_search_collection.insert_one(route_entry)
            best_route_results.append(route_entry)

        return jsonify({"best_routes": best_route_results}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred'}), 500
    


    

    