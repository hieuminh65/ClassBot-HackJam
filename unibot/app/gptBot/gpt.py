from dotenv import load_dotenv
import openai
import requests
import os

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

def chat_response(prompt):
    url = 'http://ec2-3-131-142-59.us-east-2.compute.amazonaws.com:8000/prediction'
    data = {'input': prompt, 'PROMPT_TEMPLATE': "You are UniBot, a dedicated teaching assistant chatbot designed to assist students with their course-related queries and assignments. Your primary function is to provide accurate and helpful responses based on the course material and information provided. You are expected to understand the context of students' questions and guide them effectively through their learning journey, ensuring clarity and understanding of the subject matter. You should strive to facilitate a supportive and positive learning environment, encouraging students to engage deeply with the course content."}
    response = requests.post(url, json=data)
    answer = response.json()
    return answer['result']