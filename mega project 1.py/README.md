# Voice Assistant

A Python-based voice assistant that can perform various tasks through voice commands.

## Features
- Voice command recognition using Google Speech Recognition
- Text-to-speech response using gTTS
- Open websites (Google, LinkedIn, YouTube)
- Play music from a predefined library
- Fetch latest news headlines
- Interactive voice confirmation for exit

## Setup
1. Clone this repository
2. Install requirements: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your News API key
4. Run the assistant: `python main.py`

## Commands
- Say "Happy" to activate the assistant
- "open google/linkedin/youtube"
- "play [song name]"
- "news"
- "exit"

## Requirements
- Python 3.7+
- Internet connection for voice recognition and API calls
