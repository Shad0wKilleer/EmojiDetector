#%%
import os
import pickle
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping

# === Paths ===
image_folder = r"C:\Users\bsame\OneDrive\Desktop\SE\Screenshots\Cropped"
label_file = r"C:\Users\bsame\OneDrive\Desktop\SE\Screenshots\labels.txt"

# === Step 1: Load Labels ===
labels_dict = {}
with open(label_file, 'r', encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split(', ')
        if len(parts) == 3:
            filename, emoji, unicode_val = parts
            labels_dict[filename] = unicode_val

# === Step 2: Load and Preprocess Images ===
X = []
y = []

for fname in os.listdir(image_folder):
    if fname.endswith(".png") and fname in labels_dict:
        img_path = os.path.join(image_folder, fname)
        try:
            img = Image.open(img_path).convert("RGB").resize((64, 64))
            X.append(np.array(img) / 255.0)
            y.append(labels_dict[fname])
        except:
            print(f"Skipping {fname}, error loading image.")

X = np.array(X)
print(X.shape)

# === Step 3: Encode Labels ===
le = LabelEncoder()
y_encoded = le.fit_transform(y)
y_cat = to_categorical(y_encoded)

# ✅ Save LabelEncoder object as Label.pkl
with open("Label.pkl", "wb") as f:
    pickle.dump(le, f)

# === Save preprocessed data for reuse ===
np.save("X_data.npy", X)
np.save("y_data.npy", y_cat)

# === Randomize while keeping X and y_cat aligned ===
indices = np.arange(len(X))
np.random.shuffle(indices)
X = X[indices]
y_cat = y_cat[indices]

# === Step 4: Train/Test Split ===
X_train, X_test, y_train, y_test = train_test_split(X, y_cat, test_size=0.3, random_state=42)

# === Step 5: Data Augmentation ===
datagen = ImageDataGenerator(
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True
)
datagen.fit(X_train)

# === Step 6: Build Improved Model ===
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    BatchNormalization(),
    MaxPooling2D((2, 2)),

    Conv2D(64, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),

    Conv2D(128, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),

    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.5),
    Dense(len(le.classes_), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# === Step 7: Early Stopping ===
early_stop = EarlyStopping(patience=10, restore_best_weights=True)

# === Step 8: Train Model ===
history = model.fit(
    datagen.flow(X_train, y_train, batch_size=64),
    epochs=100,
    validation_data=(X_test, y_test),
    callbacks=[early_stop]
)

# === Step 9: Save Model ===
model.save("emoji_unicode_model.h5")
print("✅ Model saved as emoji_unicode_model.h5")
print("✅ Label encoder saved as Label.pkl")

# === Step 10: Evaluate Model ===
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"\n📊 Test Accuracy: {test_acc:.2%}")

# === Step 11: Plot Accuracy ===
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend()
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.show()

# === Step 12: Predict Sample Image ===
sample_image_path = os.path.join(image_folder, "screenshot_1904.png")
img = Image.open(sample_image_path).convert("RGB").resize((64, 64))
img_array = np.expand_dims(np.array(img) / 255.0, axis=0)

pred = model.predict(img_array)

# Load label encoder from Label.pkl
with open("Label.pkl", "rb") as f:
    le = pickle.load(f)

predicted_unicode = le.inverse_transform([np.argmax(pred)])[0]
print(f"🔤 Predicted Unicode: {predicted_unicode}")