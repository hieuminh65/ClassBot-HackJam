# Bull Bot

## Description
A Chatbot that can answer questions about University of South Florida

## Server

### Flask App - AWS EC2 

Server hosts the embedding model and make calls to OpenAI API to generate answers to questions.

### Express App - Cyclic

Express server get requests from the client and make calls to the Flask server to get answers to questions.

## Client - Vite App - Vercel

Client is a web app that allows users to ask questions and get answers from the server.