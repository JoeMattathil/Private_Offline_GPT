import streamlit as st
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import GPT4All, LlamaCpp
import chromadb
import os
import time
import base64
from PIL import Image
import tempfile
import fun_def.chat_ui as su




def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local('ui_elements/background.jpg')

st.sidebar.image("ui_elements/chatbot.png", width=200)
st.sidebar.markdown("---")
st.sidebar.markdown(
            "This  is a proof of concept on offline generative model. "
            "The dataset of the equipment compared to the kndowledge base on which the model is built is minimal. "
            "The model can thus throw generelized outputs. "
            "The result will depend on the clarity of the questions asked . "
            "Add your files into the source_documents folder and run ingest.py . "
            "It will create a vector store of the documents as db . "
            "The model will then be able to answer the questions based on the documents in the db . "
            "Run app.py to start the chatbot . "
)

# Load environment variables from .env file
if not load_dotenv():
    st.error("Could not load .env file or it is empty. Please check if it exists and is readable.")
    st.stop()

embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME")
persist_directory = os.environ.get('PERSIST_DIRECTORY')

model_type = os.environ.get('MODEL_TYPE')
model_path = os.environ.get('MODEL_PATH')
model_n_ctx = os.environ.get('MODEL_N_CTX')
model_n_batch = int(os.environ.get('MODEL_N_BATCH', 8))
target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS', 4))

from constants import CHROMA_SETTINGS

# Initialize Chroma database and retriever
embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
chroma_client = chromadb.PersistentClient(settings=CHROMA_SETTINGS, path=persist_directory)
db = Chroma(persist_directory=persist_directory, embedding_function=embeddings, client_settings=CHROMA_SETTINGS,
            client=chroma_client)
retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})

# Initialize LLM based on the selected model type
if model_type == "LlamaCpp":
    llm = LlamaCpp(model_path=model_path, max_tokens=model_n_ctx, n_batch=model_n_batch, verbose=False)
elif model_type == "GPT4All":
    llm = GPT4All(model=model_path, max_tokens=model_n_ctx, backend='gptj', n_batch=model_n_batch, verbose=False)
else:
    st.error(f"Model type {model_type} is not supported. Please choose one of the following: LlamaCpp, GPT4All")
    st.stop()

qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)

# Streamlit UI


st.title("Generative AI based Offline Chatbot")
st.subheader("Developed by Joe Sibi Mattathil")
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

        
for message in st.session_state.messages:
    su.message_func(
        message["content"],
        True if message["role"] == "user" else False,
        True if message["role"] == "assistant" else False,
    )

        
# Accept user input
if query := st.chat_input("Enter your Query here"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    su.message_func(query, is_user=True)
    # Display user message in chat message container
    res = qa(query)
    answer, docs = res['result'], res['source_documents']
    # Display assistant response in chat message container

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": answer})
    su.message_func(answer, is_user=False)