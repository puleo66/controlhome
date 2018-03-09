__author__ = 'Puleo'


import wx
import configparser
import codecs

import watching_door_gui
import setup_dialog_gui as setup

doors = {}

class HeaterPanelDoors(wx.Panel):

    def __init__(self, parent):

        self.parent = parent

        wx.Panel.__init__(self, self.parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.paint = HeaterPaintDoors(self)

        sizer.Add(self.paint, 1, wx.EXPAND | wx.ALL, 2)

        self.SetSizer(sizer)



class HeaterPaintDoors(wx.Window):

    def __init__(self, parent):

        wx.Window.__init__(self, parent)

        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(wx.BLACK)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouse)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)

        self.door0 = watching_door_gui.WatchingDoor(self, 0)
        self.door1 = watching_door_gui.WatchingDoor(self, 1)
        self.door2 = watching_door_gui.WatchingDoor(self, 2)

        self.configDoor = configparser.ConfigParser()
        # Open the file with the correct encoding
        with codecs.open('/home/pi/controlhome/config_door.ini', 'r', encoding='utf-8') as f:
            self.configDoor.read_file(f)

        self.LoadConfig()

    def OnPaint(self, evt):
        #dc = wx.PaintDC(self)
        dc = wx.AutoBufferedPaintDC(self)
        self.door0.Draw(dc)
        self.door1.Draw(dc)
        self.door2.Draw(dc)
        evt.Skip()

    def OnMouse(self, evt):

        modul, methodName = self.GetDoor(evt.GetX(), evt.GetY())

        setupDlg = setup.SetupDlg(None, -1, methodName + " Setup", False, modul, self.configDoor)
        if setupDlg.ShowModal() == wx.ID_OK:

            cfgfile = open('/home/pi/controlhome/config_door.ini','w')
            self.configDoor.write(cfgfile)
            cfgfile.close()

            self.Refresh()
        setupDlg.Destroy()
        evt.Skip()

    def OnMouseMotion(self, evt):
        modul, methodName = self.GetDoor(evt.GetX(), evt.GetY())
        sbNew = self.GetParent().GetParent().GetParent().GetParent().GetParent().sb
        if modul != None:
            if modul.visibl:
                sbNew.SetForegroundColour(wx.RED)
                sbNew.SetStatusText("Code: " + modul.addr.replace(".0", "-") + " " + modul.descript)

        else:
            sbNew.SetStatusText("")

        evt.Skip()

    def GetDoor(self, x=0, y=0, j=None):

        mod = None

        if j == None:
            for i in range(0, len(doors)):

                if (doors[i]['y'] < y < doors[i]['y']+100):
                    mod = True
                    break
        else:
            mod = True
            i = j

        if mod:
            methodName = 'door' + str(i)

            return getattr(self, methodName), methodName
        else:
            return None, ""


    def CheckDoor(self, val):

        for i in range(0, len(doors)):
            mod, methodName = self.GetDoor(0,0,i)
            if mod != None:
                if mod.visibl:
                    txt0 = mod.addr.replace(".0", " ")
                    if val.find(txt0) != -1:
                        txt1 = val[val.find(txt0) + len(txt0):]
                        tmp_open = mod.open
                        if (int(txt1) == 82) | (int(txt1) == 2):
                            mod.open = False
                        else:
                            mod.open = True
                        if tmp_open != mod.open:
                            self.Refresh()
                        break

    def LoadConfig(self):

        for methodName in self.configDoor.sections():
            obj = getattr(self, methodName)
            for name, value in self.configDoor.items(methodName):
                if name == "addr":
                    obj.addr = value
                if name == "descript":
                    obj.descript = value
                if name == "visibl":
                    if value == "True":
                        obj.visibl = True
                    else:
                        obj.visibl = False