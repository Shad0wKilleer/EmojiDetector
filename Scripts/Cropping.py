from PIL import Image
import os

# Paths
screenshot_folder = r"C:\Users\bsame\OneDrive\Desktop\SE\Screenshots"
output_folder = os.path.join(screenshot_folder, "Cropped")
os.makedirs(output_folder, exist_ok=True)

# Continuous output index
current_index = 22837

# Base crop origin
base_left, base_top = 1603, 827

# All crop variations: (left_offset, top_offset, width, height)
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

# Get all screenshots
all_images = sorted(f for f in os.listdir(screenshot_folder) if f.endswith(".png"))

# For each variation, apply it to ALL images
for variation_index, (dx, dy, w, h) in enumerate(variations, start=1):
    print(f"\n🌀 Applying variation {variation_index} to all images...")

    for image_name in all_images:
        input_path = os.path.join(screenshot_folder, image_name)

        left = base_left + dx
        top = base_top + dy
        right = left + w
        bottom = top + h
        crop_box = (left, top, right, bottom)

        output_name = f"screenshot_{current_index}.png"
        output_path = os.path.join(output_folder, output_name)

        try:
            with Image.open(input_path) as img:
                cropped_img = img.crop(crop_box)
                cropped_img.save(output_path)
                print(f"✅ Saved: {output_name}")
                current_index += 1
        except Exception as e:
            print(f"❌ Error with {image_name}: {e}")
