import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(
    api_key = os.getenv('GROQ_API_KEY'),
)

completion = client.chat.completions.create(
    model="llama-3.2-11b-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "From the user, we are walking around here to get to the subway. Don't sugggest, just write in certain terms: What are the weather conditions? Visibility? Are roads slippery? When done, please write to be careful."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://webcams.nyctmc.org/api/cameras/c733e881-862d-4874-9d00-9bfdc3b27cbc/image?t=1739083573133"
                    }
                }
            ]
        }
    ],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=False,
    stop=None,
)

print(completion.choices[0].message)
