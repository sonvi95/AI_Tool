import re
import threading
import time

import wx
from pathlib import Path

from source.module.ModuleAudio import RECODER_AUDIO
from source.module.ModuleGrogAI import API_GROG
from source.module.ModuleSpeak import SPEAK
from source.module.ModuleSpeechToText import SPEECH_TO_TEXT
from source.ui.PanelCamera import PanelCamera
from source.ui.mainFrame import MainFrame


class LeftTopPanel(wx.Panel):
    def __init__(self, parent,size):
        wx.Panel.__init__(self, parent, size=size)
        self.SetBackgroundColour('white')
        self.panel_camera = PanelCamera(self)
        self.panel_camera.SetBackgroundColour('white')
        empty_panel = wx.Panel(self)
        empty_panel.SetBackgroundColour("white")
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.panel_camera, 1, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(empty_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(main_sizer)

class RightPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        ASSET_DIR = Path("D:/code/data/icon")

        # Load images ONCE
        # self.bmp_close = wx.Bitmap(str(ASSET_DIR / "man_doctor_close_mouth.png"))
        # self.bmp_close = wx.Bitmap(str(ASSET_DIR / "man_doctor_silent.png"))

        # self.bmp_open  = wx.Bitmap(str(ASSET_DIR / "man_doctor_open_mouth.png"))
        # self.bmp_open  = wx.Bitmap(str(ASSET_DIR / "man_doctor_litter_mouth.png"))


        self.list_picture = []
        for i in range(0,13):
            self.list_picture.append(str(Path("D:/code/data/face") / f"face{i}.png"))

        self.bmp_close = wx.Bitmap(self.list_picture[0])
        self.bmp_open = wx.Bitmap(self.list_picture[0])

        # Show initial image
        self.bitmap = wx.StaticBitmap(self, bitmap=self.bmp_close)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddStretchSpacer()
        sizer.Add(self.bitmap, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, 10)
        self.SetSizer(sizer)

        self.is_open = False
        self.status = True

    def on_switch(self):
        if self.status == False:
            return
        self.status = False
        thread = threading.Thread(target=self.thread_switch)
        thread.start()

    def off_switch(self):
        self.status = True

    def thread_switch(self):
        while True:
            for picture in self.list_picture:
                if self.status:
                    return
                self.bitmap.SetBitmap(wx.Bitmap(picture))

                time.sleep(0.2)
                self.Layout()

            # if self.status:
            #     return
            # try:
            #     if self.is_open:
            #         self.bitmap.SetBitmap(self.bmp_close)
            #     else:
            #         self.bitmap.SetBitmap(self.bmp_open)
            #
            #     self.is_open = not self.is_open
            #     self.Layout()
            #     time.sleep(0.5)
            # except:
            #     return


class CreamFrame(MainFrame):
    def __init__(self,parent,configuration):
        MainFrame.__init__(self,parent)
        self.status_bar = self.CreateStatusBar()
        self.status_bar.SetStatusText("Ready")
        self.status = True

        self.configuration = configuration
        screen_width, screen_height = wx.GetDisplaySize()
        self.SetSize(int(0.8*screen_width) , int(0.8*screen_height))
        self.SetPosition((int(screen_width*0.1), int(0.1*screen_height)))

        self.SetBackgroundColour('white')
        main_panel = wx.Panel(self)

        # -------- TOP AREA --------
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Small panel (top-left)
        self.left_panel = LeftTopPanel(main_panel, size=(200, -1))

        # Big panel (top-right, center area)
        self.right_panel = RightPanel(main_panel)
        self.right_panel.SetBackgroundColour(wx.WHITE)

        top_sizer.Add(self.left_panel, 0, wx.EXPAND | wx.ALL, 5)
        top_sizer.Add(self.right_panel, 1, wx.EXPAND | wx.ALL, 5)

        # -------- BOTTOM AREA --------
        bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)

        button = wx.Button(main_panel, label="Start")
        bottom_sizer.AddStretchSpacer()
        bottom_sizer.Add(button, 0, wx.ALL, 10)
        bottom_sizer.AddStretchSpacer()

        # -------- MAIN SIZER --------
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(top_sizer, 1, wx.EXPAND)
        main_sizer.Add(bottom_sizer, 0, wx.EXPAND)

        main_panel.SetSizer(main_sizer)


        thread_camera = threading.Thread(target=self.left_panel.panel_camera.start_camera)
        thread_camera.start()

        button.Bind(wx.EVT_BUTTON,self.on_run)
        self.Bind(wx.EVT_CLOSE,self.on_close)
        self.Show()

        self.status_running = 'None'
        self.list_data_speak = []
        self.conversation = ''
        threading.Thread(target=self.thread_prepare).start()

    def on_run(self,event):
        thread = threading.Thread(target=self.thread_speak)
        thread.start()

    def thread_speak(self):
        print('thread_speak')
        s_time = time.time()
        flag = False
        while True:
            if not self.status: break
            if self.list_data_speak == [] and self.status_running == 'None' and flag:
                self.right_panel.off_switch()
                break
            if self.list_data_speak != []:
                flag  = True
                self.right_panel.on_switch()
                mp3_fp = self.list_data_speak.pop(0)
                SPEAK.speak_no_save(mp3_fp)

            else:
                time.sleep(0.01)

        while True:

            responce = SPEECH_TO_TEXT.speech_to_text()

            self.conversation += "Patient: "+responce+'\n'

            if not self.status: break

            self.status_running ='Next'
            while True:
                if self.status_running == 'None' and self.list_data_speak == []:
                    self.right_panel.off_switch()
                    break

                else:
                    if self.list_data_speak != []:
                        self.right_panel.on_switch()
                        mp3_fp = self.list_data_speak.pop(0)
                        SPEAK.speak_no_save(mp3_fp)

                    else:
                        time.sleep(0.01)
                if not self.status: break

            if time.time()-s_time > 600:
                break



    def thread_prepare(self):
        self.status_running = "Prepare"
        print(self.status_running)
        data = API_GROG.get_sentence_to_start(self.configuration)
        print(data)
        sentences = re.split('[.]', data)
        for sentence in sentences:
            if sentence.split() == '':
                continue
            mp3_fp = SPEAK.prepare_speak_no_save(sentence)
            self.list_data_speak.append(mp3_fp)

        self.status_running ='None'
        print(self.status_running)
        self.conversation += "Doctor: "+data+'\n'
        while True:
            if self.status_running != 'None':
                new_answer = API_GROG.continue_conversation(self.configuration, self.conversation)
                self.conversation+= "Doctor: "+new_answer+'\n'
                sentences = re.split('[.]', new_answer)
                for sentence in sentences:
                    if sentence.split() == '':
                        continue
                    mp3_fp = SPEAK.prepare_speak_no_save(sentence)
                    self.list_data_speak.append(mp3_fp)

                self.status_running = 'None'
            else:
                time.sleep(0.01)
            if not self.status: break
    def on_close(self,evt):
        self.right_panel.off_switch()
        self.left_panel.panel_camera.stop_camera()
        SPEAK.stop_speak()
        self.status = False
        evt.Skip()

if __name__ == "__main__":
    app = wx.App(False)
    CreamFrame(None)
    app.MainLoop()
