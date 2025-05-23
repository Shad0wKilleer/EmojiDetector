# EmojiDetector

## Overview
EmojiDetector is a software engineering project aimed at extracting text and emojis from WhatsApp screenshots using a custom Convolutional Neural Network (CNN) model. The model is trained to filter text and emojis from the given screenshot and return the extracted text along with emoji Unicode representations with 99.99% accuracy.

## Features
- Accepts WhatsApp screenshots as input.
- Uses a CNN model for text and emoji detection.
- Outputs text and emojis in Unicode format.
- Designed for high accuracy and efficiency.
- Works without reliance on third-party APIs, ensuring complete control over data processing.

## Project Goals
- **Train a custom CNN model** to accurately detect and extract text and emojis from chat screenshots.
- **Achieve 99.99% accuracy** in production-level detection.
- **Ensure structured output** in JSON format containing text, emojis, and timestamps.
- **Deploy a dockerized solution** that can run in both cloud and local environments.

## Input & Output
- **Input:** WhatsApp chat screenshots.
- **Output:** JSON containing extracted text and emojis.

Example Output:
```json
{
  "message": "Hello! How are you?",
  "timestamp": "2024-01-01T12:34:56Z",
  "emojis": ["\ud83d\ude0a", "\ud83d\udc4d"]
}
```

## Development Requirements
- Python-based solution with a CNN model.
- Uses only open-source libraries (no third-party APIs).
- Fully dockerized for easy deployment.
- Must work with cloud and local resources.

## Milestones
0. **Starting Point:** Create a model that gives 60+ accuracy. 
1. **Prototype Milestone:** Achieve 95+% accuracy.
2. **Production Milestone:** Achieve 99.99% accuracy.
3. **Integration Milestone:** Ensure seamless deployment and performance.

## Repository Structure
```
/EmojiDetector
│── /data               # Labeled datasets for training
│── /models             # Trained CNN models
│── /src                # Source code for detection and extraction
│── /docker             # Dockerized setup
│── main.py             # Main entry point for processing
│── README.md           # Project documentation
```

## Setup & Installation
After completion. Project is still in development stage.
To set up the project locally:
```bash
git clone https://github.com/Shad0wKilleer/EmojiDetector.git
cd EmojiDetector
docker-compose up --build
```

## Contribution Guidelines
- Fork the repository.
- Create a feature branch.
- Commit your changes and submit a pull request.

##How to Run the Emoji Detector Web App
====================================

1. Install Python (if not already installed)
   - Download from https://www.python.org/downloads/

2. Open a terminal or command prompt in this project folder.

3. Install the required dependencies:
   pip install -r requirements.txt

4. Make sure these files are present in this folder:
   - app.py
   - Model_V2.h5
   - Label.pkl
   - requirements.txt
   - templates/index.html
   - static/style.css
   - static/script.js

  # these files are important for functioning of code.

5. Start the Flask server:
   python app.py


6. Open your web browser and go to:
   http://localhost:5000

7. Use the website:
   - Click "Choose an image" and select an emoji image.
   - Click "Detect Emoji" to get the unicode prediction.
   - Copy the unicode if needed, and view your prediction history below.

8. To stop the server:
   - Go to the terminal where it's running and press Ctrl+C.

If you have any issues, check the terminal for error messages or contact the developer for help.

## Contact
Please distrub someone else. I am too busy and outta your reach :)