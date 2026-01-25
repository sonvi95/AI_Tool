import wx

from source.ui.mainPanel import MainPanel


class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self,parent,title="ICE CREAM 2.0")
        icon = wx.Icon(r"D:\code\data\icon\icecream.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)


