import time

import wx
import cv2
import threading

from source.module.DeepFaceThread import DeepFaceThread


class PanelCamera(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.cap = None
        self.latest_frame = None
        self.running = False

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.Bind(wx.EVT_PAINT, self.on_paint)

    # -------- Thread: read camera --------
    def camera_thread(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.latest_frame = frame.copy()

    # -------- UI timer --------
    def on_timer(self, event):
        self.Refresh(False)   # trigger EVT_PAINT

    # -------- Paint event --------
    def on_paint(self, event):
        if self.latest_frame is None:
            return

        dc = wx.BufferedPaintDC(self)
        dc.Clear()
        frame = cv2.flip(self.latest_frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        w, h = self.GetClientSize()
        frame = cv2.resize(frame, (w, h))

        bmp = wx.Bitmap.FromBuffer(w, h, frame)
        dc.DrawBitmap(bmp, 0, 0)

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.running = True
        threading.Thread(target=self.camera_thread, daemon=True).start()

        self.deepface_thread = DeepFaceThread(self)
        self.deepface_thread.start()

        # self.timer.Start(33)
        threading.Thread(target=self.update_refesh).start()

    def update_refesh(self):
        while self.running:
            self.Refresh(False)
            time.sleep(0.01)

    def stop_camera(self):
        self.running = False
        self.timer.Stop()
        if self.cap:
            self.cap.release()

        # print(self.latest_frame)