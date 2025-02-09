from flask import Flask
import json
import os
from groq import Groq
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)

# Load environment variables (for Groq API key)
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

class routeSummary:
    def summarize_routes_with_groq(data):
        # Define the prompt
        prompt = (
            "Take the JSON file, summarize each of the routes as a short "
            "10-word blurb, such as 'via 1 train to Canal Street' for a route that leads the user into the 1 train to south ferry, but they exit at canal street. "
        )

        # Prepare the messages to send to Groq
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
            {"role": "user", "content": json.dumps(data)}  # Send the JSON data to Groq
        ]

        # Send the request to Groq API
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.5,
            max_completion_tokens=1024,
            top_p=1
        )

        return chat_completion.choices[0].message.content

    if __name__ == '__main__':
        app.run(debug=True)
