import json
import openai 
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = api_key


def getResponse(prompt):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages = [
        #{"role": "system", "content": "You are a assistant which provides feedback on CVs. suggest changes to make. Give multiple examples where to incorporate quantifiable metrics and sentences which can be replaced using Google XYZ resume template: "},
        {"role": "user", "content": "Give multiple examples where to incorporate quantifiable metrics and sentences which can be replaced using Google XYZ resume template: "},
        {"role": "user", "content": f"{prompt}"}
    ],  
    max_tokens=350,
    temperature=0.2
    )
    return response['choices'][0]['message']['content']