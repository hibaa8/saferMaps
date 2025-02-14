from flask import Blueprint, send_from_directory, request, jsonify
import os
from flask import request, Blueprint, send_from_directory, render_template, request, jsonify
import os
from flask_login import login_required, current_user
from datetime import datetime
import requests
from services.GroqImage import GroqImage
from services.MapAPI import MapAPI
from services.RoutePlanner import RoutePlanner
from services.RouteSummary import routeSummary
import json

views = Blueprint('views', __name__)

# Root route for serving React files
@views.route('/', defaults={'path': ''})  # Set default path to an empty string
@views.route('/<path:path>')  # Handle subpaths like /about or /dashboard
def serve_react(path):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    react_build_dir = os.path.join(base_dir, "../frontend/my-app/dist")  # Ensure this points to your React build folder
    print('react build directory: ')
    print(react_build_dir)
    print(f' react build directory: ' + react_build_dir)
    if path != "" and os.path.exists(os.path.join(react_build_dir, path)):
        return send_from_directory(react_build_dir, path)
    else:
        return send_from_directory(react_build_dir, "index.html")


# #call the groq camera
@views.route('/get_closest_camera', methods=['POST'])
def get_closest_camera_endpoint():
    try:
        # Get the absolute path of the current script and adjust path to 'services' folder
        base_dir = os.path.dirname(os.path.abspath(__file__))
        camera_data_path = os.path.join(base_dir, 'database', 'cameras_with_location.json')

        # Now, you can safely open the file
        with open(camera_data_path, 'r') as file:
            camera_data = json.load(file)

        # Get the JSON data from the request
        data = request.get_json()

        route_data = data['route_data']

        # Extract the destination coordinates from the route data
        destination = route_data['routes'][0]['legs'][0]['end_location']

        # Instantiate GroqImage
        groq_image = GroqImage()

        # Pass camera_data to the get_closest_camera method
        closest_camera_destination = groq_image.get_closest_camera(destination['lat'], destination['lng'], camera_data)

        if not closest_camera_destination:
            return jsonify({'error': 'No camera found with latitude and longitude'}), 404

        # Get image description from GroqImage for the destination
        description_destination = groq_image.get_image_description(closest_camera_destination['url'])

        # Prepare the response data
        response_data = {
            'destination': {
                'url': closest_camera_destination['url'],
                'description': description_destination
            }
        }

        return jsonify(response_data)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred'}), 500
    

# # Get routes from the Google API, generate a graph, and find the best routes using A* search
@views.route('/get_routes', methods=['POST'])
def get_routes():
    try:
        map_api = MapAPI(url='https://routes.googleapis.com/directions/v2:computeRoutes')
        data = request.get_json()

        if 'origin' not in data or 'destination' not in data:
            return jsonify({'error': 'Invalid input data'}), 400

        api_key = 'AIzaSyAaaTjarIA-3dvVkjjvQq1S8aTquDmJK1o'

        # Call the Google API to get public transit routes
        route_info = map_api.get_public_transit_route(data['origin'], data['destination'], api_key)
        if route_info is None:
            return jsonify({'error': 'Failed to retrieve route information'}), 500
        
        with open('log.txt', 'a') as file:
            file.write('ROUTING INFO\n')
            file.write(json.dumps(route_info, indent=2))  # Convert to string with indentation
            
        with open('database/crime_data.json', 'r') as crime_file:
            crime_data = json.load(crime_file)
                
        with open('database/population_density.json', 'r') as population_file:
            population_data = json.load(population_file)

        # find the best routes
        planner = RoutePlanner(crime_data, population_data)
        best_routes = planner.find_best_routes(route_info)

        # # Save best routes to the database 
        # best_route_results = []
        # for route_index, path, f_score in best_routes:
        #     route_entry = {
        #         "route_index": route_index + 1,
        #         "f_score": f_score,
        #         "path": path
        #     }
        #     inserted_id = views.generated_search_collection.insert_one(route_entry).inserted_id
        #     # views.generated_search_collection.insert_one(route_entry)
        #     route_entry["_id"] = str(inserted_id)  # Convert ObjectId to string
        #     best_route_results.append(route_entry)

        return jsonify({"routes": best_routes}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred'}), 500

@views.route('/summarize_routes', methods=['POST'])
def summarize():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Call Groq API to summarize the routes
        summaries = routeSummary.summarize_routes_with_groq(data)

        # Return the summaries
        return jsonify({"summaries": summaries})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    