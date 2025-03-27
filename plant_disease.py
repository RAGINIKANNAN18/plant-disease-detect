from flask import Flask, request, jsonify, render_template
import os
import google.generativeai as genai
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Gemini API Key (Replace with your actual key)
GEMINI_API_KEY = 'AIzaSyDeo_FSywoTQhoazTFyd-CUslFBuhg8lmM'

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Open image using PIL
        try:
            image = Image.open(filepath)
        except Exception as e:
            return jsonify({"error": f"Invalid image file: {str(e)}"})

        # Use Gemini AI to analyze the image for plant disease
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content([  
                "Analyze the image and identify any plant disease present. Provide the name of the disease, symptoms, and possible treatments.", 
                image
            ])

            if response and response.text:
                return jsonify({"prediction": response.text})
            else:
                return jsonify({"error": "No response from AI model"})
        
        except Exception as e:
            return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)