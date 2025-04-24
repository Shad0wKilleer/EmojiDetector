from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import numpy as np
import tensorflow as tf

# === Load Model and Classes ===
model = tf.keras.models.load_model("emoji_unicode_model.h5")
class_names = np.load("unicode_classes.npy")

# === Init API ===
app = FastAPI()


# === Predict Endpoint ===
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Load and preprocess image
        image = Image.open(file.file).convert("RGB").resize((64, 64))
        image_array = np.expand_dims(np.array(image) / 255.0, axis=0)

        # Predict
        pred = model.predict(image_array)
        predicted_unicode = class_names[np.argmax(pred)]

        return {"predicted_unicode": predicted_unicode}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
