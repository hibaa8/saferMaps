<<<<<<< HEAD
from flask import Flask, request, jsonify
import requests
import json
from dotenv import load_dotenv
import os
from flask_cors import CORS

# Load environment variables from the .env file
load_dotenv()

# app = Flask(__name__)
# CORS(app)

class MapAPI:
    def __init__(self, url):
        self.url = 'https://routes.googleapis.com/directions/v2:computeRoutes'

    def get_public_transit_route(self, origin, destination, api_key):

        # Define the request headers
        headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': api_key,
            'X-Goog-FieldMask': '*'
        }

        # Define the request data
        data = {
            'origin': {
                'address': origin
            },
            'destination': {
                'address': destination
            },
            'travelMode': 'TRANSIT',
            'computeAlternativeRoutes': True,
            'transitPreferences': {
                'routingPreference': 'LESS_WALKING',
                'allowedTravelModes': ['TRAIN']
            }
        }

        # Send the request
        response = requests.post(self.url, headers=headers, json=data)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            return None

=======
from flask import Flask, request, jsonify
import requests
import json
from dotenv import load_dotenv
import os
from flask_cors import CORS

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

def get_public_transit_route(origin, destination, api_key):
    # Define the API endpoint
    url = 'https://routes.googleapis.com/directions/v2:computeRoutes'

    # Define the request headers
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': '*'
    }

    # Define the request data
    data = {
        'origin': {
            'address': origin
        },
        'destination': {
            'address': destination
        },
        'travelMode': 'TRANSIT',
        'computeAlternativeRoutes': True,
        'transitPreferences': {
            'routingPreference': 'LESS_WALKING',
            'allowedTravelModes': ['TRAIN']
        }
    }

    # Send the request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return None

@app.route('/get_routes', methods=['POST'])
def get_routes():
    data = request.get_json()

    # Check if the input data is valid
    if 'origin' not in data or 'destination' not in data:
        return jsonify({'error': 'Invalid input data'}), 400

    # Get the Google Maps API key from the .env file
    api_key = os.getenv('GOOGLE_API_KEY')

    # Check if the API key is defined
    if api_key is None:
        return jsonify({'error': 'Google API key is not defined in the .env file'}), 500

    # Get the public transit route
    route_info = get_public_transit_route(data['origin'], data['destination'], api_key)

    # Return the combined route information as JSON
    return jsonify(route_info), 200

if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> 2ad5deb81128e9ff560178f568291513492e6f62
