import time

import speech_recognition as sr

class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 1.0

    def speech_to_text(self):
        with sr.Microphone() as source:
            print("🎤 Speak now...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source)

        text = ''
        try:
            text = self.recognizer.recognize_google(audio, language="en-US")
            print("📝 Text:", text)
        except sr.UnknownValueError:
            print("❌ Could not understand audioQ")
        except sr.RequestError as e:
            print("❌ API error:", e)
        return text

SPEECH_TO_TEXT = SpeechToText()

if __name__ == "__main__":
    SPEECH_TO_TEXT.speech_to_text()
    time.sleep(5)
    print('Next')
    SPEECH_TO_TEXT.speech_to_text()