import wx

from source.ui.PanelCamera import PanelCamera


class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        #add panel
        self.panel_camera = PanelCamera(self)

        #add buttom
        self.btn_start = wx.Button(self, wx.ID_ANY, "Start")
        self.btn_stop = wx.Button(self, wx.ID_ANY, "Stop")
        self.btn_start.Bind(wx.EVT_BUTTON, self.start_camera)
        self.btn_stop.Bind(wx.EVT_BUTTON, self.stop_camera)

        boot_sizer = wx.BoxSizer(wx.HORIZONTAL)
        boot_sizer.Add(self.btn_start, 0, wx.ALL, 5)
        boot_sizer.Add(self.btn_stop, 0, wx.ALL, 5)

        p_sizer = wx.BoxSizer(wx.VERTICAL)
        p_sizer.Add(self.panel_camera, 1, wx.EXPAND)
        p_sizer.Add(boot_sizer, 0, wx.ALL, 5)
        self.SetSizer(p_sizer)

    def start_camera(self,evt):
        self.panel_camera.start_camera()

    def stop_camera(self,evt):
        self.panel_camera.stop_camera()