import wx

from source.module.ModuleFileConfiguration import FILE_CONFIGURATION
from source.ui.DialogChangeName import ChangeDialog


class SetupFrame(wx.Frame):
    def __init__(self,parent):
        super().__init__(
            parent,
            title="ICE CREAM 2.0"
        )
        self.parent = parent
        screen_width, screen_height = wx.GetDisplaySize()
        self.SetSize(int(0.8*screen_width) , int(0.8*screen_height))
        self.SetPosition((int(screen_width*0.1), int(0.1*screen_height)))

        panel = wx.Panel(self)

        # ================= Center content =================
        center_sizer = wx.BoxSizer(wx.VERTICAL)

        self.all_configuration = FILE_CONFIGURATION.load_json()

        # ================= Person =================
        people = self.all_configuration["Scenario"]["Person"]
        person_row_sizer = wx.BoxSizer(wx.HORIZONTAL)

        person_label = wx.StaticText(panel, label="Person")
        self.person_combo = wx.ComboBox(panel,choices=list(people.keys()),style=wx.CB_READONLY)
        person_row_sizer.Add(person_label,  0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        person_row_sizer.Add(self.person_combo, 1, wx.EXPAND | wx.ALL, 10)

        self.person_text_ctrl = wx.TextCtrl(panel,style=wx.TE_MULTILINE,size=(-1, 60))

        group_people_sizer = wx.BoxSizer(wx.VERTICAL)
        group_people_sizer.Add(person_row_sizer, 0, wx.EXPAND | wx.BOTTOM, 5)
        group_people_sizer.Add(self.person_text_ctrl, 0, wx.EXPAND)

        center_sizer.Add(group_people_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # ================= Background =================
        background = self.all_configuration["Scenario"]["Background"]
        background_row_sizer = wx.BoxSizer(wx.HORIZONTAL)

        background_label = wx.StaticText(panel, label="Background")
        self.background_combo = wx.ComboBox(panel, choices=list(background.keys()), style=wx.CB_READONLY)
        background_row_sizer.Add(background_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        background_row_sizer.Add(self.background_combo, 1, wx.EXPAND | wx.ALL, 10)

        self.background_text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE, size=(-1, 60))

        group_background_sizer = wx.BoxSizer(wx.VERTICAL)
        group_background_sizer.Add(background_row_sizer, 0, wx.EXPAND | wx.BOTTOM, 5)
        group_background_sizer.Add(self.background_text_ctrl, 0, wx.EXPAND)

        center_sizer.Add(group_background_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # ================= Patient =================
        patient = self.all_configuration["Scenario"]["Patient"]
        patient_row_sizer = wx.BoxSizer(wx.HORIZONTAL)

        patient_label = wx.StaticText(panel, label="Patient")
        self.patient_combo = wx.ComboBox(panel, choices=list(patient.keys()), style=wx.CB_READONLY)
        patient_row_sizer.Add(patient_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        patient_row_sizer.Add(self.patient_combo, 1, wx.EXPAND | wx.ALL, 10)

        self.patient_text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE, size=(-1, 60))

        group_patient_sizer = wx.BoxSizer(wx.VERTICAL)
        group_patient_sizer.Add(patient_row_sizer, 0, wx.EXPAND | wx.BOTTOM, 5)
        group_patient_sizer.Add(self.patient_text_ctrl, 0, wx.EXPAND)

        center_sizer.Add(group_patient_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # ================= Bottom buttons =================
        btn_ok = wx.Button(panel, label="OK")
        btn_save = wx.Button(panel, label="Save")
        btn_add_remove = wx.Button(panel, label="Add/Remove/Change")
        btn_cancel = wx.Button(panel, label="Cancel")

        btn_cancel.Bind(wx.EVT_BUTTON, lambda e: self.Close())

        bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bottom_sizer.AddStretchSpacer()
        bottom_sizer.Add(btn_ok, 0, wx.ALL, 10)
        bottom_sizer.Add(btn_save, 0, wx.ALL, 10)
        bottom_sizer.Add(btn_add_remove, 0, wx.ALL, 10)
        bottom_sizer.Add(btn_cancel, 0, wx.ALL, 10)

        # ================= Main layout =================
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.Add(center_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
        main_sizer.AddStretchSpacer()
        main_sizer.Add(bottom_sizer, 0, wx.EXPAND)

        panel.SetSizer(main_sizer)

        self.setup_configuration()
        self.person_combo.Bind(wx.EVT_COMBOBOX,self.change_person)
        self.background_combo.Bind(wx.EVT_COMBOBOX, self.change_background)
        self.patient_combo.Bind(wx.EVT_COMBOBOX, self.change_patient)

        self.person_text_ctrl.Bind(wx.EVT_TEXT,self.update_text_person)
        self.background_text_ctrl.Bind(wx.EVT_TEXT, self.update_text_background)
        self.patient_text_ctrl.Bind(wx.EVT_TEXT, self.update_text_patient)

        btn_ok.Bind(wx.EVT_BUTTON, self.setup_ok)
        btn_save.Bind(wx.EVT_BUTTON,self.save_configuration)
        btn_add_remove.Bind(wx.EVT_BUTTON,self.add_remove)
        btn_cancel.Bind(wx.EVT_BUTTON,self.on_cancel)

        self.Show(True)

    def update_configuration(self,new_configuration):
        self.all_configuration = new_configuration

        configuration = self.all_configuration["Configuration"]

        self.person_combo.Set(list(self.all_configuration['Scenario']['Person'].keys()))
        self.background_combo.Set(list(self.all_configuration['Scenario']['Background'].keys()))
        self.patient_combo.Set(list(self.all_configuration['Scenario']['Patient'].keys()))

        self.person_combo.SetValue(configuration['Person'])
        self.background_combo.SetValue(configuration['Background'])
        self.patient_combo.SetValue(configuration['Patient'])

        self.person_text_ctrl.SetValue(self.all_configuration['Scenario']['Person'][configuration['Person']])
        self.background_text_ctrl.SetValue(self.all_configuration['Scenario']['Background'][configuration['Background']])
        self.patient_text_ctrl.SetValue(self.all_configuration['Scenario']['Patient'][configuration['Patient']])


    def change_person(self,event):
        print("change_person")
        value = self.person_combo.GetValue()
        self.update_scenario('Person',value)

    def change_background(self,event):
        print("change_background")
        value = self.background_combo.GetValue()
        self.update_scenario('Background',value)


    def change_patient(self,event):
        print("change_patient")
        value = self.patient_combo.GetValue()
        self.update_scenario('Patient',value)

    def update_scenario(self,key,data):
        self.all_configuration["Configuration"][key] = data
        if key == "Person":
            self.person_text_ctrl.SetValue(self.all_configuration['Scenario'][key][data])
        elif key == "Background":
            self.background_text_ctrl.SetValue(self.all_configuration['Scenario'][key][data])
        elif key == "Patient":
            self.patient_text_ctrl.SetValue(self.all_configuration['Scenario'][key][data])

    def setup_configuration(self):
        configuration = self.all_configuration["Configuration"]

        self.person_combo.SetValue(configuration['Person'])
        self.background_combo.SetValue(configuration['Background'])
        self.patient_combo.SetValue(configuration['Patient'])

        self.person_text_ctrl.SetValue(self.all_configuration['Scenario']['Person'][configuration['Person']])
        self.background_text_ctrl.SetValue(self.all_configuration['Scenario']['Background'][configuration['Background']])
        self.patient_text_ctrl.SetValue(self.all_configuration['Scenario']['Patient'][configuration['Patient']])

    def update_text_person(self,evt):
        person = self.person_combo.GetValue()
        self.all_configuration["Scenario"]['Person'][person] = self.person_text_ctrl.GetValue()

    def update_text_background(self,evt):
        background = self.background_combo.GetValue()
        self.all_configuration["Scenario"]['Background'][background] = self.background_text_ctrl.GetValue()

    def update_text_patient(self,evt):
        patient = self.patient_combo.GetValue()
        self.all_configuration["Scenario"]['Patient'][patient] = self.patient_text_ctrl.GetValue()

    def setup_ok(self,evt):
        self.Destroy()
        self.parent.Show(True)

    def save_configuration(self,evt):
        FILE_CONFIGURATION.save_json(self.all_configuration)
        self.Destroy()
        self.parent.Show(True)

    def add_remove(self,evt):
        ChangeDialog(self).ShowModal()

    def on_cancel(self,evt):
        self.Destroy()
        self.parent.Show(True)

if __name__ == "__main__":
    app = wx.App()
    SetupFrame(None)
    app.MainLoop()
