import os
import pickle
import numpy as np
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from PIL import Image
import emoji

# Initialize the Flask application
app = Flask(__name__)

# === Load Model and Label Mapping ===

# Load label map from pickle file
def load_label_map(label_path):
    with open(label_path, 'rb') as f:
        return pickle.load(f)

# Define file paths for model and label map
MODEL_PATH = 'Model_V2.h5'
LABEL_PATH = 'Label.pkl'

# Load the trained Keras model and label dictionary
model = load_model(MODEL_PATH)
label_map = load_label_map(LABEL_PATH)

# === Helper Functions ===

# Preprocess uploaded image: convert to RGB, resize, normalize, reshape
def preprocess_image(image):
    image = image.convert('RGB')       # Ensure 3 channels
    image = image.resize((64, 64))     # Resize to expected input shape
    arr = np.array(image) / 255.0      # Normalize pixel values to [0, 1]
    arr = arr.reshape(1, 64, 64, 3)     # Reshape to model input: (1, H, W, C)
    return arr

# Convert codepoints string like "U+1F600" into actual emoji
def codepoints_to_emoji(codepoints_str):
    chars = [chr(int(cp.replace('U+', ''), 16)) for cp in codepoints_str.split()]
    return ''.join(chars)

# Convert emoji to human-readable name using emoji library
def get_emoji_name(emoji_str):
    name = emoji.demojize(emoji_str)
    if name != emoji_str:
        return name.replace(':', '').replace('_', ' ').strip()
    else:
        return "Unknown"

# === Routes ===

# Route: Home page
@app.route('/')
def index():
    return render_template('index.html')

# Route: Prediction endpoint (accepts POST requests with image file)
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    try:
        image = Image.open(file.stream)         # Load image from request
        arr = preprocess_image(image)           # Preprocess for prediction
        pred = model.predict(arr)               # Make prediction
        class_idx = int(np.argmax(pred))        # Get predicted class index
        codepoints = label_map[class_idx] if class_idx < len(label_map) else str(class_idx)  # Get label
        return jsonify({'label': codepoints})   # Return label as JSON
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Handle errors gracefully

# === Run App ===

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
