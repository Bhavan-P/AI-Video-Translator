#pip install moviepy speechrecognition pydub googletrans==4.0.0-rc1
#pip install gtts
import moviepy.editor as mp
import speech_recognition as sr
from googletrans import Translator  # Google Translate
from gtts import gTTS  # Google Text-to-Speech
import os

def extract_audio_from_video(video_path, audio_output_path):
    # Load video and extract audio
    video_clip = mp.VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_output_path)

def convert_speech_to_text(audio_file):
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    # Load the audio file
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)  # Capture all the audio data
    
    try:
        # Perform speech recognition
        text = recognizer.recognize_google(audio_data)  # Using Google Web Speech API
        print("Transcribed Text:\n", text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def translate_text(text, target_language='es'):
    # Initialize the Google Translator
    translator = Translator()
