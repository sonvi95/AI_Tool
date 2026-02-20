import threading

from deepface import DeepFace
import time

class DeepFaceThread(threading.Thread):
    def __init__(self, panel):
        super().__init__(daemon=True)
        self.panel = panel
        self.running = True

    def run(self):
        while self.running:
            frame = self.panel.latest_frame
            if frame is not None:
                try:
                    result = DeepFace.analyze(
                        frame,
                        actions=["emotion"],
                        enforce_detection=False
                    )

                    # DeepFace returns list or dict
                    # if isinstance(result, list):
                    #     print('------------------------------------------------------------')
                    #     for idx, val in enumerate(result):
                    #         print('Face: ',idx)
                    #         print("Dominant emotion:", result[idx]["dominant_emotion"])
                    #         # print("Emotion scores:", result[idx]["emotion"])

                except Exception as e:
                    print("DeepFace error:", e)

            time.sleep(1.0)  # analyze every 1 second

    def stop(self):
        self.running = False
