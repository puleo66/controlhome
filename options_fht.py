__author__ = 'Puleo'

import wx
import wx.grid

SHOW_DEFAULT = 1 << 0
SHOW_REALTIME  = 1 << 1
SHOW_BUTTON  = 1 << 2

SHOW_ALL = SHOW_DEFAULT | SHOW_REALTIME | SHOW_BUTTON

ID_TIMER = 100

class Fht80(wx.Panel):

    def __init__(self, parent, thread):
        self.parent = parent
        self.thread = thread
        self.show = SHOW_ALL
        self.threadCount = 20

        wx.Panel.__init__(self, parent = parent)

        self.labelFhtLst = wx.StaticText(self, -1, "FHT80:")
        self.fht80ListBox = wx.ListBox(self, -1, choices = [], size= (230,5), style = wx.LB_SINGLE)
        self.labelTfLst = wx.StaticText(self, -1, "TF:")
        self.TfListBox = wx.ListBox(self, -1, choices = [], style = wx.LB_SINGLE)
        self.labelFhtTfLst = wx.StaticText(self, -1, "Connections:")
        self.fht80TfListBox = wx.ListBox(self, -1, choices = [], style = wx.LB_SINGLE)
        self.sizer_DefStBox = wx.StaticBox(self, -1, "Defaults")

        self.panelRealtime = wx.Panel(self, -1)
        self.fht_grid = wx.grid.Grid(self.panelRealtime, -1)
        self.tf_grid = wx.grid.Grid(self.panelRealtime, -1)
        self.tfun_chk = wx.CheckBox(self.panelRealtime, -1, "TF UnId Enable:")
        self.tf_un_grid = wx.grid.Grid(self.panelRealtime, -1)
        self.sizer_Realtime_staticbox = wx.StaticBox(self.panelRealtime, -1, "Real Time")

        self.refreshButton = wx.Button(self.panelRealtime, label="", size=(95, 28))
        self.clearButton = wx.Button(self.panelRealtime, label="", size=(95, 28))

        self.timer=wx.Timer(self, ID_TIMER)

        self.__set_properties()
        self.__do_layout()


        # attach the event handlers
        self.__attach_events()


    def __set_properties(self):
        if self.show & SHOW_DEFAULT:
            self.fht80ListBox.Clear()
            self.TfListBox.Clear()
            self.fht80TfListBox.Clear()

        if self.show & SHOW_REALTIME:
            self.fht_grid.CreateGrid(1, 4)
            self.tf_grid.CreateGrid(1, 4)
            self.tf_un_grid.CreateGrid(1, 4)
            self.defaultFhtGrid()
            self.defaultTfGrid()
            self.defaultTfUnGrid()

            self.tfun_chk.SetValue(False)


        if self.show & SHOW_BUTTON:
            self.refreshButton.SetLabelText("Refresh ( 20 )")
            self.clearButton.SetLabelText("Clear")

    def __do_layout(self):
        self.sizer_DefStBox.Lower()
        sizer_default = wx.StaticBoxSizer(self.sizer_DefStBox, wx.VERTICAL)
        self.sizer_Realtime_staticbox.Lower()
        sizer_realtime = wx.StaticBoxSizer(self.sizer_Realtime_staticbox, wx.VERTICAL)

        sizer_win = wx.BoxSizer(wx.VERTICAL)

        gbs_default = wx.GridBagSizer(8,0)

        gbs_default.Add(self.labelFhtLst, (0,0))
        gbs_default.Add(self.fht80ListBox, (1,0), span=(7,1), flag=wx.EXPAND)

        gbs_default.Add(self.labelTfLst, (0,5))
        gbs_default.Add(self.TfListBox, (1,5), span=(7,1), flag=wx.EXPAND)

        gbs_default.Add(self.labelFhtTfLst, (0,10))
        gbs_default.Add(self.fht80TfListBox, (1,10), span=(7,1), flag=wx.EXPAND)


        sizer_default.Add(gbs_default, 0, flag=wx.ALL, border=5)
        sizer_default.AddSpacer(10)

        sizer_win.Add(sizer_default, 0, wx.EXPAND, 0)

        gbs_realtime = wx.GridBagSizer(0,0)

        gbs_realtime.Add(self.fht_grid, (1,0), span=(7,1))
        gbs_realtime.Add(self.tf_grid, (1,5), span=(7,1))

        gbs_realtime.Add(self.refreshButton, (1,10))
        gbs_realtime.Add(self.clearButton, (2,10), span=(7,1))

        gbs_realtime.Add(self.tfun_chk, (10,0))
        gbs_realtime.Add(self.tf_un_grid, (11,0), span=(7,1))

        sizer_realtime.Add(gbs_realtime, 0, flag=wx.ALL, border=5)

        self.panelRealtime.SetSizer(sizer_realtime)
        sizer_win.Add(self.panelRealtime, 0, wx.EXPAND, 0)


        self.SetSizer(sizer_win)
        self.SetAutoLayout(True)
        self.Layout()


    def __attach_events(self):
        self.Bind(wx.EVT_BUTTON, self.onRefresh, self.refreshButton)
        self.Bind(wx.EVT_BUTTON, self.onClear, self.clearButton)

        self.Bind(wx.EVT_TIMER, self.timerEvent, self.timer)


    def load(self):

        val = self.thread.dispath(True, 'f')

        self.fht80ListBox.Clear()
        self.TfListBox.Clear()
        self.fht80TfListBox.Clear()

        for i in val:
            self.fht80ListBox.Append('[ '+str(i)+' ]    ' + self.convDecF(val[i]))

        val = self.thread.dispath(True, 'a')

        for i in val:
            t_list = self.convDecT(val[i])
            if len(t_list) != 0:
                self.TfListBox.Append('[ '+str(i)+' ]     ' + t_list)

        val = self.thread.dispath(True, 'c')

        for i in val:
            t_list = self.convFhtTf(val[i])
            if len(t_list) != 0:
                self.fht80TfListBox.Append('[ '+str(i)+' ]     ' + t_list)

        self.loadRealtime()
        self.timer.Start(1000)

        self.Layout()
        self.Fit()


    def loadRealtime(self):

        self.defaultFhtGrid()
        self.defaultTfGrid()

        val0 = self.thread.dispath(True, 'H')
        val1 = self.thread.dispath(True, 'E')
        val2 = self.thread.dispath(True, 'A')

        if self.tfun_chk.GetValue():
            val3 = self.thread.dispath(True, 'U')

        for i in val0:
            self.fht_grid.SetRowLabelValue(i, '[ ' + str(i) + ' ]')

            val_tmp = self.convDecF(val0[i])
            self.fht_grid.SetCellValue(i, 0, val_tmp[:2])
            self.fht_grid.SetCellValue(i, 1, val_tmp[len(val_tmp)-2:])


            self.fht_grid.SetCellValue(i, 2, val1[i][:3])
            self.fht_grid.SetCellValue(i, 3, 'x' + val1[i][len(val1[i])-2:])

            self.fht_grid.InsertRows(i + 1)

        self.fht_grid.DeleteRows(self.fht_grid.GetNumberRows() -1)


        for i in val2:
            self.tf_grid.SetRowLabelValue(i, '[ ' + str(i) + ' ]')

            val_tmp = self.convDecT(val2[i][:len(val2[i])-4])
            j_i = 0
            for j in val_tmp:
                j_inx = val_tmp.find(' ')

                if j_inx == -1:
                    break

                self.tf_grid.SetCellValue(i, j_i, val_tmp[:j_inx])
                val_tmp = val_tmp[j_inx+2:]
                j_i += 1

            if self.tf_grid.GetCellValue(i, 0) != '':
                self.tf_grid.SetCellValue(i, 3, 'x' + val2[i][len(val2[i])-2:])



            self.tf_grid.InsertRows(i + 1)

        self.tf_grid.DeleteRows(self.tf_grid.GetNumberRows() -1)

        if self.tfun_chk.GetValue():

            self.tf_un_grid.SetRowLabelValue(0, '[ ' + str(0) + ' ]')

            valTmp = val3[2:]
            self.tf_un_grid.SetCellValue(0, 0, valTmp[:3])
            valTmp = valTmp[3:]
            self.tf_un_grid.SetCellValue(0, 1, valTmp[:4])
            valTmp = valTmp[4:]
            self.tf_un_grid.SetCellValue(0, 2, valTmp[:3])
            valTmp = valTmp[4:]
            self.tf_un_grid.SetCellValue(0, 3, 'x' + valTmp[:3])
        else:

            self.tf_un_grid.SetRowLabelValue(0, '')
            self.tf_un_grid.SetCellValue(0, 0, '')
            self.tf_un_grid.SetCellValue(0, 1, '')
            self.tf_un_grid.SetCellValue(0, 2, '')
            self.tf_un_grid.SetCellValue(0, 3, '')


########################################################################################################################
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


    def convDecT(self, val):
        str_tmp = ''
        tmp = {}

        t = val[1:]
        t_inx = t.find('20')

        if t_inx < 2:
            tmp[0] = '0x' + t[t_inx-1]
        else:
            tmp[0] = '0x' + t[t_inx-2] + t[t_inx-1]

        t = t[t_inx+2:]
        t_inx = t.find('20')

        if t_inx < 2:
            tmp[1] = '0x' + t[t_inx-1]
        else:
            tmp[1] = '0x' + t[t_inx-2] + t[t_inx-1]

        tmp[2] = '0x' + t[t_inx+2:]

        if int(tmp[0], 0) == 0 & int(tmp[1], 0) == 0 & int(tmp[2], 0) == 0:
            return ''

        for i in tmp:
            if int(tmp[i], 16) > 0x09:
                str_tmp += str(int(tmp[i], 16))
            else:
                str_tmp += '0' + str(int(tmp[i], 16))

            str_tmp += '  '



        return  str_tmp

    def convFhtTf(self, val):

        tmp = {}

        t = val[1:]
        t_inx = t.find('20')

        if t_inx < 2:
            tmp[0] = '0x' + t[t_inx-1]
        else:
            tmp[0] = '0x' + t[t_inx-2] + t[t_inx-1]

        tmp[1] = '0x' + t[t_inx+2:]

        if int(tmp[0], 0) == 0x00:
            return ''

        i = 0
        while i != self.fht80ListBox.GetItems():
            f_str = self.fht80ListBox.Items[i]
            f_inx = f_str.find(str(int(tmp[0], 0)) + '   01')
            if f_inx != -1:
                f_inx = i
                break
            i += 1

        if i == self.fht80ListBox.GetItems():
            return ''

        f_str = self.fht80ListBox.Items[f_inx]
        t_str = self.TfListBox.Items[int(tmp[1], 0)]
        str_tmp = f_str + '  <-->  ' + t_str

        return  str_tmp

########################################################################################################################

    def defaultFhtGrid(self):
        t = self.fht_grid.GetNumberRows()

        if self.fht_grid.GetNumberRows()-1 > 0:
            self.fht_grid.DeleteRows(0,self.fht_grid.GetNumberRows()-1,True)


        for i in range(4):
            #self.fht_grid.SetColSize(i, 50) // PC
            self.fht_grid.SetColSize(i, 80)

        self.fht_grid.SetColLabelValue(0, "Hc1" )
        self.fht_grid.SetColLabelValue(1, "Hc2" )
        self.fht_grid.SetColLabelValue(2, "Ext" )
        self.fht_grid.SetColLabelValue(3, "Value" )

        #self.fht_grid.SetRowLabelSize(30)
        self.fht_grid.SetRowLabelSize(50)
        self.fht_grid.SetRowLabelValue(0, "")


        self.fht_grid.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        self.fht_grid.SetDefaultCellAlignment( wx.ALIGN_CENTRE, wx.ALIGN_TOP )

    def defaultTfGrid(self):

        if self.tf_grid.GetNumberRows()-1 > 0:
            self.tf_grid.DeleteRows(0,self.tf_grid.GetNumberRows()-1,True)


        for i in range(4):
            #self.tf_grid.SetColSize(i, 50)  // PC
            self.tf_grid.SetColSize(i, 50)

        self.tf_grid.SetColLabelValue(0, "Hc1" )
        self.tf_grid.SetColLabelValue(1, "Hc2" )
        self.tf_grid.SetColLabelValue(2, "Hc3" )
        self.tf_grid.SetColLabelValue(3, "Value" )

        #self.tf_grid.SetRowLabelSize(30)  //PC
        self.tf_grid.SetRowLabelSize(50)
        self.tf_grid.SetRowLabelValue(0, "")


        self.tf_grid.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        self.tf_grid.SetDefaultCellAlignment( wx.ALIGN_CENTRE, wx.ALIGN_TOP )

    def defaultTfUnGrid(self):

        if self.tf_un_grid.GetNumberRows()-1 > 0:
            self.tf_un_grid.DeleteRows(0,self.tf_un_grid.GetNumberRows()-1,True)


        for i in range(4):
            #self.tf_grid.SetColSize(i, 50)  // PC
            self.tf_un_grid.SetColSize(i, 50)

        self.tf_un_grid.SetColLabelValue(0, "Hc1" )
        self.tf_un_grid.SetColLabelValue(1, "Hc2" )
        self.tf_un_grid.SetColLabelValue(2, "Hc3" )
        self.tf_un_grid.SetColLabelValue(3, "Value" )

        #self.tf_grid.SetRowLabelSize(30)  //PC
        self.tf_un_grid.SetRowLabelSize(50)
        self.tf_un_grid.SetRowLabelValue(0, "")


        self.tf_un_grid.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        self.tf_un_grid.SetDefaultCellAlignment( wx.ALIGN_CENTRE, wx.ALIGN_TOP )

########################################################################################################################

    def onRefresh(self, event):
        self.loadRealtime()
        self.threadCount = 20
        self.refreshButton.SetLabelText("Refresh ( " + str(self.threadCount)+ ' )')
        event.Skip()

    def onClear(self, event):

        val = self.thread.dispath(True, 'D')
        if val[0] == 'x1':
            self.loadRealtime()

        event.Skip()

########################################################################################################################
#         Timer Event !
########################################################################################################################
    def timerEvent(self, event):
        if self.GetParent().GetParent().GetParent().fhtTread:
            if self.threadCount == 1:
                self.threadCount = 20
                self.loadRealtime()
            else:
                self.threadCount -= 1

            self.refreshButton.SetLabelText("Refresh ( " + str(self.threadCount)+ ' )')
        else:
            self.timer.Stop()
            self.threadCount = 20

        event.Skip()