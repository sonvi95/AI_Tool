import os

import pyaudio
import wave
import numpy as np
import time
from pathlib import Path
import whisper

# =============================
# PARAMETERS
# =============================
RATE = 44100
CHUNK = 1024
CHANNELS = 1
FORMAT = pyaudio.paInt16

SILENCE_THRESHOLD = 100      # volume threshold (adjust if needed)
SILENCE_DURATION = 1.5         # seconds
MAXTIME_RECORD = 20

class RecorderAudio:
    def __init__(self):
        pass

    def is_silent(self, audio_data):
        """Check if audio chunk is silent"""
        # Convert to float to avoid overflow
        audio_data = audio_data.astype(np.float32)

        rms = np.sqrt(np.mean(audio_data ** 2))
        return rms < SILENCE_THRESHOLD

    def record_until_silence(self,output_file="audio"):
        audio = pyaudio.PyAudio()
        output_file = output_file+'.wav'
        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )

        frames = []
        silent_time = 0
        last_sound_time = time.time()
        start_time = last_sound_time
        print("🎙️ Recording... Speak now")

        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

            audio_np = np.frombuffer(data, dtype=np.int16)

            if not self.is_silent(audio_np):
                last_sound_time = time.time()

            silent_time = time.time() - last_sound_time

            if silent_time >= SILENCE_DURATION:
                print("🛑 Silence detected. Stop recording.")
                break

            if time.time() - start_time > MAXTIME_RECORD:
                print("Over time")
                break

        stream.stop_stream()
        stream.close()
        audio.terminate()

        with wave.open(output_file, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b"".join(frames))

        print(f"✅ Audio saved to {output_file}")

        return output_file

    def audio_to_text(self,audio_file, language="en"):
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")

        model = whisper.load_model("base")

        result = model.transcribe(
            str(audio_file),
            language=language,
            fp16=False
        )
        print('result: ',result["text"])
        return result["text"]

RECODER_AUDIO = RecorderAudio()




# if __name__ == "__main__":
#     RECODER_AUDIO.record_until_silence()
#     AUDIO_FILE = Path(__file__).parent / "audio.wav"
#     RECODER_AUDIO.audio_to_text(AUDIO_FILE)