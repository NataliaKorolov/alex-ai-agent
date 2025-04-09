import streamlit as st
from openai import OpenAI
import PyPDF2
import os

# Load the PDF (same as before)
def read_pdf(file_path):
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# Load your business content
pdf_text = read_pdf("Delightful_Lashes_Price_List.pdf")


# Step 1: Connect to OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# System prompt
system_message = {
    "role": "system",
    "content": f"""
You are Alex, a smart and friendly assistant working for Delightful Lashes.
Use this info to answer questions about pricing and services:

{pdf_text}

If the question is general, respond like a helpful business assistant.
"""
}

# Start Streamlit app
st.set_page_config(page_title="Chat with Alex", layout="centered")
st.title("💬 Chat with Alex — Delightful Lashes AI Assistant")

# Session-based message storage
if "messages" not in st.session_state:
    st.session_state.messages = [system_message]

# User input
user_input = st.chat_input("Ask Alex something...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get response from OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

# Display messages
for msg in st.session_state.messages[1:]:  # skip system message
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
