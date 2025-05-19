from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np
import tensorflow as tf

# === Load the trained TensorFlow model and class labels ===
model = tf.keras.models.load_model("Model_v2.h5")

# Load the class names (unicode labels) saved previously with np.save()
class_names = np.load("Label.pkl", allow_pickle=True)

# === Initialize FastAPI app instance ===
app = FastAPI()

# === Enable Cross-Origin Resource Sharing (CORS) ===
# This allows API to be accessed from any origin (for development convenience)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],          # Allow all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],          # Allow all headers
)

# === Prediction endpoint ===
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Receives an image file uploaded by the user,
    preprocesses it, performs model prediction,
    and returns the predicted unicode class label.
    """
    try:
        # Open the uploaded image file, convert to RGB and resize to (64, 64)
        image = Image.open(file.file).convert("RGB").resize((64, 64))
        
        # Normalize pixel values to [0, 1] and expand dims for batch input shape
        image_array = np.expand_dims(np.array(image) / 255.0, axis=0)

        # Predict class probabilities using the model
        pred = model.predict(image_array)

        # Get the index of the highest probability
        pred_index = np.argmax(pred)

        # Map prediction index to the corresponding unicode class label
        predicted_unicode = class_names[pred_index]

        # Return the predicted unicode label as JSON
        return {"predicted_unicode": predicted_unicode}

    except Exception as e:
        # Return error message with HTTP 500 status code if prediction fails
        return JSONResponse(status_code=500, content={"error": str(e)})
