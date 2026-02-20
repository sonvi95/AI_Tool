import pyttsx3


class Speak_V2():
    def __init__(self):
        self.recording = False
        self.engine = pyttsx3.init()
        # Select voice
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)  # try different indexes

        # Control speech
        self.engine.setProperty('rate', 130)  # slower = more natural
        self.engine.setProperty('volume', 1.0)  # 0.0 – 1.0

    def speak(self, text):
        print('speak: ',text)
        self.engine.say(text)
        self.engine.runAndWait()

    def stop(self):
        self.engine.stop()

PEAK_V2 = Speak_V2()