import cv2
import os

# === File Paths & Configuration ===

# Path to the input video file
video_path = "C:/Users/bsame/OneDrive/Desktop/Videos/Screen_Recording_20250302_125204.mp4"

# Directory where extracted frames will be saved
output_dir = "C:/Users/bsame/OneDrive/Desktop/Screenshots"
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't already exist

# Starting number for naming the saved frames
start_number = 1

# === Open and Validate Video ===

# Open the video file
cap = cv2.VideoCapture(video_path)

# Check if the video was successfully opened
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# === Frame Extraction Setup ===

# Get the video's frames per second (FPS)
fps = cap.get(cv2.CAP_PROP_FPS)

# Set frame interval to capture one frame every 2 seconds
frame_interval = int(fps * 2)

# Initialize counters
frame_count = 0         # Total number of frames processed
saved_count = start_number  # Current label number for saved frames

# === Frame Capture Loop ===

while True:
    ret, frame = cap.read()  # Read the next frame

    if not ret:
        break  # Exit loop if video has ended or frame read fails

    # Save frame at defined interval (every 2 seconds)
    if frame_count % frame_interval == 0:
        filename = os.path.join(output_dir, f"frame_{saved_count}.png")
        cv2.imwrite(filename, frame)  # Save the frame as PNG
        print(f"Saved: {filename}")
        saved_count += 1  # Increment file label

    frame_count += 1  # Increment frame tracker

# === Cleanup ===

cap.release()              # Release the video capture object
cv2.destroyAllWindows()    # Close all OpenCV windows

print("Frame extraction complete!")
