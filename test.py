from openai import OpenAI, Client
from dotenv import load_dotenv # Add
import os

load_dotenv()  # Load environment variables from .env file

client = OpenAI()  # Initialize the OpenAI client with the API key

rules = "I am running some test of the ChatGPT API, so please act naturally"

message = "What are some effective ways to cut grass?"


completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        # TODO: Link to an SQL database, to pull relevant content and store learnings on how to best apply AI wrapper
        messages = [
            {"role": "system", 
            "content": rules},
            {"role": "user",
            "content": message }
        ]
    )

print(completion.choices[0].message.content)