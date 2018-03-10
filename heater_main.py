__author__ = 'Puleo'


import wx
import configparser
import codecs

import setup_dialog_gui as setup
import watching_pipe_ai
import watching_radiator_gui
import watching_heater_gui
import watching_tank_gui
import get_temp

radiators = {}

class HeaterPanel(wx.Panel):

    def __init__(self, parent):

        self.parent = parent

        wx.Panel.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.paint = HeaterPaint(self)

        sizer.Add(self.paint, 1, wx.EXPAND | wx.ALL, 2)

        self.SetSizer(sizer)



class HeaterPaint(wx.Window):

    def __init__(self, parent):
        self.parent = parent

        wx.Window.__init__(self, self.parent)

        # Self Test !!!
        self.val0 = {0: 'x14203', 1: 'xA201', 2: 'x1E202', 3: 'x1E201', 4: 'x14202', 5: 'x14201', 6: 'x002000'}
        self.val1 = {0: 'xB62000', 1: 'x322000', 2: 'xB62000', 3: 'xB62000', 4: 'xB62000', 5: 'xB6208', 6: 'x002000'}

        self.dialogs = [ 0, 0, 0, 0, 0, 0, 0 ]


        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(wx.BLACK)

        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouse)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseRight)    # Only Test !!!!
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)

        self.rad0 = watching_radiator_gui.WatchingRadiator(self, 300, 10, 0, True)
        self.rad1 = watching_radiator_gui.WatchingRadiator(self, 400, 10, 1, True)

        self.rad2 = watching_radiator_gui.WatchingRadiator(self, 300, 170, 2, True)
        self.rad3 = watching_radiator_gui.WatchingRadiator(self, 400, 170, 3, True)
        self.rad4 = watching_radiator_gui.WatchingRadiator(self, 500, 170, 4, True)

        self.rad5 = watching_radiator_gui.WatchingRadiator(self, 300, 340, 5, True)
        self.rad6 = watching_radiator_gui.WatchingRadiator(self, 100, 10, 6, False)


        self.pipes = watching_pipe_ai.WatchingPipeAi(self)

        self.heater = watching_heater_gui.WatchingHeater(self, 65, 240)

        self.tank = watching_tank_gui.WatchingTank(self, 85, 530)

        self.configRad = configparser.ConfigParser()
        # Open the file with the correct encoding
        with codecs.open('/home/pi/controlhome/config_rad.ini', 'r', encoding='utf-8') as f:
            self.configRad.read_file(f)

        self.LoadConfig()

    def onPaint(self, evt):

        dc = wx.AutoBufferedPaintDC(self)

        self.rad0.Draw(dc)
        self.rad1.Draw(dc)
        self.rad2.Draw(dc)
        self.rad3.Draw(dc)
        self.rad4.Draw(dc)
        self.rad5.Draw(dc)
        self.rad6.Draw(dc)

        self.heater.InstallHeater(dc)

        self.tank.InstallTank(dc)

        self.pipes.DispatchDrawPipes(dc, self.dialogs)

        evt.Skip()

    def OnMouse(self, evt):
        modul, methodName = self.GetRadiator(evt.GetX(), evt.GetY())

        setupDlg = setup.SetupDlg(None, -1, methodName + " Setup", True, modul, self.configRad)
        if setupDlg.ShowModal() == wx.ID_OK:

            cfgfile = open('/home/pi/controlhome/config_rad.ini','w')
            self.configRad.write(cfgfile)
            cfgfile.close()

            if modul.visibl:
                self.dialogs[int(methodName.replace("rad", ""))] = 1
            else:
                self.dialogs[int(methodName.replace("rad", ""))] = 0

            self.Refresh()
        setupDlg.Destroy()

        evt.Skip()


    # Only Test !!!!!
    def OnMouseRight(self, evt):
        modul, methodName = self.GetRadiator(evt.GetX(), evt.GetY())

        modulAddr = modul.addr.replace(".0", "")
        addrLo = modulAddr[3:]
        addrHi = hex(int(modulAddr[:2])).upper()[2:]

        addr = "x" + addrHi + "20" + addrLo

        for i in range(len(self.val0)):
            if self.val0[i] == addr:
                tmpNr = i
                break


        tmpVal = self.val1[tmpNr]
        tmpLen = len(tmpVal)
        tmp = tmpVal[:tmpLen-2]
        tmp1 = tmpVal[tmpLen-2:]

        if tmp1 == "00":
            tmp1 = "FF"
        else:
            tmp1 = "00"

        tmpVal = tmp + tmp1
        self.val1[tmpNr] = tmpVal

        self.CheckRadiator(self.val0, self.val1)


        self.pipes.pipeDrawEnd = True
        self.pipes.dialogLoad = True

        self.Refresh()


        evt.Skip()

    def OnMouseMotion(self, evt):
        modul, methodName = self.GetRadiator(evt.GetX(), evt.GetY())
        sbNew = self.GetParent().GetParent().GetParent().GetParent().sb
        if modul != None:
            if modul.visibl:
                sbNew.SetStatusText(modul.descript, 1)
        else:
            sbNew.SetStatusText("", 1)

        evt.Skip()

    def GetRadiator(self, x=0 , y=0, j=None):

        mod = None

        if j == None:
            for i in range(0, len(radiators)):

                if (radiators[i]['x'] <= x <= radiators[i]['x']+80)&(radiators[i]['y'] <= y <= radiators[i]['y']+80):
                    mod = True
                    break
        else:
            mod = True
            i = j

        if mod:
            methodName = 'rad' + str(i)

            return getattr(self, methodName), methodName
        else:
            return None, ""


    def radiatorConv(self, val0, val1):
        addr = {}
        cmd = {}
        val = {}

        for i in val0:

            val_tmp = self.convDecF(val0[i])

            addr[i] = val_tmp[:2] + val_tmp[len(val_tmp)-2:]
            cmd[i] = val1[i][:3]
            val[i] = val1[i][len(val1[i])-2:]

        return addr, cmd, val

    def convDecF(self, val):
        str_tmp = ''
        tmp = {}

        t = val[1:]
        t_inx = t.find('20')

        if t_inx < 2:
            tmp[0] = '0x' + t[t_inx-1]
        else:
            tmp[0] = '0x' + t[t_inx-2] + t[t_inx-1]

        tmp[1] = '0x' + t[t_inx+2:]

        for i in tmp:
            if int(tmp[i], 16) > 0x09:
                str_tmp += str(int(tmp[i], 16))
            else:
                str_tmp += '0' + str(int(tmp[i], 16))

        str_tmp = str_tmp[:2] + '   ' + str_tmp[2:]

        return  str_tmp



    def CheckRadiator(self, val0, val1):

        addr, cmd, val2 = self.radiatorConv(val0, val1)

        for i in range(0, len(radiators)):
            mod, methodName = self.GetRadiator(0,0,i)
            if mod != None:
                if mod.visibl:
                    obj_addr = mod.addr.replace(".0", "")

                    for i in addr:
                        if addr[i] == obj_addr:
                            n = i
                            break
                        else:
                            n = -1

                    if n != -1:
                        if str(cmd[n]) + str(val2[n]) != "x6764":      # FHT80b communication !
                            tmpVal = int(val2[n],16)
                            if tmpVal > 3:                    # x03 * 100 / 255 != 00 !!!!
                                if tmpVal == 255:
                                    mod.th_mass = str(((tmpVal*100)/255)-1)[:2]
                                else:
                                    mod.th_mass = str(((tmpVal*100)/255))[:2]

                                if mod.th_mass.find(".") != -1:
                                    mod.th_mass = "0" + mod.th_mass[:1]

                                self.dialogs[int(methodName.replace("rad", ""))] = 2

                            else:
                                mod.th_mass = "00"
                                self.dialogs[int(methodName.replace("rad", ""))] = 1

        heaterONOFF = 0
        for nr in range(len(self.dialogs)):
            if self.dialogs[nr] > 1:
                heaterONOFF = 1

        if heaterONOFF > 0:
            self.heater.onOff = True
        else:
            self.heater.onOff = False

    def TankHeaterData(self, termoObject):

        if termoObject.TermoEnable:
            valTemp = termoObject.valTemp

            x = get_temp.DS1820()
            data, addr, count = x.loadDataTemp()

            #
            # Check 85 grad !!!!!!!!!!!
            #

            for row in valTemp:
                if valTemp[row] == "Flow Hot Water":
                    self.heater.Flow_Hot_Water = str(data[0])[:4]
                if valTemp[row] == "Return Cold Water":
                    self.heater.Return_Cold_Water = str(data[2])[:4]
                if valTemp[row] == "Hot Water Top":
                    self.tank.Hot_Water_Top = str(data[1])[:4]
                if valTemp[row] == "Hot Water Bottom":
                    self.tank.Hot_Water_Bottom = str(data[3])[:4]


    def HeaterMain(self,termoObject, val0, val1):

        self.CheckRadiator(val0, val1)
        self.TankHeaterData(termoObject)

        self.pipes.pipeDrawEnd = True
        self.pipes.dialogLoad = True

        self.Refresh()

    def LoadConfig(self):

        for methodName in self.configRad.sections():
            obj = getattr(self, methodName)
            for name, value in self.configRad.items(methodName):
                if name == "addr":
                    obj.addr = value
                if name == "descript":
                    obj.descript = value
                if name == "visibl":
                    if value == "True":
                        obj.visibl = True
                    else:
                        obj.visibl = False
