import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

def get_public_transit_route(origin, destination, api_key):
    # Define the API endpoint
    url = 'https://routes.googleapis.com/directions/v2:computeRoutes'

    # Define the request headers
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': 'routes.legs.steps.transitDetails'
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
        print(f'Error: {response.status_code}')
        return None

def main():
    # Define the origin and destination
    origin = input("Enter the origin: ")
    destination = input("Enter the destination: ")

    # Get the Google Maps API key from the .env file
    api_key = os.getenv('GOOGLE_API_KEY')

    # Check if the API key is defined
    if api_key is None:
        print("Google API key is not defined in the .env file.")
        return

    # Get the public transit route
    route_info = get_public_transit_route(origin, destination, api_key)

    # Save the route information to a JSON file
    if route_info is not None:
        with open('route_info.json', 'w') as f:
            json.dump(route_info, f, indent=4)

if __name__ == "__main__":
    main()