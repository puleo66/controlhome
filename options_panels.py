#!/usr/bin/env python
__author__ = 'Puleo'

import wx

class CntrPnl(wx.Panel):

    def __init__(self, parent, pnlComm, pnlSys):
        self.parent = parent
        self.panel_comm = pnlComm
        self.panel_system = pnlSys

        # wx.SIMPLE_BORDER wx.RAISED_BORDER wx.SUNKEN_BORDER wx.NO_BORDER
        wx.Panel.__init__(self, parent, pos=(6, 6), size=(150, 500), style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour(self.parent.GetBackgroundColour())

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel_comm, 1, wx.EXPAND)
        self.sizer.Add(self.panel_system, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.SetAutoLayout(True)
        self.Layout()

        self.Fit()
        self.Show()
