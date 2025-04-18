import streamlit as st
from openai import OpenAI
import PyPDF2
import os
from PIL import Image
import re
from pdf_service_extractor import read_pdf
from pdf_service_extractor import extract_services_from_pdf_text


# Load your business content
pdf_text = read_pdf("Delightful_Lashes_Price_List.pdf")

# service_options = extract_services_from_pdf_text(pdf_text)

service_options = [
    "Lash Lift",
    "Classic Full Set",
    "Volume Fill",
    "Hybrid Fill",
    "Mega Volume",
    "Lash Removal",
    "Tinting",
    "Other"
]


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

logo = Image.open("DelightfulLashesLogo.png")
st.image(logo, width=300)  # You can change width to fit your layout

st.markdown("""
    <style>
    body {
        background-color: #fffafc;
    }
    .stApp {
        background: linear-gradient(to bottom right, #fff0f5, #e6e6fa);
        font-family: 'Segoe UI', sans-serif;
    }
    .stChatMessage {
        background-color: #ffffff44;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
    }
    .stChatMessage.user {
        background-color: #dce9f9;
        color: #000;
    }
    .stChatMessage.assistant {
        background-color: #fef9ec;
        color: #222;
    }
    </style>
""", unsafe_allow_html=True)


st.title("💬 Chat with Alex — Delightful Lashes AI Assistant")

# Session-based message storage
if "messages" not in st.session_state:
    st.session_state.messages = [system_message]

# User input
user_input = st.chat_input("Ask Alex something...")



if user_input and "book" in user_input.lower():
    with st.form("booking_form", clear_on_submit=True):
        name = st.text_input("Your name")
        date = st.date_input("Preferred date")
        time = st.time_input("Preferred time")
        service = st.selectbox("Choose a service", service_options)
        submitted = st.form_submit_button("Submit Booking Request")

        if submitted:
            booking_info = f"📅 Booking Request:\n- Name: {name}\n- Date: {date}\n- Time: {time}\n- Service: {service}"
            st.success("Thank you! We've received your request 💖")
            st.session_state.messages.append({"role": "assistant", "content": booking_info})


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
