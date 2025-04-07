import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary  # Fixed spelling
from gtts import gTTS
import pygame
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

recognizer = sr.Recognizer()
ttsx = pyttsx3.init()
newsapi = os.getenv("NEWS_API_KEY")

def speak(text):
    temp_file = "temp.mp3"
    try:
        tts = gTTS(text)
        tts.save(temp_file)

        pygame.mixer.init()
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.delay(100)

        pygame.mixer.music.stop()
        pygame.mixer.quit()
    
    except Exception as e:
        print(f"Error in speak function: {e}")
    finally:
        # Always try to remove the temp file
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception as e:
                print(f"Error removing temp file: {e}")

def processCommand(c):
    c = c.lower()
    if "open google" in c:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    
    elif "open linkedin" in c:
        speak("Opening Linkedin")
        webbrowser.open("https://www.linkedin.com")
  
    elif "open youtube" in c:
        speak("Opening Youtube")
        webbrowser.open("https://www.youtube.com")
        
    elif c.startswith("play"):
        try:
            song = c.split(" ", 1)[1]
            if song in musiclibrary.music:
                webbrowser.open(musiclibrary.music[song])
                speak(f"Playing {song}")
            else:
                speak(f"Sorry, I couldn't find the song {song}.")
        except IndexError:
            speak("Please specify the song name after 'play'.")
        except Exception as e:
            speak(f"An error occurred: {e}")
    
    elif "news" in c:
        try:
            if not newsapi or len(newsapi) != 32:
                speak("Invalid or missing News API key.")
                return
            
            r = requests.get(f"https://newsapi.org/v2/top-headlines?apiKey={newsapi}")
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])
                if articles:
                    speak("Here are the top news headlines:")
                    for article in articles[:5]:
                        speak(article['title'])
                else:
                    speak("Sorry, I couldn't find any news articles.")
            else:
                speak("Failed to fetch news. Please try again later.")
        except Exception as e:
            speak(f"An error occurred while fetching news: {e}")
    else:
        speak("Sorry, I didn't understand that command.")

if __name__ == "__main__":
    speak("Initializing Happy...")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            
            print("Recognizing...")
            word = recognizer.recognize_google(audio)
            print(f"You said: {word}")
            
            if word.lower() == "happy":
                speak("How can I assist you?")
                with sr.Microphone() as source:
                    print("Happy Active...")
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
                    command = recognizer.recognize_google(audio)
                    print(f"Command received: {command}")
                    processCommand(command)
            
            elif "exit" in word.lower():
                speak("Are you sure you want to exit?")
                with sr.Microphone() as source:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    confirm = recognizer.recognize_google(audio).lower()
                    if "yes" in confirm:
                        speak("Goodbye!")
                        break
                    else:
                        speak("Resuming operations.")

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            speak("Sorry, I didn't catch that. Could you repeat?")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            speak("There seems to be an issue with the speech recognition service.")
        except Exception as e:
            print(f"Error: {e}")
            speak("An error occurred. Please try again.")

