__author__ = 'Puleo'

import wx

SHOW_LOG = 1 << 0

SHOW_ALL = SHOW_LOG

class HeaterLogPanel(wx.Panel):

    def __init__(self, parent):

        self.show = SHOW_ALL

        wx.Panel.__init__(self, parent = parent)

        #self.logList = wx.ListBox(self, -1, choices = [], size= (160,5), style = wx.LB_SINGLE)  // PC
        self.logList = wx.ListBox(self, -1, choices = [], size= (220,5), style = wx.LB_SINGLE)
        self.logList.SetBackgroundColour(wx.LIGHT_GREY)
        self.sizer_log_staticbox = wx.StaticBox(self, -1, "FHT and TF Log")

        self.__set_properties()
        self.__do_layout()


    def __set_properties(self):
        if self.show & SHOW_LOG:
            self.logList.Clear()


    def __do_layout(self):

        self.sizer_log_staticbox.Lower()
        sizer_log = wx.StaticBoxSizer(self.sizer_log_staticbox, wx.VERTICAL)

        sizer_win = wx.BoxSizer(wx.VERTICAL)
        gbs = wx.GridBagSizer(0,0)

        #gbs.Add(self.logList, (0,0), span=(9,1), flag=wx.EXPAND)    // PC
        gbs.Add(self.logList, (0,0), span=(21,1), flag=wx.EXPAND)

        sizer_log.Add(gbs, 0, flag=wx.ALL, border=5)
        sizer_win.Add(sizer_log, 0, wx.EXPAND, 0)

        self.SetAutoLayout(True)
        self.SetSizer(sizer_win)
        sizer_win.Fit(self)
        self.Layout()

    def load(self, msg):
        #if self.logList.Count >= 10:  // PC
        if self.logList.Count >= 17:
            self.logList.Delete(0)

        self.logList.Append(msg)




