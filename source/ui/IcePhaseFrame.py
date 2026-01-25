import re
import threading
import wx
from pathlib import Path
import time

from source.module.Module import split_text
from source.module.ModuleGrogAI import API_GROG
from source.module.ModuleSpeak import SPEAK
from source.module.ModuleSpeak_V2 import PEAK_V2
from source.ui.CreamPhaseFrame import CreamFrame
from source.ui.mainFrame import MainFrame


class BoardText(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, size=(300, 150))
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        self.text = wx.TextCtrl(
            self,
            value="",
            style=wx.TE_MULTILINE | wx.BORDER_NONE
        )

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)

    def on_size(self, event):
        w, h = self.GetClientSize()
        self.text.SetPosition((10, 10))
        self.text.SetSize((w - 20, h - 20))
        event.Skip()

    def on_paint(self, event):
        dc = wx.PaintDC(self)
        gc = wx.GraphicsContext.Create(dc)

        w, h = self.GetSize()

        # Nền bảng
        gc.SetBrush(wx.Brush(wx.Colour(245, 245, 235)))

        # Viền bảng
        gc.SetPen(wx.Pen(wx.Colour(90, 90, 90), 3))

        # Vẽ bảng (vừa nền vừa viền)
        gc.DrawRoundedRectangle(1, 1, w - 2, h - 2, 10)

    def on_write_text(self,text):
        self.text.AppendText(text)

class LeftPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        ASSET_DIR = Path("D:/code/data/icon")

        self.list_picture = []
        for i in range(0,13):
            self.list_picture.append(str(Path("D:/code/data/face") / f"face{i}.png"))
        print(self.list_picture)
        # Load images ONCE
        # self.bmp_close = wx.Bitmap(str(ASSET_DIR / "man_doctor_close_mouth.png"))
        # self.bmp_close = wx.Bitmap(str(ASSET_DIR / "man_doctor_silent.png"))

        self.bmp_close = wx.Bitmap(self.list_picture[0])

        # self.bmp_open  = wx.Bitmap(str(ASSET_DIR / "man_doctor_open_mouth.png"))
        # self.bmp_open  = wx.Bitmap(str(ASSET_DIR / "man_doctor_litter_mouth.png"))
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
        if  self.status:
            return
        self.status = True

    def thread_switch(self):
        while True:
            # if self.status:
            #     return
            # if self.is_open:
            #     self.bitmap.SetBitmap(self.bmp_close)
            # else:
            #     self.bitmap.SetBitmap(self.bmp_open)
            for picture in self.list_picture:
                if self.status:
                    return
                self.bitmap.SetBitmap(wx.Bitmap(picture))

                time.sleep(0.2)
                self.Layout()
            # self.is_open = not self.is_open
            # self.Layout()
            # time.sleep(0.7)



class IcePhaseFrame(MainFrame):
    def __init__(self,parent,configuration):
        MainFrame.__init__(self,parent)
        self.s_time = time.time()
        self.configuration = configuration
        self.stop_down = False

        self.list_data = []
        self.state = 'Get'
        #v1 v2
        thread_get_data = threading.Thread(target=self.thread_get_data_ice_phase)
        thread_get_data.start()
        self.list_show = []
        self.prepare_data = []
        #v1
        # thread_prepare = threading.Thread(target=self.thread_prepare)
        # thread_prepare.start()

        #v3
        threading.Thread(target=self.thread_show).start()
        thread_prepare = threading.Thread(target=self.thread_prepare_v3)
        thread_prepare.start()

        screen_width, screen_height = wx.GetDisplaySize()
        self.SetSize(int(0.8*screen_width) , int(0.8*screen_height))
        self.SetPosition((int(screen_width*0.1), int(0.1*screen_height)))

        self.parent = parent
        self.SetBackgroundColour("white")
        panel = wx.Panel(self)

        # ---------- Left small panel ----------
        self.left_panel = LeftPanel(panel)
        self.left_panel.SetBackgroundColour("white")
        self.left_panel.SetMinSize((300, -1))   # fixed width

        # ---------- Right big panel ----------
        self.right_panel = BoardText(panel)
        self.right_panel.SetBackgroundColour("white")

        # ---------- Bottom button ----------
        self.btn_bottom = wx.Button(panel, label="Start", size=(120, 40))
        self.btn_back = wx.Button(panel, label="Back", size=(120, 40))
        self.btn_skip = wx.Button(panel, label="Skip", size=(120, 40))
        self.btn_bottom.Disable()
        # ---------- Top area: left + right ----------
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_sizer.Add(self.left_panel,0,wx.EXPAND | wx.ALL,5)
        top_sizer.Add(self.right_panel,1,wx.EXPAND | wx.ALL,5)

        # ---------- Main layout ----------
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(top_sizer,1,wx.EXPAND)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        btn_sizer.Add(self.btn_back, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        btn_sizer.Add(self.btn_bottom,0,wx.ALL | wx.CENTER,10)
        btn_sizer.Add(self.btn_skip, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)

        main_sizer.Add(btn_sizer, 0, wx.ALL | wx.CENTER, 10)
        panel.SetSizer(main_sizer)
        print("IcePhaseFrame: ",time.time()-self.s_time)
        self.Show(True)

        self.Bind(wx.EVT_CLOSE,self.on_close)

        self.btn_bottom.Bind(wx.EVT_BUTTON,self.on_start)
        self.btn_back.Bind(wx.EVT_BUTTON,self.on_back)
        self.btn_skip.Bind(wx.EVT_BUTTON,self.on_skip)
        # thread_read_summary = threading.Thread(target=self.thread_read)
        # thread_read_summary.start()

        # self.prepare_data = []
        # thread_prepare = threading.Thread(target=self.thread_prepare)
        # thread_prepare.start()

        #v1
        # thread_speak = threading.Thread(target=self.thread_speak)
        # thread_speak.start()

        #v2
        # self.thread_speak_v2 = threading.Thread(target=self.thread_speak_v2)
        # self.thread_speak_v2.start()

        #v3
        thread_speak_v3 = threading.Thread(target=self.thread_speak_v3)
        thread_speak_v3.start()



    def thread_show(self):
        while True:
            if self.stop_down:
                break
            if self.list_show != []:
                data = self.list_show.pop(0)
                if data['type'] == 'introduce':
                    introduce = API_GROG.get_the_introduce_to_show(self.configuration)
                    self.right_panel.on_write_text(introduce)
                else:
                    data_speak = API_GROG.get_data_ice_phase_to_show(self.configuration['Patient'])
                    self.right_panel.on_write_text('\n\n'+data_speak)
            else:
                time.sleep(1)


    def thread_speak_v3(self):
        while True:
            if self.prepare_data != []:
                if self.stop_down:
                    break
                data_speak = self.prepare_data.pop(0)
                print('Speak: ', time.time() - self.s_time)
                self.left_panel.on_switch()
                # self.right_panel.on_write_text(data_speak['data'])
                SPEAK.speak_no_save(data_speak['mp3_fp'])
                # self.left_panel.off_switch()
            else:
                if self.state == 'Speak':
                    self.left_panel.off_switch()
                    break
                self.left_panel.off_switch()
                time.sleep(0.1)
        if not self.stop_down:
            self.state = 'Done'
            self.btn_bottom.Enable()

    def thread_speak_v2(self):
        while True:
            if self.list_data != []:
                data_check = self.list_data.pop(0)
                # print(data_check)
                lines = data_check.split('\n')
                self.left_panel.on_switch()
                for line in lines:
                    if line.strip() == '':
                        continue
                    if self.stop_down:
                        break
                    self.right_panel.on_write_text(line+'\n')
                    PEAK_V2.speak(line)
                self.left_panel.off_switch()
            else:
                if self.state == 'Prepare':
                    break
                time.sleep(0.1)



    def on_back(self,evt):
        self.stop_thread()
        self.parent.Show(True)
        self.Destroy()

    def on_skip(self,evt):
        # thread_stop = threading.Thread(target=self.stop_thread)
        # thread_stop.start()
        self.stop_thread()
        self.on_start(evt)

    def stop_thread(self):
        self.stop_down = True
        SPEAK.stop_speak()
        # PEAK_V2.stop()


    def thread_get_data_ice_phase(self):
        introduce = API_GROG.get_the_introduce(self.configuration)
        # print(introduce)
        self.list_data.append(introduce)
        data_speak = API_GROG.get_data_ice_phase(self.configuration['Patient'])
        # print(data_speak)
        self.list_data.append(data_speak)
        # print("Done thread_get_data_ice_phase")
        self.state = 'Prepare'

    def thread_prepare_v3(self):
        idx = 0
        first = True
        while True:
            if self.list_data != []:
                data_check = self.list_data.pop(0)
                # print(data_check)
                lines_after = re.split('[\n]',data_check)
                if first:
                    self.list_show.append({'data':data_check,'type':'introduce'})
                    line0 = lines_after[0]
                    lines0 = re.split('[.,]', line0)
                    lines = []
                    for l in lines0:
                        if lines == []:
                            lines.append(l)
                            continue
                        else:
                            if len(l) < 20 or len(lines[-1]) < 20:
                                d = lines.pop()
                                lines.append(d + l)
                            else:
                                lines.append(l)
                    lines += lines_after[1:]
                    first = False
                else:
                    self.list_show.append({'data': data_check, 'type': 'term'})
                    lines = lines_after


                # lines = split_text(data_check)
                for line in lines:
                    if line.strip()=='':
                        continue
                    if self.stop_down:
                        break
                    # data = line + '\n'
                    # file_speak = SPEAK.prepare_speak(data)
                    # self.left_panel.on_switch()
                    # self.right_panel.on_write_text(data)
                    # SPEAK.speak(file_speak)
                    # self.left_panel.off_switch()

                    mp3_fp = SPEAK.prepare_speak_no_save(line)
                    idx+=1
                    self.prepare_data.append({'data':line+'\n','mp3_fp':mp3_fp})
            else:
                if self.state == 'Prepare' :
                    break
                time.sleep(0.1)
        # print("Done thread_prepare")
        self.state = 'Speak'

    def thread_prepare(self):
        idx = 0
        while True:
            if self.list_data != []:
                data_check = self.list_data.pop(0)
                # print(data_check)
                lines = data_check.split('\n')
                for line in lines:
                    if line.strip()=='':
                        continue
                    if self.stop_down:
                        break
                    # data = line + '\n'
                    # file_speak = SPEAK.prepare_speak(data)
                    # self.left_panel.on_switch()
                    # self.right_panel.on_write_text(data)
                    # SPEAK.speak(file_speak)
                    # self.left_panel.off_switch()

                    file_speak = SPEAK.prepare_speak(line,'ice_phase_'+str(idx+time.time()))
                    idx+=1
                    self.prepare_data.append({'data':line+'\n','speak':file_speak})
            else:
                if self.state == 'Prepare' :
                    break
                time.sleep(1)
        # print("Done thread_prepare")
        self.state = 'Speak'

    def thread_speak(self):
        while True:
            if self.prepare_data != []:
                if self.stop_down:
                    break
                data_speak = self.prepare_data.pop(0)
                print('Speak: ',time.time()-self.s_time)
                self.left_panel.on_switch()
                self.right_panel.on_write_text(data_speak['data'])
                SPEAK.speak(data_speak['speak'])
                self.left_panel.off_switch()
            else:
                if self.state == 'Speak':
                    break
                time.sleep(1)
        self.state = 'Done'
        self.btn_bottom.Enable()

    def on_close(self,evt):
        self.stop_thread()
        self.left_panel.off_switch()
        evt.Skip()

    def thread_read(self):
        #introduce
        s_time = time.time()
        print('Start Reading: ',s_time)
        introduce = API_GROG.get_the_introduce(self.configuration)
        print('Time request : ', time.time() - s_time)
        s_time = time.time()
        lines= introduce.split("\n")
        for line in lines:
            if line.strip() == '':
                continue
            data = line + '\n'
            file_speak = SPEAK.prepare_speak(data)
            self.left_panel.on_switch()
            self.right_panel.on_write_text(data)
            SPEAK.speak(file_speak)
            self.left_panel.off_switch()
            print('Time speak : ', time.time() - s_time)
            s_time = time.time()

        data_speak = API_GROG.get_data_ice_phase(self.configuration['Patient'])
        lines = data_speak.split('.')
        print('Time request : ', time.time() - s_time)
        s_time = time.time()
        for line in lines:
            if line.strip() == '':
                continue
            data = line + '.'
            file_speak = SPEAK.prepare_speak(data)
            self.left_panel.on_switch()
            self.right_panel.on_write_text(data)
            SPEAK.speak(file_speak)
            self.left_panel.off_switch()
            print('Time speak : ', time.time() - s_time)
            s_time = time.time()

        self.btn_bottom.Enable()
    def on_start(self,evt):
        CreamFrame(self.parent,self.configuration)
        self.Destroy()


if __name__ == "__main__":
    app = wx.App()
    IcePhaseFrame(None)
    app.MainLoop()
