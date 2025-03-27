import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Configure Gemini AI
GEMINI_API_KEY = 'AIzaSyDeo_FSywoTQhoazTFyd-CUslFBuhg8lmM'
genai.configure(api_key=GEMINI_API_KEY)

# Streamlit UI
st.title("🌱 Plant Disease Detection with AI 🤖")
st.write("Upload an image of a plant leaf, and the AI will analyze it for diseases.")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Save file temporarily
    image = Image.open(uploaded_file)
    
    # Display uploaded image
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # AI Analysis Button
    if st.button("Analyze Image"):
        try:
            # Use Gemini AI to analyze the image
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content([
                "Analyze the image and identify any plant disease present. Provide the name of the disease, symptoms, and possible treatments.",
                image
            ])

            if response and response.text:
                st.subheader("Prediction Results:")
                st.write(response.text)
            else:
                st.error("No response from AI model.")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
