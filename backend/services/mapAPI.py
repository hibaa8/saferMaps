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

