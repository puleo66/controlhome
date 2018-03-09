__author__ = 'Puleo'

import wx
import wx.lib.agw.floatspin as agw

class SetupDlg(wx.Dialog):

    def __init__(self, parent, id, title, type, modul, configparser):

        self.parent = parent
        self.visible = modul.visibl
        self.desc = modul.descript
        self.addr = modul.addr
        self.title = title
        self.type = type
        self.modul = modul
        self.configparser = configparser

        wx.Dialog.__init__(self, parent, id, title, size=(320, 200))


        panel = wx.Panel(self, -1)

        self.lb_addr = wx.StaticText(panel, -1, "Address:", (20,20))
        self.sp_h0 = agw.FloatSpin(panel, -1, pos=(100, 15), size=(60, -1), min_val=0, max_val=999, agwStyle=agw.FS_RIGHT, increment=1, digits=0)
        self.sp_h1 = agw.FloatSpin(panel, -1, pos=(170, 15), size=(60, -1), min_val=0, max_val=999, agwStyle=agw.FS_RIGHT, increment=1, digits=0)
        self.sp_h2 = agw.FloatSpin(panel, -1, pos=(240, 15), size=(60, -1), min_val=0, max_val=999, agwStyle=agw.FS_RIGHT, increment=1, digits=0)
        self.lb_desc = wx.StaticText(panel, -1, "Description:", (20,70))
        self.tx_desc = wx.TextCtrl(panel, -1,  pos=(100, 70), size=(200,20))

        self.bt_ok = wx.Button(panel, wx.ID_OK, "", pos=(100, 130))
        self.bt_cancel = wx.Button(panel, wx.ID_CANCEL, "", pos=(190, 130))
        self.cb_visibl = wx.CheckBox(panel, -1, "Visible:", pos=(20, 130))


        self.__set_properties()
        self.__attach_events()

        self.Centre()

    def __set_properties(self):
        self.cb_visibl.SetValue(self.visible)
        self.tx_desc.SetValue(self.desc)

        if not self.visible:

            self.sp_h0.Disable()
            self.sp_h1.Disable()

            if self.type:
                self.sp_h2.Hide()
            else:
                self.sp_h2.Disable()
            self.tx_desc.Disable()
        else:
            if self.type:
                self.sp_h2.Hide()

        addr = self.addr

        self.sp_h0.SetValue(int(addr[:addr.find('.0')]))
        addr = addr[addr.find('.0')+2:]
        self.sp_h1.SetValue(int(addr[:addr.find('.0')]))
        if not self.type:
            addr = addr[addr.find('.0')+2:]
            self.sp_h2.SetValue(int(addr[:addr.find('.0')]))

    def __attach_events(self):
        self.Bind(wx.EVT_BUTTON, self.OnOK, id=self.bt_ok.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=self.bt_cancel.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.OnVisible, id=self.cb_visibl.GetId())

    def OnOK(self, evt):
        self.modul.visibl = self.cb_visibl.Value
        self.modul.descript = self.tx_desc.GetValue()

        self.modul.addr = str(self.sp_h0.GetValue())
        if len(str(self.sp_h1.GetValue())) == 3:
            self.modul.addr += '0' + str(self.sp_h1.GetValue())

        if not self.type:
            self.modul.addr = str(self.sp_h0.GetValue())+ str(self.sp_h1.GetValue())
            self.modul.addr += str(self.sp_h2.GetValue())

        # Modify Config file !!!!
        title = self.title.replace(" Setup", "")
        self.configparser.set(title, 'addr', self.modul.addr)
        self.configparser.set(title, 'descript', self.tx_desc.GetValue())
        if self.cb_visibl.Value:
            self.configparser.set(title, 'visibl', 'True')
        else:
            self.configparser.set(title, 'visibl', 'False')

        evt.Skip()

    def OnCancel(self, evt):
        self.Close(True)
        evt.Skip()


    def OnVisible(self,evt):
        if self.cb_visibl.GetValue():

            self.sp_h0.Enable()
            self.sp_h1.Enable()


            if self.type:
                self.sp_h2.Hide()
            else:
                self.sp_h2.Enable()
            self.tx_desc.Enable()
        else:
            self.sp_h0.Disable()
            self.sp_h1.Disable()

            if self.type:
                self.sp_h2.Hide()
            else:
                self.sp_h2.Disable()
            self.tx_desc.Disable()

        evt.Skip()

