import speech_recognition as sr
import pyttsx3
import os
from chat import MODEL_NAME

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that."
        except sr.WaitTimeoutError:
            return "Timeout. Please try again."

def voice_assistant():
    print("Voice Assistant is active. Say 'exit' to stop.")
    while True:
        user_input = speech_to_text()
        if user_input.lower() == "exit":
            text_to_speech("Goodbye!")
            break

        print(f"You: {user_input}")
        os.system(f'ollama chat {MODEL_NAME} --input "{user_input}"')

if __name__ == "__main__":
    voice_assistant()
