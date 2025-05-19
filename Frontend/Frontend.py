import os
import pickle
import numpy as np
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from PIL import Image
import emoji

app = Flask(__name__)

# Load model and labels
def load_label_map(label_path):
    with open(label_path, 'rb') as f:
        return pickle.load(f)

MODEL_PATH = 'Model_V2.h5'
LABEL_PATH = 'Label.pkl'

model = load_model(MODEL_PATH)
label_map = load_label_map(LABEL_PATH)

# Preprocess image (assuming 48x48 grayscale, adjust if needed)
def preprocess_image(image):
    image = image.convert('RGB')  # convert to RGB
    image = image.resize((64, 64))
    arr = np.array(image) / 255.0
    arr = arr.reshape(1, 64, 64, 3)
    return arr

def codepoints_to_emoji(codepoints_str):
    chars = [chr(int(cp.replace('U+', ''), 16)) for cp in codepoints_str.split()]
    return ''.join(chars)

def get_emoji_name(emoji_str):
    name = emoji.demojize(emoji_str)
    if name != emoji_str:
        return name.replace(':', '').replace('_', ' ').strip()
    else:
        return "Unknown"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    try:
        image = Image.open(file.stream)
        arr = preprocess_image(image)
        pred = model.predict(arr)
        class_idx = int(np.argmax(pred))
        codepoints = label_map[class_idx] if class_idx < len(label_map) else str(class_idx)
        return jsonify({'label': codepoints})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 