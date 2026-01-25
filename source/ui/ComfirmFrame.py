import wx

from source.module.ModuleFileConfiguration import FILE_CONFIGURATION
from source.ui.IcePhaseFrame import IcePhaseFrame


# from source.ui.StartWindow import StartFrame

configuration = {
    "Person": "You are a general practitioner.",
    "Background": "You are in a situation where, due to a high volume of patients, a mix-up in medical records occurred, leading to an incorrect initial diagnosis.",
    "Patient": "Ms. Hoài, 46 years old, generally healthy, married, and currently working as a chief accountant at a large corporation in Hanoi. She has a history of stomach pain."
}


class ComfirmFrame(wx.Frame):
    def __init__(self,parent):
        super().__init__(
            parent,
            title="ICE CREAM 2.0",
            size=(800, 500)
        )
        self.parent = parent
        panel = wx.Panel(self)

        configuration = FILE_CONFIGURATION.load_json()
        self.configuration = {}
        for key in configuration["Configuration"]:
            sub_key = configuration["Configuration"][key]
            self.configuration[key] = configuration["Scenario"][key][sub_key]

        # -------- Expandable TextCtrl --------
        self.text_ctrl = wx.TextCtrl(
            panel,
            value="",
            style=wx.TE_MULTILINE
        )

        # -------- Bottom buttons --------
        btn_left = wx.Button(panel, label="Back", size=(100, 35))
        btn_right = wx.Button(panel, label="OK", size=(100, 35))

        btn_left.Bind(wx.EVT_BUTTON, self.on_back)
        btn_right.Bind(wx.EVT_BUTTON, self.on_ok)

        # -------- Bottom sizer --------
        bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bottom_sizer.Add(btn_left, 0, wx.ALL, 10)
        bottom_sizer.AddStretchSpacer()
        bottom_sizer.Add(btn_right, 0, wx.ALL, 10)

        # -------- Main layout --------
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Expandable TextCtrl
        main_sizer.Add(
            self.text_ctrl,
            1,  # <-- IMPORTANT (expand)
            wx.EXPAND | wx.ALL,
            10
        )

        # Bottom buttons
        main_sizer.Add(
            bottom_sizer,
            0,  # <-- fixed height
            wx.EXPAND
        )

        panel.SetSizer(main_sizer)
        self.show_text_information()

        self.Show()

    def show_text_information(self):
        data_show = ''
        for key in self.configuration:
            data_show += key + ": " + self.configuration[key] + "\n"
        self.text_ctrl.SetValue(data_show)

    def on_ok(self, event):
        IcePhaseFrame(self,self.configuration)
        self.Show(False)

    def on_back(self,event):
        self.parent.Show(True)
        self.Destroy()

if __name__ == "__main__":
    app = wx.App()
    ComfirmFrame()
    app.MainLoop()
