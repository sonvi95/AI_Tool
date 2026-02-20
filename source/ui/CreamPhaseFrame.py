import re
import threading
import time

import sounddevice as sd
import cv2
import soundfile as sf
import wx
from pathlib import Path

from source.module.Cache.DiskCache import CACHE
from source.module.LLM.ModuleGrogAI import API_GROG
from source.module.Control.ModuleSenario import Scenario
from source.module.AudioModule.ModuleSpeak import SPEAK
from source.module.AudioModule.ModuleSpeechToText import SPEECH_TO_TEXT
from source.ui.PanelCamera import PanelCamera
from source.ui.mainFrame import MainFrame

class VideoPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.frame = None
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.Bind(wx.EVT_PAINT, self.on_paint)



    def on_paint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.Clear()

        if self.frame is not None:
            h, w = self.frame.shape[:2]
            panel_w, panel_h = self.GetClientSize()
            bmp = wx.Bitmap.FromBuffer(w, h, self.frame)
            dc.DrawBitmap(bmp, int((panel_w-w)/2), panel_h-h)


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

        self.stop_down = False

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
        self.video_panel = VideoPanel(main_panel)
        self.video_panel.SetBackgroundColour(wx.WHITE)
        self.txt_show = wx.TextCtrl(main_panel, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.BORDER_SUNKEN)
        # -------- STATE --------
        self.current_frame = None
        self.playing = False

        top_sizer.Add(self.left_panel, 0, wx.EXPAND | wx.ALL, 5)
        top_sizer.Add(self.video_panel, 1, wx.EXPAND | wx.ALL, 5)
        top_sizer.Add(self.txt_show, 1, wx.EXPAND | wx.ALL, 5)

        # -------- BOTTOM AREA --------
        bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.button = wx.Button(main_panel, label="Start")
        self.button.Disable()
        bottom_sizer.AddStretchSpacer()
        bottom_sizer.Add(self.button, 0, wx.ALL, 10)
        bottom_sizer.AddStretchSpacer()

        # -------- MAIN SIZER --------
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(top_sizer, 1, wx.EXPAND)
        main_sizer.Add(bottom_sizer, 0, wx.EXPAND)

        main_panel.SetSizer(main_sizer)

        thread_camera = threading.Thread(target=self.left_panel.panel_camera.start_camera)
        thread_camera.start()

        self.button.Bind(wx.EVT_BUTTON,self.on_run)
        self.Bind(wx.EVT_CLOSE,self.on_close)
        self.Show()

        self.status_running = 'None'
        self.list_data_speak = []
        self.conversation = ''
        self.emotion = False
        threading.Thread(target=self.thread_convation).start()

    def on_pain(self):
        while True:
            if self.current_frame is not None:
                self.video_panel.frame = self.current_frame
                self.video_panel.Refresh(False)


    def thread_convation(self):
        senario = Scenario(self.configuration)
        introduce = senario.get_introduce()
        emotion = senario.get_emotion()
        self.play_video_with_audio(introduce['content']+'\n'+emotion['content'], emotion['mp4'], emotion['wav'])

        while True:
            if self.left_panel.panel_camera.running:
                self.button.Enable()
                break
            if not self.status:
                break

    def play_video_with_audio(self,content,video_path, audio_path,time_wait= 0):
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(fps)
        if fps <= 0:
            fps = 25
        frame_time = 1.0 / fps
        # Load audio
        audio, sr = sf.read(audio_path, dtype="float32")
        # pygame.mixer.music.load(filename)
        # pygame.mixer.music.play()

        self.playing = True
        sd.stop()
        sd.play(audio, sr)
        start_time = time.time()
        if content != '':
            self.txt_show.SetValue(content)

        # start_time = time.time()
        frame_index = 0

        while cap.isOpened() and self.playing:
            if self.stop_down:
                break
            ret, frame = cap.read()
            if not ret:
                break
            s_t = time.time()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.current_frame = frame
            self.video_panel.frame = frame
            self.video_panel.Refresh(False)

            frame_index += 1
            expected = frame_index * frame_time
            actual = time.time() - start_time
            delay = expected - actual
            if delay > 0:
                time.sleep(delay)

        cap.release()
        sd.stop()
        self.playing = False


    def on_run(self,event):
        thread = threading.Thread(target=self.thread_speak)
        thread.start()

    def thread_speak(self):
        print('thread_speak')
        s_time = time.time()
        senario = Scenario(self.configuration)
        start = senario.start_convertation()
        self.play_video_with_audio('', start['mp4'], start['wav'])
        self.conversation+="Doctor: "+start['content']+'\n'
        while True:
            question = SPEECH_TO_TEXT.speech_to_text()
            # question ="How do you think I'm doing? I've been waiting here for over an hour! This place is ridiculous!"
            if question != '':
                self.conversation += "Patient: " + question + '\n'
                new_answer = API_GROG.continue_conversation(self.configuration, self.conversation)
                print(new_answer)
                self.conversation += "Doctor: " + new_answer + '\n'
                file_output = SPEAK.create_video(new_answer, CACHE.get_hash_value(self.conversation))
                self.play_video_with_audio('', file_output, file_output.replace('.mp4', '.wav'))
                # break
            if time.time()-s_time > 600:
                break
            if not self.status: break
        #
        #     responce = SPEECH_TO_TEXT.speech_to_text()
        #
        #     self.conversation += "Patient: "+responce+'\n'
        #
        #     if not self.status: break
        #
        #     self.status_running ='Next'
        #     while True:
        #         if self.status_running == 'None' and self.list_data_speak == []:
        #             self.right_panel.off_switch()
        #             break
        #
        #         else:
        #             if self.list_data_speak != []:
        #                 self.right_panel.on_switch()
        #                 mp3_fp = self.list_data_speak.pop(0)
        #                 SPEAK.speak_no_save(mp3_fp)
        #
        #             else:
        #                 time.sleep(0.01)
        #         if not self.status: break
        #
        #     if time.time()-s_time > 600:
        #         break



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
        # self.right_panel.off_switch()
        self.left_panel.panel_camera.stop_camera()
        # SPEAK.stop_speak()
        self.status = False
        evt.Skip()

if __name__ == "__main__":
    app = wx.App(False)
    CreamFrame(None)
    app.MainLoop()
