import wx

from source.module.ModuleFileConfiguration import FILE_CONFIGURATION
from source.module.ModuleGrogAI import API_GROG


class PromptFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Setup Prompt", size=(600, 400))

        panel = wx.Panel(self)

        screen_width, screen_height = wx.GetDisplaySize()
        self.SetSize(int(0.8*screen_width) , int(0.8*screen_height))
        self.SetPosition((int(screen_width*0.1), int(0.1*screen_height)))


        # ======================
        # Row 1: top
        # ======================
        row1_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.all_config = FILE_CONFIGURATION.load_json()

        list_prompt = list(self.all_config["Prompt"].keys())

        lbl = wx.StaticText(panel, label="Select option:")
        self.combo = wx.ComboBox(
            panel,
            choices=list_prompt,
            style=wx.CB_READONLY,value=list_prompt[0]
        )

        row1_sizer.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 8)
        row1_sizer.Add(self.combo, 0)

        # ======================
        # Row 2: middle (full frame)
        # ======================
        self.text_ctrl = wx.TextCtrl(
            panel,
            style=wx.TE_MULTILINE,value=self.all_config["Prompt"][list_prompt[0]]
        )

        # ======================
        # Row 3: bottom (buttons on right)
        # ======================
        row3_sizer = wx.BoxSizer(wx.HORIZONTAL)

        btn_ok = wx.Button(panel, label="OK")
        btn_ok.Bind(wx.EVT_BUTTON,self.save)
        btn_cancel = wx.Button(panel, label="Cancel")

        row3_sizer.AddStretchSpacer()  # push buttons to the right
        row3_sizer.Add(btn_ok, 0, wx.RIGHT, 8)
        row3_sizer.Add(btn_cancel, 0)

        # ======================
        # Main layout
        # ======================
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.Add(row1_sizer, 0, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(self.text_ctrl, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        main_sizer.Add(row3_sizer, 0, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(main_sizer)

        f_sizer = wx.BoxSizer(wx.VERTICAL)
        f_sizer.Add(panel, 1, wx.EXPAND | wx.ALL, 0)

        self.text_ctrl.Bind(wx.EVT_TEXT, self.update_text)

        self.SetSizer(f_sizer)
        self.Centre()
        self.Show()

    def update_text(self,event):
        self.all_config["Prompt"][self.combo] = self.text_ctrl.GetValue()
        event.Skip()

    def save(self,event):
        FILE_CONFIGURATION.save_json(self.all_config)
        API_GROG.load_configuration()

if __name__ == "__main__":
    app = wx.App(False)
    frame = PromptFrame()
    app.MainLoop()
