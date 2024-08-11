import streamlit as st
import os
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
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
)

# Set app to wide mode
st.set_page_config(layout='wide')

# Title of our app
st.title('Your AI Writing Assistant')

# Create a subheader
st.subheader('Feeling stuck writing your essays? Chat with your AI Writing Assistant to brainstorm!')

# Sidebar for user input
with st.sidebar:
    st.title('Input your writing details')
    st.subheader('Enter details of the writing task you have')

    # Blog title
    blog_title = st.text_input("Blog Title")

    # Keyword input
    keywords = st.text_area("Keywords (Comma-Separated)")

    # Number of words
    num_words = st.slider("Number of Words", min_value=100, max_value=1000, step=100)

    # Number of images
    num_images = st.number_input("Number of Images", min_value=1, max_value=10, step=1)

    # Generate blog button
    submit_button = st.button("Generate Blog")

    if submit_button:
        prompt = f"Give me a few lines on {blog_title} and use keywords, {num_words} to help write the blog, with {num_words} as the word count"
        
        # Use the model to generate content
        response = model.generate_content({
            "parts": [prompt]
        })

        # Get the generated content text
        generated_text = response.text

        # Start a chat session
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [prompt],
                },
                {
                    "role": "model",
                    "parts": [generated_text],
                },
            ]
        )

        # Send message to chat session
        chat_response = chat_session.send_message(prompt)

        st.write(chat_response.text)
