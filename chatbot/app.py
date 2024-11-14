from flask import Flask, render_template, request, jsonify
import openai
import os
import sys
import pandas as pd

from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_openai import OpenAIEmbeddings
from langchain_openai.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper

app = Flask(__name__, template_folder="templates", static_folder="static")

os.environ["OPENAI_API_KEY"] = "*********************************************"

query = None

if len(sys.argv) > 1:
    query = sys.argv[1]

loader = DirectoryLoader("data/")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(texts, embeddings)

qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever())

chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    retriever=docsearch.as_retriever(search_kwargs={"k": 1}),
)

chat_history = []

@app.route('/')
def index():
    return render_template('MARVIS.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    global query, chat_history

    user_input = request.form['user_input']

    if not user_input:
        return jsonify({'response': 'Please provide a valid input.'})

    result = chain({"question": user_input, "chat_history": chat_history})
    response = result['answer']

    chat_history.append((user_input, response))
    query = None

    # Replace newline characters with <br> tags
    response_with_br = response.replace('\n', '<br>')

    return jsonify({'response': response_with_br})

if __name__ == '__main__':
    app.run(debug=True)