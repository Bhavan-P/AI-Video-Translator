#pip install resemble
#pip install request
#pip install moviepy speechrecognition pydub googletrans==4.0.0-rc1
import moviepy.editor as mp
import speech_recognition as sr
from googletrans import Translator  # Google Translate
import requests
import resemble
# Initialize Resemble API
#place your api key
resemble.api_key = ""

# Step 1: Extract audio from video
def extract_audio_from_video(video_path, audio_output_path):
    video_clip = mp.VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_output_path)
    print(f"Audio extracted and saved to {audio_output_path}")

# Step 2: Convert the extracted audio to text (Speech-to-Text)
def convert_speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data)
        print("Transcribed Text:\n", text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

# Step 3: Translate the transcribed text to a target language
def translate_text(text, target_language='es'):
    translator = Translator()
    try:
        translation = translator.translate(text, dest=target_language)
        print(f"Translated Text to {target_language}:\n", translation.text)
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return None

# Step 4: Clone and translate the voice using Resemble API
def clone_and_translate(text, voice_uuid, project_id, language_code="es"):
    url = f"https://f.cluster.resemble.ai/synthesize"
    headers = {
        "Authorization": f"Token {resemble.api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "script": text,
        "voice_uuid": voice_uuid,
        "language_code": language_code
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print("Successfully cloned and translated voice.")
        return response.json()["audio_url"]
    else:
        print(f"Error: {response.text}")
        return None

# Main Program Flow
def video_translation_pipeline(video_path, voice_uuid, project_id, target_language='es'):
    audio_output_path = "extracted_audio.wav"
    
    # Step 1: Extract audio from the video
    extract_audio_from_video(video_path, audio_output_path)
    
    # Step 2: Convert speech to text
    transcribed_text = convert_speech_to_text(audio_output_path)
    
    # Step 3: Translate the transcribed text to the target language
    if transcribed_text:
        translated_text = translate_text(transcribed_text, target_language)
        
        if translated_text:
            print("Translation was successful.")
            
            # Step 4: Clone and translate the voice
            audio_url = clone_and_translate(translated_text, voice_uuid, project_id, language_code=target_language)
            if audio_url:
                print(f"Audio URL: {audio_url}")
        else:
            print("Translation failed.")
    else:
        print("Speech-to-text conversion failed.")

# Example usage
if __name__ == "__main__":
    video_path = "input_video.mp4"  # Specify your video file
    target_language = 'es'  # 'es' for Spanish, or any other language code
    voice_uuid = "your_cloned_voice_uuid"  # Replace with your cloned voice UUID
    project_id = "your_project_id"  # Replace with your project ID

    # Call the pipeline
    video_translation_pipeline(video_path, voice_uuid, project_id, target_language)
