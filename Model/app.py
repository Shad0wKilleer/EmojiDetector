from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np
import tensorflow as tf

# === Load Model and Class Names ===
model = tf.keras.models.load_model("Model_v2.h5")
class_names = np.load("Label.pkl", allow_pickle=True)  # ← Was saved with np.save()

# === Init API ===
app = FastAPI()

# Optional: enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Predict Endpoint ===
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        image = Image.open(file.file).convert("RGB").resize((64, 64))
        image_array = np.expand_dims(np.array(image) / 255.0, axis=0)

        pred = model.predict(image_array)
        pred_index = np.argmax(pred)
        predicted_unicode = class_names[pred_index]  # <- Fixed line

        return {"predicted_unicode": predicted_unicode}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})