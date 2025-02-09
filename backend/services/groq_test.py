from flask import Flask, request, jsonify
import json
import os
import math
from groq import Groq
from dotenv import load_dotenv

app = Flask(__name__)

# Load the environment variables
load_dotenv()

# Initialize the client
client = Groq(api_key=os.getenv('GROQ_API_KEY'))


# Function to calculate the distance between two points
def get_distance(lat1, lon1, lat2, lon2):
    R = 6371  # radius of the earth in kilometers
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c * 1000  # convert to meters
    return distance

# Function to find the closest camera
def get_closest_camera(latitude, longitude, cameras):
    closest_camera = None
    min_distance = float('inf')
    for camera in cameras:
        if 'latitude' in camera and 'longitude' in camera:
            distance = get_distance(latitude, longitude, camera['latitude'], camera['longitude'])
            if distance < min_distance:
                min_distance = distance
                closest_camera = camera
    return closest_camera

# Function to get image description from groq
def get_image_description(image_url):
    response = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": "From the user, we are walking around here to get to the subway. Don't suggest, just write in certain terms: What are the weather conditions? Visibility? Anything else noteworthy?"},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]}
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False
    )

    # Extract the text content properly
    if response.choices and response.choices[0].message and isinstance(response.choices[0].message.content, str):
        return response.choices[0].message.content
    else:
        return "No valid response received."

# Define the Flask endpoint to process the data
@app.route('/process_data', methods=['POST'])
def process_data():
    try:
        # Get the absolute path of the current script and adjust path to 'services' folder
        base_dir = os.path.dirname(os.path.abspath(__file__))
        camera_data_path = os.path.join(base_dir, '..', 'services', 'cameras_with_location.json')

        # Load the camera data from the file
        with open(camera_data_path, 'r') as file:
            camera_data = json.load(file)

        # Get the JSON data from the request
        data = request.get_json()

        # Validate input data
        if 'route_data' not in data:
            return jsonify({'error': 'Missing required parameters'}), 400

        route_data = data['route_data']

        # Extract the destination coordinates from the route data
        destination = route_data['routes'][0]['legs'][0]['end_location']

        # Find the closest camera to the destination
        closest_camera_destination = get_closest_camera(destination['lat'], destination['lng'], camera_data)

        if not closest_camera_destination:
            return jsonify({'error': 'No camera found with latitude and longitude'}), 404

        # Get image description from groq for the destination
        description_destination = get_image_description(closest_camera_destination['url'])

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
