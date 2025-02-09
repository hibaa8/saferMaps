from flask import Flask
import os
import math
from groq import Groq
from dotenv import load_dotenv

app = Flask(__name__)

# Load the environment variables
load_dotenv()

# Initialize the client
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

class GroqImage:
    # Function to calculate the distance between two points
    def get_distance(self, lat1, lon1, lat2, lon2):
        R = 6371  # radius of the earth in kilometers
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c * 1000  # convert to meters
        return distance

    # Function to find the closest camera
    def get_closest_camera(self, latitude, longitude, cameras):
        closest_camera = None
        min_distance = float('inf')
        for camera in cameras:
            if 'latitude' in camera and 'longitude' in camera:
                distance = self.get_distance(latitude, longitude, camera['latitude'], camera['longitude'])
                if distance < min_distance:
                    min_distance = distance
                    closest_camera = camera
        return closest_camera

    # Function to get image description from groq
    def get_image_description(self, image_url):
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
