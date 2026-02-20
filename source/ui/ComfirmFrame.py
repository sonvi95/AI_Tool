import threading

import wx

from source.module.Control.ModuleControler import ModuleControler
from source.module.Control.ModuleFileConfiguration import FILE_CONFIGURATION
from source.module.Control.ModuleSenario import Scenario
from source.ui.IcePhaseFrame import IcePhaseFrame
import wx.lib.newevent

# from source.ui.StartWindow import StartFrame

#data to test
configuration = {
    "Person": "You are a general practitioner.",
    "Background": "You are in a situation where, due to a high volume of patients, a mix-up in medical records occurred, leading to an incorrect initial diagnosis.",
    "Patient": "Ms. Hoài, 46 years old, generally healthy, married, and currently working as a chief accountant at a large corporation in Hanoi. She has a history of stomach pain."
}

#
ThreadDoneEvent, EVT_THREAD_DONE = wx.lib.newevent.NewEvent()

#class to catch the event
class WorkerThread(threading.Thread):
    def __init__(self, window, configuration):
        """
        this function use when it starts to run
        :rtype: None
        """
        super().__init__(daemon=True)
        self.window = window
        self.configuration = configuration

    def run(self):
        """
        the function is called when it starts to run
        """
        senario = Scenario(self.configuration)
        data_introduce = senario.get_introduce()
        senario.get_question()
        data_ice_phase = senario.get_data_ice_phase()
        print(data_introduce)
        print(data_ice_phase)
        emotion = senario.get_emotion()
        print(emotion)
        start_convertation = senario.start_convertation()
        evt = ThreadDoneEvent()
        wx.PostEvent(self.window, evt)

class ConfirmFrame(wx.Frame):
    def __init__(self,parent):
        """
        This function is called when it starts to run
        :param parent:
        """
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
        self.btn_right = wx.Button(panel, label="OK", size=(100, 35))

        btn_left.Bind(wx.EVT_BUTTON, self.on_back)
        self.btn_right.Bind(wx.EVT_BUTTON, self.on_ok)

        # -------- Bottom sizer --------
        bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bottom_sizer.Add(btn_left, 0, wx.ALL, 10)
        bottom_sizer.AddStretchSpacer()
        bottom_sizer.Add(self.btn_right, 0, wx.ALL, 10)

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
        self.Bind(EVT_THREAD_DONE, self.on_thread_done)

        self.Show()

    def show_text_information(self):
        """
        Show the text information of the scenario.
        """
        data_show = ''
        for key in self.configuration:
            data_show += key + ": " + self.configuration[key] + "\n"
        self.text_ctrl.SetValue(data_show)

    def on_ok(self, event):
        """
        the event is called when the ok button is pressed.
        :param event:
        """
        # threading.Thread(target=self.thread_function).start()
        # senario = Scenario(self.configuration)
        # data_introduce = senario.get_introduce()
        # data_ice_phase = senario.get_data_ice_phase()
        # question = senario.get_question()
        # IcePhaseFrame(self,self.configuration)
        # self.Show(False)
        self.btn_right.Disable()

        #call the worker thread,
        self.worker = WorkerThread(self,self.configuration)
        self.worker.start()

    def on_thread_done(self,evt):
        """
        after the worker thread has finished running, this function is called.
        :param evt:
        """
        IcePhaseFrame(self,self.configuration)
        self.Show(False)

    def thread_function(self,):
        """
        The thread function to get the template data.
        """
        data_introduce,data_ice_phase,emotion = ModuleControler.get_scenario_database(self.configuration)

        evt = ThreadDoneEvent()
        wx.PostEvent(self.window, evt)

    def on_back(self,event):
        """
        Back to main frame.
        :param event:
        """
        self.parent.Show(True)
        self.Destroy()

if __name__ == "__main__":
    app = wx.App()
    ConfirmFrame()
    app.MainLoop()
