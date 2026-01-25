import wx

class ChangeDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="ICE CREAM 2.0")
        main = wx.BoxSizer(wx.VERTICAL)
        self.parent = parent
        print(id(self.parent.all_configuration))
        self.all_configuration = self.parent.all_configuration.copy()
        print('all_configuration: ',id(self.all_configuration))
        self.form = wx.FlexGridSizer(cols=2, hgap=10, vgap=8)
        self.form.AddGrowableCol(1, 1)

        # Row 1
        self.form.Add(wx.StaticText(self, label="Select item:"), 0, wx.ALIGN_TOP)
        self.type_key = wx.ComboBox(self, choices=list(self.all_configuration["Scenario"].keys()),value=list(self.all_configuration["Scenario"].keys())[0],style=wx.CB_READONLY)
        self.form.Add(self.type_key, 1, wx.EXPAND)

        # Row 2
        self.form.Add(wx.StaticText(self, label="Action:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.radio = wx.RadioBox(
            self,
            choices=["Add", "Remove", "Change"],
            majorDimension=3,
            style=wx.RA_SPECIFY_COLS
        )
        self.radio.Bind(wx.EVT_RADIOBOX, self.on_radio_change)
        self.form.Add(self.radio, 1, wx.EXPAND)

        # ---------- Row 3 ----------
        self.value_label = wx.StaticText(self, label="Value:")
        self.form.Add(self.value_label, 0, wx.ALIGN_CENTER_VERTICAL)

        # Panel to swap controls
        self.value_panel = wx.Panel(self)
        value_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.value_text = wx.TextCtrl(self.value_panel)
        self.value_combo = wx.ComboBox(
            self.value_panel,
            style=wx.CB_READONLY
        )

        value_sizer.Add(self.value_text, 1, wx.EXPAND)
        value_sizer.Add(self.value_combo, 1, wx.EXPAND)

        self.value_panel.SetSizer(value_sizer)

        # Default state → TextCtrl visible
        self.value_combo.Hide()

        self.form.Add(self.value_panel, 1, wx.EXPAND)

        # Dynamic row
        self.new_value_label = wx.StaticText(self, label="New value:")
        self.dynamic_panel = wx.Panel(self)
        dyn = wx.BoxSizer(wx.HORIZONTAL)
        self.new_value = wx.TextCtrl(self.dynamic_panel)
        dyn.Add(self.new_value, 1, wx.EXPAND)
        self.dynamic_panel.SetSizer(dyn)

        self.form.Add(self.new_value_label, 0, wx.ALIGN_TOP)
        self.form.Add(self.dynamic_panel, 1, wx.EXPAND)

        # 🔴 hide BOTH
        self.new_value_label.Hide()
        self.dynamic_panel.Hide()

        main.Add(self.form, 1, wx.EXPAND | wx.ALL, 12)

        # Buttons
        btns = wx.BoxSizer(wx.HORIZONTAL)
        btns.AddStretchSpacer()
        btn_ok = wx.Button(self, wx.ID_OK, "OK")
        btn_cancel = wx.Button(self, wx.ID_CANCEL, "Cancel")
        btns.Add(btn_ok, 0, wx.RIGHT, 10)
        btns.Add(btn_cancel, 0)
        main.Add(btns, 0, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(main)
        self.Fit()

        self.type_key.Bind(wx.EVT_COMBOBOX,self.on_select_item)
        btn_ok.Bind(wx.EVT_BUTTON,self.on_ok)
        btn_cancel.Bind(wx.EVT_BUTTON,self.on_cancel)

    def on_ok(self, event):
        selection = self.radio.GetStringSelection()
        if selection in ("Remove", "Change"):
            select_value = self.value_combo.GetValue()
        else:
            select_value = self.value_text.GetValue()
        selection = self.radio.GetStringSelection()
        type_data = self.type_key.GetValue()
        print('select_value: ',select_value,'selection: ',selection,'type_data: ',type_data)
        if select_value == "":
            wx.MessageBox("Please select an item!", "Error", wx.ICON_ERROR)
            print('1')
        else:
            if selection == "Change":
                if self.new_value.GetValue() == "":
                    wx.MessageBox("Please select an item!", "Error", wx.ICON_ERROR)
                else:
                    new_value = self.new_value.GetValue()
                    if new_value not in self.all_configuration["Scenario"][type_data]:
                        self.all_configuration["Scenario"][type_data][new_value] = self.all_configuration["Scenario"][type_data][select_value]
                        del self.all_configuration["Scenario"][type_data][select_value]
                        if select_value == self.all_configuration["Configuration"][type_data]:
                            self.all_configuration["Configuration"][type_data] = new_value
                        self.parent.update_configuration(self.all_configuration)
                        self.Destroy()
                    else:
                        wx.MessageBox("The value exists!", "Error", wx.ICON_ERROR)
            elif selection == "Remove":
                if len(self.all_configuration["Scenario"][type_data]) != 0:
                    del self.all_configuration["Scenario"][type_data][select_value]
                    if select_value == self.all_configuration["Configuration"][type_data]:
                        self.all_configuration["Configuration"][type_data]=list(self.all_configuration["Scenario"][type_data].keys())[0]
                    self.parent.update_configuration(self.all_configuration)
                    self.Destroy()
                else:
                    wx.MessageBox("Can not delete the last item!", "Error", wx.ICON_ERROR)
            else:
                if select_value not in self.all_configuration["Scenario"][type_data]:
                    self.all_configuration["Scenario"][type_data][select_value] = ""
                    self.parent.update_configuration(self.all_configuration)
                    self.Destroy()
                else:
                    wx.MessageBox("The value exists!", "Error", wx.ICON_ERROR)


    def on_cancel(self, event):
        self.Destroy()

    def on_select_item(self,event):
        selection = self.radio.GetStringSelection()
        use_combo = selection in ("Remove", "Change")
        if use_combo:
            type_data = self.type_key.GetValue()
            list_options = list(self.all_configuration["Scenario"][type_data].keys())
            self.value_combo.Set(list_options)

    def on_radio_change(self, event):
        selection = self.radio.GetStringSelection()

        # Row 3: swap control
        use_combo = selection in ("Remove", "Change")
        self.value_text.Show(not use_combo)
        self.value_combo.Show(use_combo)

        if use_combo:
            type_data = self.type_key.GetValue()
            list_options = list(self.all_configuration["Scenario"][type_data].keys())
            self.value_combo.Set(list_options)


        # Dynamic row (row 4)
        show_dynamic = selection == "Change"
        self.new_value_label.Show(show_dynamic)
        self.dynamic_panel.Show(show_dynamic)

        self.Layout()
        self.Fit()


if __name__ == "__main__":
    app = wx.App(False)
    ChangeDialog(None).ShowModal()
    app.MainLoop()
