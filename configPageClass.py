import wx

def configPage(self, sizer_5):
        self.panelConfig = wx.ScrolledWindow(self.topRightConfigPane, wx.ID_ANY, style=wx.TAB_TRAVERSAL)
        self.panelConfig.SetScrollRate(10, 10)
        sizer_5.Add(self.panelConfig, 2, wx.EXPAND, 0)
        grid_sizer_1 = wx.FlexGridSizer(14, 5, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)

        lblStorage = wx.StaticText(self.panelConfig, wx.ID_ANY, "Write local Logs:")
        grid_sizer_1.Add(lblStorage, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        self.cbxUseLocalLogs = wx.CheckBox(self.panelConfig, wx.ID_ANY, "")
        grid_sizer_1.Add(self.cbxUseLocalLogs, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)

        lblLocalLogLocation = wx.StaticText(self.panelConfig, wx.ID_ANY, "Local Log Path:")
        grid_sizer_1.Add(lblLocalLogLocation, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        self.txtLocalLogLocation = wx.TextCtrl(self.panelConfig, wx.ID_ANY, "")
        self.txtLocalLogLocation.SetMinSize((165, -1))
        grid_sizer_1.Add(self.txtLocalLogLocation, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)

        label_1 = wx.StaticText(self.panelConfig, wx.ID_ANY, "Use Remote Data Host:")
        grid_sizer_1.Add(label_1, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        self.cbxUseRmtDataHost = wx.CheckBox(self.panelConfig, wx.ID_ANY, "")
        grid_sizer_1.Add(self.cbxUseRmtDataHost, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)

        label_2 = wx.StaticText(self.panelConfig, wx.ID_ANY, "Remote Data Host Address:")
        grid_sizer_1.Add(label_2, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        self.txtRemoteHostAddr = wx.TextCtrl(self.panelConfig, wx.ID_ANY, "")
        self.txtRemoteHostAddr.SetMinSize((165, -1))
        grid_sizer_1.Add(self.txtRemoteHostAddr, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        label_5 = wx.StaticText(self.panelConfig, wx.ID_ANY, "I2C Sensor Bus #:")
        grid_sizer_1.Add(label_5, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.txtSensorBus = wx.TextCtrl(self.panelConfig, wx.ID_ANY, "")
        grid_sizer_1.Add(self.txtSensorBus, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        label_3 = wx.StaticText(self.panelConfig, wx.ID_ANY, "Local Magnetometer:")
        grid_sizer_1.Add(label_3, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        self.checkbox_1 = wx.CheckBox(self.panelConfig, wx.ID_ANY, "")
        grid_sizer_1.Add(self.checkbox_1, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        label_6 = wx.StaticText(self.panelConfig, wx.ID_ANY, "Local Mag Bus Address:")
        grid_sizer_1.Add(label_6, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        self.scSensor1Addr = wx.SpinCtrl(self.panelConfig, wx.ID_ANY, "0", min=0, max=100)
        grid_sizer_1.Add(self.scSensor1Addr, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        label_10 = wx.StaticText(self.panelConfig, wx.ID_ANY, "Local Temp Sensor: ")
        grid_sizer_1.Add(label_10, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        self.checkbox_3 = wx.CheckBox(self.panelConfig, wx.ID_ANY, "")
        grid_sizer_1.Add(self.checkbox_3, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        label_11 = wx.StaticText(self.panelConfig, wx.ID_ANY, "Local Temp Sensor Addr:")
        grid_sizer_1.Add(label_11, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        self.scLocalTempSensorAddr = wx.SpinCtrl(self.panelConfig, wx.ID_ANY, "0", min=0, max=100)
        grid_sizer_1.Add(self.scLocalTempSensorAddr, 0, wx.ALL, 2)

        grid_sizer_1.Add((0, 0), 0, 0, 0)

        label_4 = wx.StaticText(self.panelConfig, wx.ID_ANY, "Remote Magnetometer:")
        grid_sizer_1.Add(label_4, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        self.checkbox_2 = wx.CheckBox(self.panelConfig, wx.ID_ANY, "")
        grid_sizer_1.Add(self.checkbox_2, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        label_7 = wx.StaticText(self.panelConfig, wx.ID_ANY, "Remote Mag Bus Address:")
        grid_sizer_1.Add(label_7, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        self.scSensor2Addr = wx.SpinCtrl(self.panelConfig, wx.ID_ANY, "0", min=0, max=100)
        grid_sizer_1.Add(self.scSensor2Addr, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        grid_sizer_1.Add((0, 0), 0, 0, 0)

        label_12 = wx.StaticText(self.panelConfig, wx.ID_ANY, "Read Remote Temp:")
        grid_sizer_1.Add(label_12, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        self.cbUseRemoteTempSensor = wx.CheckBox(self.panelConfig, wx.ID_ANY, "")
        grid_sizer_1.Add(self.cbUseRemoteTempSensor, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        label_13 = wx.StaticText(self.panelConfig, wx.ID_ANY, "Remote Temp Sensor Addr:")
        grid_sizer_1.Add(label_13, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        self.scRemoteTempSensorAddr = wx.SpinCtrl(self.panelConfig, wx.ID_ANY, "0", min=0, max=100)
        grid_sizer_1.Add(self.scRemoteTempSensorAddr, 0, wx.ALL, 2)

        grid_sizer_1.Add((0, 0), 0, 0, 0)

        label_8 = wx.StaticText(self.panelConfig, wx.ID_ANY, "Sampling Mode:")
        grid_sizer_1.Add(label_8, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        self.cbSampleMode = wx.ComboBox(self.panelConfig, wx.ID_ANY, choices=["Polled Mode", "Continuous Mode"], style=wx.CB_DROPDOWN)
        self.cbSampleMode.SetSelection(0)
        grid_sizer_1.Add(self.cbSampleMode, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)

        label_9 = wx.StaticText(self.panelConfig, wx.ID_ANY, "Log File Format")
        grid_sizer_1.Add(label_9, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        self.cbLogFormat = wx.ComboBox(self.panelConfig, wx.ID_ANY, choices=["JSON", "CSV"], style=wx.CB_DROPDOWN)
        self.cbLogFormat.SetMinSize((165, -1))
        self.cbLogFormat.SetSelection(0)

        grid_sizer_1.Add(self.cbLogFormat, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((20, 20), 0, 0, 0)
        grid_sizer_1.Add((20, 20), 0, 0, 0)
        grid_sizer_1.Add((20, 20), 0, 0, 0)
        grid_sizer_1.Add((20, 20), 0, 0, 0)
        grid_sizer_1.Add((20, 20), 0, 0, 0)

        grid_sizer_1.AddGrowableRow(0)
        grid_sizer_1.AddGrowableRow(1)
        grid_sizer_1.AddGrowableRow(2)
        grid_sizer_1.AddGrowableRow(3)
        grid_sizer_1.AddGrowableRow(4)
        grid_sizer_1.AddGrowableRow(6)
        grid_sizer_1.AddGrowableRow(8)
        grid_sizer_1.AddGrowableCol(0)
        grid_sizer_1.AddGrowableCol(1)
        grid_sizer_1.AddGrowableCol(2)
        grid_sizer_1.AddGrowableCol(3)
        grid_sizer_1.AddGrowableCol(4)
        self.panelConfig.SetSizer(grid_sizer_1)
#        self.topRightConfigPane.SetSizer(sizer_5)
