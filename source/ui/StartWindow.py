import wx

from source.ui.ComfirmFrame import ConfirmFrame
from source.ui.FramePrompt import PromptFrame
from source.ui.SetupFrame import SetupFrame


class StartFrame(wx.Frame):
    def __init__(self):
        """
        Create frame when app starts.
        :rtype: None
        """
        super().__init__(None, title="ICE CREAM 2.0", size=(300, 300))

        panel = wx.Panel(self)

        btn_start = wx.Button(panel, label="Start", size=(120, 35))
        btn_setup  = wx.Button(panel, label="Setup",  size=(120, 35))
        btn_prompt = wx.Button(panel, label="Prompt", size=(120, 35))
        btn_exit  = wx.Button(panel, label="Exit",  size=(120, 35))

        btn_exit.Bind(wx.EVT_BUTTON, lambda e: self.Close())

        # Vertical sizer
        v_sizer = wx.BoxSizer(wx.VERTICAL)

        # Push buttons to vertical center
        v_sizer.AddStretchSpacer()

        # Add buttons centered horizontally
        v_sizer.Add(btn_start, 0, wx.ALL | wx.CENTER, 10)
        v_sizer.Add(btn_setup,  0, wx.ALL | wx.CENTER, 10)
        v_sizer.Add(btn_prompt, 0, wx.ALL | wx.CENTER, 10)
        v_sizer.Add(btn_exit,  0, wx.ALL | wx.CENTER, 10)


        # Push buttons to vertical center
        v_sizer.AddStretchSpacer()

        panel.SetSizer(v_sizer)

        btn_start.Bind(wx.EVT_BUTTON,self.run_start)
        btn_setup.Bind(wx.EVT_BUTTON,self.run_setup)
        btn_prompt.Bind(wx.EVT_BUTTON, self.on_prompt)

        self.Show()

    def run_start(self,event):
        """
        This function is used to execute the Confirmly frame.
        :rtype: None
        """
        confirm_frame = ConfirmFrame(self)
        self.Show(False)

    def on_prompt(self,evt):
        """
        The function is used to execute the Prompt frame.
        :param evt:
        """
        PromptFrame()

    def run_setup(self,event):
        """
        The function is used to execute the SetupFrame frame.
        :param event:
        """
        SetupFrame(self)
        self.Show(False)

if __name__ == "__main__":
    app = wx.App()
    StartFrame()
    app.MainLoop()
