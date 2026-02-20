import os

from gtts import gTTS

import warnings

from source.module.Video.Wav2Lip.Wav2LipEngine import ENGINE_WAV

warnings.filterwarnings("ignore", category=UserWarning)
from io import BytesIO
import pygame
import time

class Speak():
    def __init__(self):
        """
        the contructor of the speaker. This function needs to call before starting the speaker.
        :rtype: None
        """
        pygame.mixer.init()

    def prepare_speak(self,text,file_name='output',lang="en"):
        """
        the function prepares the speaker. This function needs to call before starting the speaker.
        Use the value return form this fucntion to input to the speaker function.
        :param text: the text to speak
        :param lang: the language of the speaker
        :return:
        """
        filename = './result/'+file_name+".mp3"
        # Stop & unload previous audio
        # pygame.mixer.music.stop()
        # pygame.mixer.music.unload()
        try:
            # Delete old file safely
            if os.path.exists(filename):
                os.remove(filename)
        except:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

            # Delete old file safely
            if os.path.exists(filename):
                os.remove(filename)

        # Create new TTS
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)

        return filename

    def speak(self, filename):
        """
        the function speaks the speaker. This function needs to call before starting the speaker.
        :param filename:
        """
        # Play
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.2)

    def prepare_speak_no_save(self,text,lang="en"):
        """
        convert from text to mp3.
        :param text:
        :param lang:
        :return:
        """
        try:
            mp3_fp = BytesIO()
            tts = gTTS(text=text, lang=lang)
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            return mp3_fp
        except:
            return None

    def speak_no_save(self,mp3_fp):
        """
        play the mp3.
        :param mp3_fp:
        :return:
        """
        if mp3_fp is None:
            return None

        try:
            pygame.mixer.music.load(mp3_fp, "mp3")
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(0.2)
        except:
            return None

    def stop_speak(self):
        """
        stop speaking
        """
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    def create_video(self,text,file_name,lang="en"):
        """
        create the video form text
        :param text:
        :param file_name:
        :param lang:
        :return:
        """
        filename_wav = './result/'+file_name+".wav"
        # Stop & unload previous audio
        # pygame.mixer.music.stop()
        # pygame.mixer.music.unload()
        try:
            # Delete old file safely
            if os.path.exists(filename_wav):
                os.remove(filename_wav)
        except:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

            # Delete old file safely
            if os.path.exists(filename_wav):
                os.remove(filename_wav)
        tts = gTTS(text, lang="en")
        tts.save(filename_wav)

        filename_mp4 = './result/'+file_name+".mp4"
        # 2️⃣ AudioModule → Video
        ENGINE_WAV.infer(filename_wav, filename_mp4)
        return filename_mp4

SPEAK = Speak()

if __name__ == '__main__':
    data = SPEAK.prepare_speak_no_save("""All users now automatically start with a free one-month Pro trial. After that, you can subscribe to Pro or keep using the core features for free – now with Jupyter support included.

PyCharm Professional users are unaffected and will continue to enjoy full access to all Pro features in the unified product.""")
    SPEAK.speak_no_save(data)



