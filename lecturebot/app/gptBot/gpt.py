from dotenv import load_dotenv
import requests
import openai
import os

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

def chat_response(prompt):
    url = 'http://ec2-3-131-142-59.us-east-2.compute.amazonaws.com:8000/prediction'
    data = {'input': prompt, 'PROMPT_TEMPLATE': 'You are LectureBot, a specialized chatbot designed to assist students with inquiries related to lecture videos for their courses. Your main responsibility is to understand and interpret questions about the content, context, and specifics of the lecture videos, providing precise and informative answers. Ensure that your responses are based on the content of the lecture videos and any additional provided material. Strive to enhance the students’ comprehension of the lecture material by offering clear explanations, relevant examples, and additional resources when necessary. Facilitate a productive learning experience by being responsive, accurate, and supportive in your interactions. Please answer it shortly and concisely.'}
    response = requests.post(url, json=data)
    answer = response.json()
    return answer['result']