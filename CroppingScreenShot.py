from PIL import Image
import os

# Paths
screenshot_folder = r"C:\Users\bsame\OneDrive\Desktop\SE\Screenshots"
output_folder = os.path.join(screenshot_folder, "Cropped")
label_file_path = os.path.join(screenshot_folder, "labels.txt")

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Define crop box (left, upper, right, lower)
# Adjust these values to match the area where the emoji is located on screen
crop_box = (1600, 820, 1680, 900) # Example values — you MUST tweak this based on your screen

# Process each labeled screenshot
with open(label_file_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, start=1):
        parts = line.strip().split(', ')
        screenshot_name = parts[0]

        screenshot_path = os.path.join(screenshot_folder, screenshot_name)
        cropped_path = os.path.join(output_folder, f'screenshot_{idx}.png')

        try:
            with Image.open(screenshot_path) as img:
                cropped_img = img.crop(crop_box)
                cropped_img.save(cropped_path)
                print(f"✅ Cropped and saved: {cropped_path}")
        except Exception as e:
            print(f"❌ Error processing {screenshot_name}: {e}")