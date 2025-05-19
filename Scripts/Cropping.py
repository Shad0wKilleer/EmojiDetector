from PIL import Image
import os

# === Configuration ===

# Folder containing the original screenshots
screenshot_folder = r"C:\Users\bsame\OneDrive\Desktop\SE\Screenshots"

# Output folder where cropped images will be saved
output_folder = os.path.join(screenshot_folder, "Cropped")
os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

# Starting index for naming cropped output files
current_index = 22837

# Base coordinates (top-left corner) for cropping
base_left, base_top = 1603, 827

# List of crop variations: each tuple contains (left_offset, top_offset, width, height)
variations = [
    (-4, -4, 64, 64),
    (3, 2, 66, 66),
    (0, 0, 80, 80),
    (-5, 0, 70, 70),
    (2, -3, 72, 72),
    (-2, 5, 64, 64),
    (1, 1, 76, 76),
    (-6, -6, 80, 80),
    (0, 4, 68, 68),
    (-3, 2, 60, 60),
]

# Get a sorted list of all PNG screenshot filenames in the folder
all_images = sorted(f for f in os.listdir(screenshot_folder) if f.endswith(".png"))

# === Processing Images ===

# Apply each crop variation to all screenshots
for variation_index, (dx, dy, w, h) in enumerate(variations, start=1):
    print(f"\n🌀 Applying variation {variation_index} to all images...")

    # Iterate over every image in the screenshot folder
    for image_name in all_images:
        input_path = os.path.join(screenshot_folder, image_name)

        # Compute the crop box using the base coordinates and variation offset
        left = base_left + dx
        top = base_top + dy
        right = left + w
        bottom = top + h
        crop_box = (left, top, right, bottom)

        # Generate output filename and path
        output_name = f"screenshot_{current_index}.png"
        output_path = os.path.join(output_folder, output_name)

        # Open the image, apply the crop, and save the result
        try:
            with Image.open(input_path) as img:
                cropped_img = img.crop(crop_box)
                cropped_img.save(output_path)
                print(f"✅ Saved: {output_name}")
                current_index += 1  # Increment the file index for next output
        except Exception as e:
            print(f"❌ Error with {image_name}: {e}")
