import streamlit as st
import google.generativeai as genai

# Set your API key directly (for testing purposes, it is better to use environment variables in production)
api_key = "AIzaSyDuHVQdHpGY3hEIlkjX6L-_WaHcAGpxNwg"
genai.configure(api_key=api_key)

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

# Set app to wide mode
st.set_page_config(layout='wide')

# Title of the app
st.title('Your AI Writing Assistant')

# Create a subheader
st.subheader('Feeling stuck writing your essays? Chat with your AI Writing Assistant to brainstorm!')


# Initialize chat history if not already done
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Display the chat history
st.write("### Conversation")
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.write(f"**You:** {message['content']}")
    else:
        st.write(f"**AI:** {message['content']}")

# Input box for new messages
user_input = st.text_input("Enter your message here")

# Send message button
if st.button("Send"):
    if user_input:
        # Add the user input to chat history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Build the history for the AI model
        chat_history_for_model = [{"role": msg["role"], "parts": [msg["content"]]} for msg in st.session_state.chat_history]
        
        # Generate a response from the model
        chat_session = model.start_chat(history=chat_history_for_model)
        chat_response = chat_session.send_message(user_input)
        
        # Add the AI's response to chat history
        st.session_state.chat_history.append({
            "role": "model",
            "content": chat_response.text
        })
        
        # Clear the input box and update the app
        st.experimental_rerun()
