#!/usr/bin/env python
__author__ = 'Puleo'

import wx

class CntrBtnPnl(wx.Panel):
    """
    Contains the buttons and the label of the window
    """

    def __init__(self, parent):
       self.parent = parent

       wx.Panel.__init__(self, parent, pos=(6, 6), size=(150, 500))
       self.SetBackgroundColour(self.parent.GetBackgroundColour())

       self.btnCom= wx.Button(self, label="Connection", size=(70, 28))
       self.btnSys= wx.Button(self, label="Diagnostics", size=(70, 28))
       self.btnFht= wx.Button(self, label="FHT80", size=(70, 28))
       self.btnTemp= wx.Button(self, label="Temperature", size=(70, 28))
       self.btnOut= wx.Button(self, label="Logout", size=(70, 28))

       self.btnSys.Disable()
       self.btnFht.Disable()

       self.parent.Bind(wx.EVT_BUTTON, self.OnComm, self.btnCom)
       self.parent.Bind(wx.EVT_BUTTON, self.OnSys, self.btnSys)
       self.parent.Bind(wx.EVT_BUTTON, self.OnFht, self.btnFht)
       self.parent.Bind(wx.EVT_BUTTON, self.OnTemp, self.btnTemp)
       self.parent.Bind(wx.EVT_BUTTON, self.OnOut, self.btnOut)

       #making a sizer
       box = wx.BoxSizer(wx.VERTICAL)

       box.Add(self.btnCom, 0, wx.EXPAND | wx.ALL)
       box.Add(self.btnSys, 0, wx.EXPAND | wx.ALL)
       box.Add(self.btnFht, 0, wx.EXPAND | wx.ALL)
       box.Add(self.btnTemp, 0, wx.EXPAND | wx.ALL)
       box.Add(self.btnOut, 0, wx.EXPAND | wx.ALL)

       self.SetAutoLayout(True)
       self.SetSizer(box)
       self.Layout()

       self.Fit()
       self.Show()

    # Functions
    def OnComm(self, evt):
        self.GetParent().GetParent().GetParent().optionPnlChange(0)
        evt.Skip()

    def OnSys(self, evt):
        self.GetParent().GetParent().GetParent().optionPnlChange(1)
        evt.Skip()

    def OnFht(self, evt):
        self.GetParent().GetParent().GetParent().optionPnlChange(2)
        evt.Skip()

    def OnTemp(self, evt):
        self.GetParent().GetParent().GetParent().optionPnlChange(3)
        evt.Skip()

    def OnOut(self, evt):
        self.GetParent().GetParent().GetParent().OnClose(evt)
        evt.Skip()