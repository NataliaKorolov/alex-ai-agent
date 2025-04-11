# from openai import OpenAI

# # Replace YOUR key here
# client = OpenAI(
#     api_key="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"
# )

# # Define X’s system prompt
# system_message = {
#     "role": "system",
#     "content": """
# You are X, an intelligent and friendly AI assistant created to support small business owners. 
# You can help with:

# 1. Business Planning
# 2. Marketing Strategies
# 3. Social Media Management
# 4. Finance and Budgeting
# 5. Customer Service
# 6. Operations
# 7. Technology Tools
# 8. Human Resources

# Always respond with helpful, clear, friendly advice. Invite the user to ask more questions.
# """
# }

# # Store the conversation history
# messages = [system_message]

# print("💬 Chat with X — type 'exit' to stop.\n")

# # Chat loop
# while True:
#     user_input = input("You: ")
#     if user_input.lower() in ["exit", "quit"]:
#         print("X: Goodbye! 👋")
#         break

#     # Add user message
#     messages.append({"role": "user", "content": user_input})

#     # Send to GPT
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=messages
#     )

#     # Get assistant reply
#     reply = response.choices[0].message.content
#     print("X:", reply)

#     # Save assistant reply to history
#     messages.append({"role": "assistant", "content": reply})


from openai import OpenAI
import PyPDF2
import os

# Step 1: Connect to OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Step 2: Load PDF file content
def read_pdf(file_path):
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# Load your actual PDF here
pdf_text = read_pdf("Delightful_Lashes_Price_List.pdf")

# Step 3: Define Alex's personality and knowledge
system_message = {
    "role": "system",
    "content": f"""
You are Alex, an intelligent and friendly AI assistant working for Delightful Lashes.

You specialize in:
1. Helping customers understand lash services and pricing
2. Explaining appointment options and recommendations
3. Answering questions about Delightful Lashes' services

Use the following content to guide your responses:

{pdf_text}

If the user asks about general small business topics, respond as a helpful assistant for entrepreneurs.
"""
}

# Step 4: Start the conversation loop
messages = [system_message]

print("💬 Chat with Alex — type 'exit' to stop.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Alex: Goodbye! 👋")
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    reply = response.choices[0].message.content
    print("Alex:", reply)

    messages.append({"role": "assistant", "content": reply})
