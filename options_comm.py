__author__ = 'Puleo'

import wx
import serial
import serial.tools.list_ports

SHOW_BAUDRATE = 1 << 0
SHOW_FORMAT = 1 << 1
SHOW_FLOW = 1 << 2
SHOW_TIMEOUT = 1 << 3
SHOW_RESULT = 1 << 4

SHOW_ALL = SHOW_BAUDRATE | SHOW_FORMAT | SHOW_FLOW | SHOW_TIMEOUT | SHOW_RESULT

class Connection(wx.Panel):

    def __init__(self, parent, serial, thread):
        self.show = SHOW_ALL
        wx.Panel.__init__(self, parent = parent)

        self.serial = serial
        self.thread = thread
        self.serial.timeout = 0.5   # make sure that the alive event can be checked from time to time

        self.label_2 = wx.StaticText(self, -1, "Port")
        self.choice_port = wx.Choice(self, -1, choices=[])
        self.label_1 = wx.StaticText(self, -1, "Baudrate")
        self.combo_box_baudrate = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN)
        self.sizer_1_staticbox = wx.StaticBox(self, -1, "Basics")

        self.panel_format = wx.Panel(self, -1)
        self.label_3 = wx.StaticText(self.panel_format, -1, "Data Bits")
        self.choice_databits = wx.Choice(self.panel_format, -1, choices=["choice 1"])
        self.label_4 = wx.StaticText(self.panel_format, -1, "Stop Bits")
        self.choice_stopbits = wx.Choice(self.panel_format, -1, choices=["choice 1"])
        self.label_5 = wx.StaticText(self.panel_format, -1, "Parity")
        self.choice_parity = wx.Choice(self.panel_format, -1, choices=["choice 1"])
        self.sizer_format_staticbox = wx.StaticBox(self.panel_format, -1, "Data Format")

        self.panel_timeout = wx.Panel(self, -1)
        self.checkbox_timeout = wx.CheckBox(self.panel_timeout, -1, "Use Timeout")
        self.text_ctrl_timeout = wx.TextCtrl(self.panel_timeout, -1, "")
        self.label_6 = wx.StaticText(self.panel_timeout, -1, "seconds")
        self.sizer_timeout_staticbox = wx.StaticBox(self.panel_timeout, -1, "Timeout")

        self.panel_flow = wx.Panel(self, -1)
        self.checkbox_rtscts = wx.CheckBox(self.panel_flow, -1, "RTS/CTS")
        self.checkbox_xonxoff = wx.CheckBox(self.panel_flow, -1, "Xon/Xoff")
        self.sizer_flow_staticbox = wx.StaticBox(self.panel_flow, -1, "Flow Control")

        self.button_ok = wx.Button(self, wx.ID_OK, "")
        self.button_cancel = wx.Button(self, wx.ID_CANCEL, "")
        self.button_find = wx.Button(self, wx.ID_FIND, "")

        self.button_cancel.Disable()

        self.panel_results = wx.Panel(self, -1)
        self.label_res0 = wx.StaticText(self.panel_results, -1, "Tick Counter:")
        self.res0_val = wx.StaticText(self.panel_results, -1, "Osjghfjghfég")
        self.label_res1 = wx.StaticText(self.panel_results, -1, "Current Task:")
        self.res1_val = wx.StaticText(self.panel_results, -1, "Osjghfjghfég")
        self.label_res2 = wx.StaticText(self.panel_results, -1, "OSVersion Nr:")
        self.res2_val = wx.StaticText(self.panel_results, -1, "Osjghfjghfég")
        self.label_res3 = wx.StaticText(self.panel_results, -1, "Proc Name:")
        self.res3_val = wx.StaticText(self.panel_results, -1, "Osjghfjghfég")
        self.sizer_results_staticbox = wx.StaticBox(self.panel_results, -1, "Communication Result ")

        self.__set_properties()
        self.__do_layout()

        # attach the event handlers
        self.__attach_events()

    def __set_properties(self):
        # begin wxGlade: SerialConfigDialog.__set_properties

        self.choice_databits.SetSelection(0)
        self.choice_stopbits.SetSelection(0)
        self.choice_parity.SetSelection(0)
        self.text_ctrl_timeout.Enable(False)
        self.button_ok.SetDefault()

        if not self.show & SHOW_BAUDRATE:
            self.label_1.Hide()
            self.combo_box_baudrate.Hide()
        if not self.show & SHOW_FORMAT:
            self.panel_format.Hide()
        if not self.show & SHOW_TIMEOUT:
            self.panel_timeout.Hide()
        if not self.show & SHOW_FLOW:
            self.panel_flow.Hide()
        if not self.show & SHOW_RESULT:
            self.panel_results.Hide()


        # fill in ports and select current setting
        preferred_index = 0
        self.choice_port.Clear()
        self.ports = []
        for n, (portname, desc, hwid) in enumerate(sorted(serial.tools.list_ports.comports())):
            self.choice_port.Append(u'{} - {}'.format(portname, desc))
            self.ports.append(portname)
            if self.serial.name == portname:
                preferred_index = n
        self.choice_port.SetSelection(preferred_index)

        if self.show & SHOW_BAUDRATE:
            preferred_index = None
            # fill in baud rates and select current setting
            self.combo_box_baudrate.Clear()
            for n, baudrate in enumerate(self.serial.BAUDRATES):
                self.combo_box_baudrate.Append(str(baudrate))
                if self.serial.baudrate == baudrate:
                    preferred_index = n
            if preferred_index is not None:
                self.combo_box_baudrate.SetSelection(preferred_index)
            else:
                self.combo_box_baudrate.SetValue(u'{}'.format(self.serial.baudrate))

        if self.show & SHOW_FORMAT:
            # fill in data bits and select current setting
            self.choice_databits.Clear()
            for n, bytesize in enumerate(self.serial.BYTESIZES):
                self.choice_databits.Append(str(bytesize))
                if self.serial.bytesize == bytesize:
                    index = n
            self.choice_databits.SetSelection(index)
            # fill in stop bits and select current setting
            self.choice_stopbits.Clear()
            for n, stopbits in enumerate(self.serial.STOPBITS):
                self.choice_stopbits.Append(str(stopbits))
                if self.serial.stopbits == stopbits:
                    index = n
            self.choice_stopbits.SetSelection(index)
            # fill in parities and select current setting
            self.choice_parity.Clear()
            for n, parity in enumerate(self.serial.PARITIES):
                self.choice_parity.Append(str(serial.PARITY_NAMES[parity]))
                if self.serial.parity == parity:
                    index = n
            self.choice_parity.SetSelection(index)

        if self.show & SHOW_TIMEOUT:
            # set the timeout mode and value
            if self.serial.timeout is None:
                self.checkbox_timeout.SetValue(False)
                self.text_ctrl_timeout.Enable(False)
            else:
                self.checkbox_timeout.SetValue(True)
                self.text_ctrl_timeout.Enable(True)
                self.text_ctrl_timeout.SetValue(str(self.serial.timeout))

        if self.show & SHOW_FLOW:
            # set the rtscts mode
            self.checkbox_rtscts.SetValue(self.serial.rtscts)
            # set the rtscts mode
            self.checkbox_xonxoff.SetValue(self.serial.xonxoff)

        if self.show & SHOW_RESULT:
            self.res0_val.SetLabel("")
            self.res1_val.SetLabel("")
            self.res2_val.SetLabel("")
            self.res3_val.SetLabel("")


        # end wxGlade

    def __do_layout(self):
        # begin wxGlade:

        self.sizer_flow_staticbox.Lower()
        sizer_flow = wx.StaticBoxSizer(self.sizer_flow_staticbox, wx.HORIZONTAL)

        self.sizer_timeout_staticbox.Lower()
        sizer_timeout = wx.StaticBoxSizer(self.sizer_timeout_staticbox, wx.HORIZONTAL)

        self.sizer_1_staticbox.Lower()
        sizer_1 = wx.StaticBoxSizer(self.sizer_1_staticbox, wx.VERTICAL)

        self.sizer_results_staticbox.Lower()
        sizer_results = wx.StaticBoxSizer(self.sizer_results_staticbox, wx.HORIZONTAL)

        self.sizer_format_staticbox.Lower()
        sizer_format = wx.StaticBoxSizer(self.sizer_format_staticbox, wx.VERTICAL)

        grid_sizer_1 = wx.FlexGridSizer(4, 2, 0, 0)
        result_sizer_1 = wx.FlexGridSizer(6, 2, 5, 25)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)

        sizer_basics = wx.FlexGridSizer(3, 2, 0, 0)
        sizer_basics.AddSpacer(10)
        sizer_basics.AddSpacer(10)
        sizer_basics.Add(self.label_2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        sizer_basics.Add(self.choice_port, 0, wx.EXPAND, 0)
        sizer_basics.Add(self.label_1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        sizer_basics.Add(self.combo_box_baudrate, 0, wx.EXPAND, 0)
        sizer_basics.AddGrowableCol(1)
        sizer_1.Add(sizer_basics, 0, wx.EXPAND, 0)
        sizer_2.Add(sizer_1, 0, wx.EXPAND, 0)

        grid_sizer_1.AddSpacer(10)
        grid_sizer_1.AddSpacer(10)
        grid_sizer_1.Add(self.label_3, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        grid_sizer_1.Add(self.choice_databits, 1, wx.EXPAND | wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.label_4, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        grid_sizer_1.Add(self.choice_stopbits, 1, wx.EXPAND | wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.label_5, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        grid_sizer_1.Add(self.choice_parity, 1, wx.EXPAND | wx.ALIGN_RIGHT, 0)

        sizer_format.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        self.panel_format.SetSizer(sizer_format)
        sizer_2.Add(self.panel_format, 0, wx.EXPAND, 0)

        sizer_timeout.AddSpacer(10)
        sizer_timeout.Add(self.checkbox_timeout, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        sizer_timeout.Add(self.text_ctrl_timeout, 0, 0, 0)
        sizer_timeout.Add(self.label_6, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)

        self.panel_timeout.SetSizer(sizer_timeout)
        sizer_2.Add(self.panel_timeout, 0, wx.EXPAND, 0)

        sizer_flow.AddSpacer(10)
        sizer_flow.Add(self.checkbox_rtscts, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        sizer_flow.Add(self.checkbox_xonxoff, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        sizer_flow.Add((10, 10), 1, wx.EXPAND, 0)
        self.panel_flow.SetSizer(sizer_flow)
        sizer_2.Add(self.panel_flow, 0, wx.EXPAND, 0)

        sizer_3.Add(self.button_ok, 0, 0, 0)
        sizer_3.Add(self.button_cancel, 0, 0, 0)
        sizer_3.Add(self.button_find, 0, 0, 0)
        sizer_2.Add(sizer_3, 0, wx.ALL | wx.ALIGN_RIGHT, 4)


        result_sizer_1.AddSpacer(10)
        result_sizer_1.AddSpacer(10)
        result_sizer_1.AddSpacer(10)
        result_sizer_1.AddSpacer(10)
        result_sizer_1.Add(self.label_res0, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        result_sizer_1.Add(self.res0_val,  1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        result_sizer_1.Add(self.label_res1, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        result_sizer_1.Add(self.res1_val,  1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        result_sizer_1.Add(self.label_res2, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        result_sizer_1.Add(self.res2_val,  1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        result_sizer_1.Add(self.label_res3, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        result_sizer_1.Add(self.res3_val,  1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)

        sizer_results.Add(result_sizer_1, 1, wx.EXPAND, 0)
        self.panel_results.SetSizer(sizer_results)
        sizer_2.Add(self.panel_results, 1, wx.EXPAND, 0)


        self.panel_results.Hide()

        self.SetAutoLayout(True)
        self.SetSizer(sizer_2)
        sizer_2.Fit(self)
        self.Layout()

        # end wxGlade

    def __attach_events(self):
        self.Bind(wx.EVT_BUTTON, self.OnOK, id=self.button_ok.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=self.button_cancel.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnFind, id=self.button_find.GetId())
        if self.show & SHOW_TIMEOUT:
            self.Bind(wx.EVT_CHECKBOX, self.OnTimeout, id=self.checkbox_timeout.GetId())

    def OnOK(self, events):
        success = True
        self.serial.port = self.ports[self.choice_port.GetSelection()]
        if self.show & SHOW_BAUDRATE:
            try:
                b = int(self.combo_box_baudrate.GetValue())
            except ValueError:
                with wx.MessageDialog(
                        self,
                        'Baudrate must be a numeric value',
                        'Value Error',
                        wx.OK | wx.ICON_ERROR) as dlg:
                    dlg.ShowModal()
                success = False
            else:
                self.serial.baudrate = b
        if self.show & SHOW_FORMAT:
            self.serial.bytesize = self.serial.BYTESIZES[self.choice_databits.GetSelection()]
            self.serial.stopbits = self.serial.STOPBITS[self.choice_stopbits.GetSelection()]
            self.serial.parity = self.serial.PARITIES[self.choice_parity.GetSelection()]
        if self.show & SHOW_FLOW:
            self.serial.rtscts = self.checkbox_rtscts.GetValue()
            self.serial.xonxoff = self.checkbox_xonxoff.GetValue()
        if self.show & SHOW_TIMEOUT:
            if self.checkbox_timeout.GetValue():
                try:
                    self.serial.timeout = float(self.text_ctrl_timeout.GetValue())
                except ValueError:
                    with wx.MessageDialog(
                            self,
                            'Timeout must be a numeric value',
                            'Value Error',
                            wx.OK | wx.ICON_ERROR) as dlg:
                        dlg.ShowModal()
                    success = False
            else:
                self.serial.timeout = None
        if success:
            self.OnPortSettings(events)

    def OnCancel(self, events):
        self.thread.stop()               # stop reader thread
        self.serial.close()             # cleanup

        self.button_cancel.Disable()
        self.button_find.Enable()
        self.button_ok.Enable()
        self.GetParent().GetParent().GetParent().disableOpPanelBtn()

        self.panel_results.Hide()

    def OnFind(self, events):
        preferred_index = 0
        self.choice_port.Clear()
        self.ports = []
        for n, (portname, desc, hwid) in enumerate(sorted(serial.tools.list_ports.comports())):
            self.choice_port.Append(u'{} - {}'.format(portname, desc))
            self.ports.append(portname)
            if self.serial.name == portname:
                preferred_index = n
        self.choice_port.SetSelection(preferred_index)

    def OnTimeout(self, events):
        if self.checkbox_timeout.GetValue():
            self.text_ctrl_timeout.Enable(True)
        else:
            self.text_ctrl_timeout.Enable(False)

        events.Skip()


    def OnPortSettings(self, event):

        wx.BeginBusyCursor()

        lab_val = self.thread.dispath(event, 's')

        self.res0_val.SetLabel(lab_val[0])
        self.res1_val.SetLabel(lab_val[1])
        self.res2_val.SetLabel(lab_val[2])
        self.res3_val.SetLabel(lab_val[3])

        self.button_cancel.Enable()
        self.button_find.Disable()
        self.button_ok.Disable()
        self.GetParent().GetParent().GetParent().enableOpPanelBtn()

        self.panel_results.Show()
        self.Layout()

        wx.EndBusyCursor()
