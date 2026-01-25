import time
import threading
import wx
from pathlib import Path

class ImageSwitchPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        ASSET_DIR = Path("D:/code/data/icon")

        # Load images ONCE
        self.bmp_close = wx.Bitmap(str(ASSET_DIR / "man_doctor_close_mouth.png"))
        self.bmp_open  = wx.Bitmap(str(ASSET_DIR / "man_doctor_open_mouth.png"))

        # Show initial image
        self.bitmap = wx.StaticBitmap(self, bitmap=self.bmp_close)


        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.bitmap, 0, wx.ALL | wx.CENTER, 10)
        self.SetSizer(sizer)

        self.is_open = False
        self.status = False

    def on_switch(self):
        thread = threading.Thread(target=self.thread_switch)
        thread.start()

    def thread_switch(self):
        while True:
            if self.status:
                return
            if self.is_open:
                self.bitmap.SetBitmap(self.bmp_close)
            else:
                self.bitmap.SetBitmap(self.bmp_open)

            self.is_open = not self.is_open
            self.Layout()
            time.sleep(0.5)
