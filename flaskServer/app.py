from flask import Flask, request, jsonify
from config import Config
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chat_models.openai import ChatOpenAI
import pinecone


app = Flask(__name__)
app.config.from_object(Config)

import os
os.environ["OPENAI_API_KEY"] = app.config['OPENAI_API_KEY']
@app.route('/')
@app.route('/prediction', methods=['POST', 'GET'])
def prediction():
    data = request.get_json()
    if 'input' not in data:
        return jsonify({'error': 'The key in the data should be input.'}), 400
    prompt = data['input']
    global PROMPT_TEMPLATE
    PROMPT_TEMPLATE = data['PROMPT_TEMPLATE'] if data['PROMPT_TEMPLATE'] else app.config['PROMPT_TEMPLATE']
    
    try:
        embeddingModel = embeddings()
        docsearch = pineconeInitialization(embeddingModel)
        llm_model = llm_LOAD('gpt-3.5-turbo-16k', 500, 0.5)
        result = retrieve(prompt, docsearch, llm_model, PROMPT_TEMPLATE)
        answer = result['result']
        # answer += "\n\nSources of information: \n\n"
        # for doc in result['source_documents']:
        #     if 'title' in doc.metadata:
        #         answer += f"Title: {doc.metadata['title']}"
        #     if 'description' in doc.metadata:
        #         answer += f"Description of the document: {doc.metadata['description']}"
        return jsonify({'result': answer}), 200
    except Exception as e:
        return jsonify({'error': f'{e}'}), 400

EMBEDDINGS_MODEL = None
PINE_CONE = None
def embeddings():
    """openai embeddings models. Dimensions: 1536"""
    global EMBEDDINGS_MODEL
    EMBEDDINGS_MODEL = OpenAIEmbeddings()
    print("Embeddings Loaded")
    
    return EMBEDDINGS_MODEL

def pineconeInitialization(embeddings):
    global PINE_CONE

    if PINE_CONE is None:
        print("Initializing PineCone...")
        api_key = app.config['PINECONE_API']
        env = app.config['PINECONE_ENV']
        pinecone.init(api_key=api_key, environment=env)
        print("PineCone initialized")
        index = app.config['PINECONE_INDEX']
        docsearch = Pinecone.from_existing_index(index, embeddings)
    print("Vector Store Loaded")
    return docsearch

def llm_LOAD(model_name = 'gpt-3.5-turbo', max_tokens = 500, temperature=0.5):
    print("Loading Language Model...")
    llm = ChatOpenAI(
    temperature=temperature,
    model_name = model_name,
    max_tokens = max_tokens,
    )
    print("Language Model Loaded")
    return llm

def retrieve(query, docsearch, llm, prompt_template):
    print("Retrieving...")
    prompt_template = prompt_template + " \n\n "
    prompt_template += " {context} " + " \n\n "
    prompt_template += " Question: {question} "

    PROMPT = PromptTemplate(template=prompt_template, input_variables=['question', 'context'])

    query = query
    qa_with_sources = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever(), return_source_documents=True ,chain_type_kwargs={"prompt": PROMPT})

    result = qa_with_sources({"query": query})
    return result

def main():
    print('working')

if __name__ == "__main__":
    print("Hello I'm Working")
    app.run(host="0.0.0.0", port=8000, debug=True)
    main()