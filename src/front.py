import streamlit as st
import sys
import os

# Añadir el directorio padre al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chatbot import predict_class, get_response, intents


st.title("AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "first message" not in st.session_state:
    st.session_state.first_message = True

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.first_message:
    with st.chat_message("assistant"):
        st.markdown("Hola soy un bot. ¿En qué puedo ayudarte?")
    
    st.session_state.messages.append({"role": "assistant", "content": "Procesando..."})
    st.session_state.first_message = False

if prompt := st.chat_input("Escribe un mensaje..."):
    with st.chat_message("user"):
        st.markdown(prompt)
        
    st.session_state.messages.append({"role": "user", "content": prompt})

    inst = predict_class(prompt)
    res = get_response(inst, intents)

    with st.chat_message("assistant"):
        st.markdown(res)
    
    st.session_state.messages.append({"role": "assistant", "content": res})