from dotenv import load_dotenv

load_dotenv() #loading all environment variables

import streamlit as st
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv('GOOGLE_API_KEY')) #setting the api key

#loading the model

model = genai.GenerativeModel("gemini-1.5-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream = True)
    return response

st.set_page_config(page_title="Q&A")

st.header("QA Chatbot Using Gemini")

#initialize session state if there is no history

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []   

input = st.text_input("Input: ", key="input")

submit = st.button("Ask the question")

if submit and input:
    response = get_gemini_response(input)
    st.session_state['chat_history'].append(("You", input))  # Fixed tuple syntax
    st.subheader("The response is:")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))  # Fixed tuple syntax

st.subheader("The chat history is:")

for role,text in st.session_state['chat_history']:
    st.write(f'{role}:{text}')